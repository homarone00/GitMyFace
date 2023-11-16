import configparser

import paho.mqtt.client as mqtt

from ultralytics import YOLO
import cv2
import math 


class MQTT_client():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.pubtopic = self.config.get("MQTT","PubTopic", fallback= "traffic-light")

        self.setupMQTT()

    def setupMQTT(self):        
        self.clientMQTT = mqtt.Client()
        self.clientMQTT.on_connect = self.on_connect
        self.clientMQTT.on_message = self.on_message

        print("Connecting to MQTT broker...")

        self.clientMQTT.connect(
            self.config.get("MQTT","Server", fallback= "localhost"),
            self.config.getint("MQTT","Port", fallback= 1883), 60)

        self.clientMQTT.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def publish(self, data):
        self.clientMQTT.publish(self.pubtopic, data)

class YOLO_Detector():

    def __init__(self, mqtt_client):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.model_name = self.config.get("Detector","Model", fallback= "hotweels_car_yolov8n.pt")
        self.show = self.config.get("Detector","ShowVideo", fallback= "False")

        self.mqtt_client = mqtt_client

        self.setupDetector()

    def setupDetector(self):
        # start webcam
        self.cap = cv2.VideoCapture(2)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # model
        self.model = YOLO(self.model_name)

        # object classes
        self.classNames = ["car"]

    def loop(self):
        while True:
            success, img = self.cap.read()

            results = self.model(img, stream=True)

            # coordinates
            for r in results:
                boxes = r.boxes

                for i, box in enumerate(boxes):

                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # class name
                    cls_id = int(box.cls[0])

                    # confidence
                    confidence = math.ceil((box.conf[0]*100))/100

                    print("[#%d] %s - conf: %.2f" % (i, self.classNames[cls_id], confidence))
                    
                    if (self.show):
                        # put box in cam
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        # object details
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2

                        cv2.putText(img, self.classNames[cls_id], org, font, fontScale, color, thickness)

                self.mqtt_client.publish(len(boxes))
            
            if (self.show):
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break

        self.cap.release()

if __name__ == '__main__':
    mc = MQTT_client()
    dt = YOLO_Detector(mc)

    dt.loop()