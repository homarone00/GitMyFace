#sample5
# configuration

from flask import Flask
from config import Config


appname = "IOT - sample5"
app = Flask(appname)
myconfig = Config()
app.config.from_object(myconfig)

myset=[]

@app.route('/')
def testoHTML():
    return '<h1>I love IoT</h1>'


@app.route('/list')
def printList():
    txt = ";".join(myset)
    return txt

@app.route('/addToList/<name>')
def addToList(name):
    myset.append(name)
    return str(len(myset))


if __name__ == '__main__':
    app.run(host=app.config.get('FLASK_RUN_HOST','0.0.0.0'), port=app.config.get('FLASK_RUN_PORT',80))