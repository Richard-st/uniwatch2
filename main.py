from flask import Flask, render_template, get_template_attribute
from flask_socketio import SocketIO
from flask_api import status
import watchMongodb
import watchWatchdog
import logging  
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
socketio = SocketIO(app,logger=True, cors_allowed_origins='*')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    pageData = watchMongodb.getThumbnailsForIndex(3)
    return render_template('index.html',pageTitle='Index',pageData=pageData)


def sendImagesToBrowsers(source):

    print ("***************Send from :" + source)
    pageData = watchMongodb.getThumbnailsForIndex(3)
    #smallGallery = get_template_attribute('macros.html', 'smallGallery')
    # socketio.send(smallGallery(pageData),broadcast=True)
    print (socketio)
    socketio.send("Sent from :" + source,broadcast=True)

# def sendImagesToBrowsers():
#     print ("Send")
#     socketio.send("File Loaded",broadcast=True)

def pushToWs():
    while True:
        print("send to page")
        sendImagesToBrowsers("Push Rows")
        time.sleep(15)


@app.route('/history')
def history():
    return render_template('history.html',pageTitle='History')

@app.route('/setup')
def setup():
    #htmlTest = get_template_attribute('setup.html', 'myMacro')
    #print (htmlTest())

    return render_template('setup.html',pageTitle='Setup')

#
# socketio
#

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!') 

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.send('my response', "Emit from Server", callback=messageReceived)




if __name__ == '__main__':

    #pushThread = threading.Thread(target=pushToWs)
    #pushThread.start()


    notifyThread = threading.Thread(target=watchWatchdog.notify)
    notifyThread.start()
    socketio.run(app, host='0.0.0.0')
    notifyThread.join()
    #pushThread.join()