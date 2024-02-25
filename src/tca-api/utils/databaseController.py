import pymongo
from bson.objectid import ObjectId
from datetime import datetime

mdb_client = pymongo.MongoClient("mongodb://host.docker.internal:27017/")
database = mdb_client["tinkoffCashbackAnalytics"]["partnersData"]

def getPartnerDataById(id):
    query = {"_id": ObjectId(id)}
    return database.find_one(query)

def getPartnerDataByName(name):
    query = {"name": name}
    return database.find_one(query)

def savePartnerData(name, budget):
    partnerData = {"name": name, "budget": budget, "cashbackData": [{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "name": "", "cashback": 0}], "isStopped": False}
    return database.insert_one(partnerData)

def updateCashbackData(id, newCashback):
    query = {"_id": ObjectId(id)}
    partner = database.find_one(query)

    if not newCashback["date"]:
        newCashback["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cashbackData = partner["cashbackData"]
    cashbackData.append(newCashback)

    newValues = {"$set": {"cashbackData": cashbackData}}
    return database.update_one(query, newValues)


