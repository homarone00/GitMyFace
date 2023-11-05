# sample4
# vector

from flask import Flask


appname = "IOT - sample4"
app = Flask(appname)

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
    if name == 'juve':
        pass
    else:
        myset.append(name)
    return str(len(myset))


if __name__ == '__main__':
    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)