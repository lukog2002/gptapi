DB_NAME = 'apps'
DB_COLLECTION = 'applist' 
CONNECTION_STRING = "mongodb://mongo:27017/"


from pymongo import MongoClient
client = MongoClient(CONNECTION_STRING)

db = client[DB_NAME] 
collection = db[DB_COLLECTION]
print("mongo connected")
def insertData(document) : 
    print(collection.find_one({"app-name" : document['app-name']}))
    if collection.find_one({"app-name" : document['app-name']}) == None :  
        collection.insert_one(document)
        return "inserted" 
    return "app-name already exits"

def retrieveAllData() : 
    documents = collection.find({} , {'_id' : 0}) 
    lst = [] 
    for val in documents : 
        lst.append(val) 
    return lst 

def deleteApp(appName) :
    collection.delete_one({"app-name" : appName}) 