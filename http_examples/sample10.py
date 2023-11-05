# sample10
# request types

from flask import Flask
from config import Config
from flask import render_template, request, jsonify

appname = "IOT - sample10"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

myset=[]


@app.errorhandler(404)
def page_not_found(error):
    return 'Errore', 404

@app.route('/')
def testoHTML():
    if request.accept_mimetypes['application/json']:
        return jsonify( {'text':'I Love IoT'})
    else:
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