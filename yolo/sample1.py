import configparser

from ultralytics import YOLO
import cv2
import math 

class YOLO_Detector():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.show = self.config.get("Detector","ShowVideo", fallback= "False")

        self.setupDetector()

    def setupDetector(self):
        # start webcam
        self.cap = cv2.VideoCapture(2)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # model
        self.model = YOLO("yolov8n.pt")

    def loop(self):
        while True:
            success, img = self.cap.read()

            results = self.model(img)

            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the video capture object and close the display window
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    dt = YOLO_Detector()
    dt.loop()