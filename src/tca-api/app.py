from flask import Flask, jsonify, abort, request
from utils.databaseController import *
#from utils.forest2 import *
import csv

app = Flask(__name__)

@app.route("/tca/api/partners/<string:company_id>", methods=['GET'])
def getPartnerDataHandler(company_id):

    info = getPartnerDataById(company_id)

    if info:
        return jsonify({"task": {
            "id": str(info["_id"]), 
            "name": info["name"], 
            "budget": info["budget"],
            "spent_budget": sum(x["cashback"] for x in info["cashbackData"]),
            "isStopped": info["isStopped"]
            }}), 200
    return abort(404)

@app.route("/tca/api/partners", methods=["POST"])
def addPartnerDataHandler():
    if not request.json or (not "name" in request.json and not "budget" in request.json):
        return abort(400)
    
    savePartnerData(request.json["name"], request.json["budget"])

    info = getPartnerDataByName(request.json["name"])
    
    if info:
        return jsonify({"task": {
            "id": str(info["_id"]), 
            "name": info["name"], 
            "budget": info["budget"],
            "spent_budget": sum(x["cashback"] for x in info["cashbackData"])
            }}), 201
    return abort(404)

@app.route("/tca/api/partners/<string:company_id>/cashback", methods=["PUT"])
def updateCashbackDataHandler(company_id):
    if not request.json or (not "name" in request.json and not "cashback" in request.json):
        return abort(400)

    info = getPartnerDataById(company_id)
    
    if info: 
        if info["isStopped"]:
            return abort(405)
        updateCashbackData(company_id, {"date": request.json["date"] if "date" in request.json else "", "name": request.json["name"], "cashback": request.json["cashback"]})
        return "", 200
        
    return abort(404)

@app.route("/tca/api/partners/resetdatabse", methods=["POST", "GET"])
def resetDatabaseHandler():
    if not request.json or 'file' not in request.files:
        return abort(400)

    file = request.files["file"]
    if not file.filename.split(".")[-1] == "csv":
        abort(406)
    file.save("database/", "temp_database.csv")

    with open("database/temp_database.csv", "r") as database:
        csvReader = csv.reader(database, delimiter=",")
        for row in csvReader:
            if not getPartnerDataByName(row[0]):
                savePartnerData(row[0], 0)
            updateCashbackData(getPartnerDataByName(row[0])["_id"], row[-1])

    return "", 201

@app.route("/tca/api/partners/<string:name>", methods=['GET'])
def generatePlotHandler(name):
    Generateplot(name, getPartnerDataByName(name)["budget"])



@app.route('/', methods=['GET'])
def hello_world():
    return 'Moe Flask приложение в контейнере Docker.'

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=8080,)
