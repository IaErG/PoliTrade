import json
from pydoc import pager
import requests

MIN_TRADES_WANTED = 20
ALL_POLITICIANS_API = "https://bff.capitoltrades.com/politicians?pageSize=all&page=1&metric=countTrades&metric=countIssuers&metric=dateLastTraded&metric=volume"
TRADE_API_START = "https://bff.capitoltrades.com/trades?page="
TRADE_API_END = "&pageSize=100&politician="
PAGE_START_NUM = "1"

# Politician trades api = https://bff.capitoltrades.com/trades?politician=C001075&txDate=all

def getPoliticians():
    pols = []
    rawData = requests.get(ALL_POLITICIANS_API).text
    data = json.loads(rawData)["data"]

    for polData in data:
        countTrades = polData["stats"]["countTrades"]
        if(countTrades > MIN_TRADES_WANTED):
            fullName = polData["firstName"] + " " + polData["lastName"]
            pols.append({"_politicianId" : polData["_politicianId"], "fullName" : fullName})    

    return pols


# Uses politicianId in order to see what trades they have made
def getPoliticianTrades(polID):
    startNum = 1
    tradesURL = tradeAPI(startNum, polID)
    req = requests.get(tradesURL)
    trades = json.loads(req.text)["data"]
    meta = json.loads(req.text)["meta"]
    pages = meta["paging"]["totalPages"]

    if (pages > startNum):
        allTrades = []
        allTrades.append(trades)
        startNum += 1

        while startNum <= pages:
            tradesURL = tradeAPI(startNum, polID)
            req = requests.get(tradesURL)
            trades = json.loads(req.text)["data"]
            allTrades.append(trades)
            startNum += 1
        
        return allTrades

    
    else:
        return trades
   

def tradeAPI(pageNum, polID):
    return TRADE_API_START + str(pageNum) + TRADE_API_END + polID


# This method combines all valid politicians and their trades into an Array of Dictionaries using the results from getPoliticians and utilizing the getPoliticianTrades method
def collectPoliticianTrades():
    politicianTrades = []
    politicians = getPoliticians()

    print(getPoliticianTrades(politicians[0]["_politicianId"]))




collectPoliticianTrades()


#Grading system for politicians that calculates performance of individual 
#Who's consistently increasing their wealth vs who got lucky on big gamble 