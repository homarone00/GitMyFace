# sample 7
# rendering with templates

from flask import Flask
from config import Config
from flask import render_template
import os

appname = "IOT - " + os.path.basename(__file__)
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

myset=[]

@app.route('/')
def testoHTML():
    return '<h1>I love IoT</h1>'


@app.route('/list', methods=['GET'])
def printList():
    return render_template('lista.html', lista=myset)

@app.route('/addToList/<name>', methods=['POST'])
def addToList(name):
    myset.append(name)
    return str(len(myset))



if __name__ == '__main__':
    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)