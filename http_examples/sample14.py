#sample14: openAPI from sample6
# pip install -U flask-openapi3

from flask import Flask
from config import Config

# specific imports:
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI


appname = "IOT - sample14"

info = Info(title=appname, version="1.0.0")
app = OpenAPI(appname, info=info)

myconfig = Config()
app.config.from_object(myconfig)

myset=[]


@app.get('/')
def testoHTML():
    '''
    This is the homepage
    '''
    return '<h1>I love IoT</h1>'


@app.get('/list')
def printList():
    txt = ";".join(myset)
    return txt

@app.post('/addToList/<name>', methods=['POST'])
def addToList(name):
    '''
    first line

    after a blank line

    '''
    myset.append(name)
    return str(len(myset))


if __name__ == '__main__':
    app.run(host=app.config.get('FLASK_RUN_HOST','0.0.0.0'), port=app.config.get('FLASK_RUN_PORT',80))