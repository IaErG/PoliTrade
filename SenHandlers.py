import json
from bs4 import BeautifulSoup
import requests

# Recieves input from user in format FirstName LastName for what US Senator they wish to get the ID for
def formatSenName():
    name = input("Input the name of the politicion you would like to track: ").split(" ")
    return name

# Uses first and last name of senator to get their politicianId from capitol trades
def getSenCode(senName):
    senUrl = "https://bff.capitoltrades.com/politicians?page="
    pNum = 1
    urlEnder = "&pageSize=15"
    
    while pNum <= 15:
        req = requests.get(senUrl + str(pNum) + urlEnder)
        senList = list(json.loads(req.text)["data"])
        
        for sen in senList:
            if (sen["firstName"] == senName[0] and sen["lastName"] == senName[1]):
                return sen["_politicianId"]
        
        pNum += 1
    
# Uses politicianId in order to see what trades they have made
def getSenTrades(polID):
    tradesURL = "https://bff.capitoltrades.com/trades?politician=" + polID + "&txDate=all"

    req = requests.get(tradesURL)
    trades = list(json.loads(req.text)["data"])

    for t in trades:
        if t["txType"] == "sell":
            print(t["pubDate"])


getSenTrades(getSenCode(["Mark", "Green"]))