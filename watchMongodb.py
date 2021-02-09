import pymongo 
import logging
from datetime import datetime
import ntpath  # used to get filename from path

mdbClient   = pymongo.MongoClient("mongodb://localhost:27017/")
mdbDB       = mdbClient["camera"] 


def getCurrentID():

    logging.debug('APPLOG watchMongodb.CurrentID' )
    mdbCollection   = mdbDB["idCounter"]
    currentId       = mdbCollection.find_one()

    #check if collection exists
    if currentId == None:
        return 0
    else:
        return currentId["idCounter"]

def incrCurrentID():

    logging.debug('APPLOG watchMongodb.incrCurrentID' )
    mdbCollection   = mdbDB["idCounter"]
    currentId       = mdbCollection.find_one()

    if (currentId == None):
        mdbCollection.insert_one({"_id" : "singleCounter", "idCounter":1}) 
    else:
        mdbCollection.update_one({"_id" : "singleCounter", "idCounter": currentId["idCounter"]  }, {"$set" : {"idCounter":currentId["idCounter"] + 1 } } ) 

    newId = mdbCollection.find_one()
    return newId["idCounter"]

def insertThumbnail(filePath):

    logging.debug('APPLOG watchMongodb.insertThumbnail' )
    mdbCollection   = mdbDB["thumbnail"]

    # Build document
    now = datetime.now() # current date and time
    dateTimeStr = now.strftime("%d/%m/%Y %H:%M:%S")
    dateTime    = int(now.timestamp())
    fileName    = ntpath.basename(filePath)

    thumbnailDoc  = {"_id":incrCurrentID() , "timestamp": dateTime, "timestampStr":dateTimeStr , "filePath":filePath,"fileName":fileName}

    mdbCollection.insert_one(thumbnailDoc)

    return

def getThumbnailsForIndex(limit):
    logging.debug('APPLOG watchMongodb.getThumbnailsForIndex' )
    mdbCollection   = mdbDB["thumbnail"]

    mdbDocs = mdbCollection.find().sort("_id" , - 1).limit(limit)

    #build Thunbnail List


    reverseCounter = 0
    pageData    = {}
    thumbnails  = {}

    for doc in mdbDocs:
        thumbnails[reverseCounter] = doc
        reverseCounter +=1

    pageData['imageList']=thumbnails

    return  pageData
