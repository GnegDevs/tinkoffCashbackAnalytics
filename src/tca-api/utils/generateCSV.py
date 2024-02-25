from utils.databaseController import *

def generateCSV(name):
    with open(f"tca-api/database/{name}_plot.csv", "w", encoding="UTF-8") as tempPlot:
        tempPlot.write("merchant_name,cashback,date\n")
        data = getPartnerDataByName(name)
        for cashbackData in data["cashbackData"]:
            tempPlot.write(f"{name},{cashbackData["cashback"]},{cashbackData["date"].split(" ")[0]}\n")

generateCSV("Перекресток")
