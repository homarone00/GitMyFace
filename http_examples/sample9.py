# sample9
# errors

from flask import Flask
from config import Config
from flask import render_template

appname = "IOT - sample9"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

myset=[]


@app.errorhandler(404)
def page_not_found(error):
    return 'Ops, I think you are looking for the wrong resource', 404

@app.route('/')
def testoHTML():
    return '<h1>I love IoT</h1>'


@app.route('/list', methods=['GET'])
def printList():
    return render_template('lista2.html', lista=myset)

@app.route('/addToList/<name>', methods=['POST'])
def addToList(name):
    myset.append(name)
    return str(len(myset))



if __name__ == '__main__':
    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)