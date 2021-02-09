
import main
import watchMongodb
import logging


def newFIleDetected():

    limit = 5
    pageData = watchMongodb.getThumbnailsForIndex(limit)

    ##send mqtt notification

    ## move files to static data

    ## push data to browser clients

    #with main.app.app_context():

    with main.app.test_request_context():
        #print ("socketio from controller " + str(flask_socketio) ) 


        
        main.sendImagesToBrowsers("file change")
