import json
import requests
import time

MIN_TRADES_WANTED = 20
ALL_POLITICIANS_API = "https://bff.capitoltrades.com/politicians?pageSize=all&page=1&metric=countTrades&metric=countIssuers&metric=dateLastTraded&metric=volume"
TRADE_API_START = "https://bff.capitoltrades.com/trades?page="
TRADE_API_END = "&pageSize=100&politician="
API_BUY_SELL_FILTER = "&txType=buy&txType=sell"
PAGE_START_NUM = "1"
API_KEYWORDS = (
    "data",
    "stats",
    "meta",
    "countTrades",
    "firstName",
    "lastName",
    "_politicianId",
    "paging",
    "totalPages",
    "txType"
)

TRANSACTION_TYPES = (
    "buy",
    "sell",
    "exchange",
    "receive"
)

def getPoliticians():
    pols = []
    rawData = requests.get(ALL_POLITICIANS_API).text
    data = json.loads(rawData)[API_KEYWORDS[0]]

    for polData in data:
        countTrades = polData[API_KEYWORDS[1]][API_KEYWORDS[3]]
        if(countTrades > MIN_TRADES_WANTED):
            fullName = " ".join([polData[API_KEYWORDS[4]], polData[API_KEYWORDS[5]]])
            pols.append({API_KEYWORDS[6] : polData[API_KEYWORDS[6]], "fullName" : fullName})    

    return pols


# Uses politicianId in order to see what trades they have made
def getPoliticianTrades(polID):
    startNum = 1
    tradesURL = tradeAPI(startNum, polID)
    req = requests.get(tradesURL)
    
    trades = filterData(json.loads(req.text)[API_KEYWORDS[0]])
    meta = json.loads(req.text)[API_KEYWORDS[2]]
    pages = meta[API_KEYWORDS[7]][API_KEYWORDS[8]]

    if (pages > startNum):
        allTrades = []
        allTrades.append(trades)
        startNum += 1

        while startNum <= pages:
            tradesURL = tradeAPI(startNum, polID)
            req = requests.get(tradesURL)
            trades = json.loads(req.text)[API_KEYWORDS[0]]
            filtTrades = filterData(trades)
            allTrades.append(filtTrades)
            startNum += 1
        
        return allTrades
    
    else:
        return trades
   

def tradeAPI(pageNum, polID):
    return "".join([TRADE_API_START, str(pageNum), TRADE_API_END, polID, API_BUY_SELL_FILTER])


def filterData(data):
    results = []
    for dataPoint in data:
        dataPoint.pop("labels")
        dataPoint.pop("politician")
        dataPoint.pop("issuer")
        results.append(dataPoint)
    
    return results


# This method combines all valid politicians and their trades into an Array of Dictionaries using the results from getPoliticians and utilizing the getPoliticianTrades method
def collectPoliticianTrades():
    politicianTrades = []
    politicians = getPoliticians()

    for pol in politicians:
        trades = getPoliticianTrades(pol[API_KEYWORDS[6]])
        politicianTrades.append({"politician" : pol, "trades" : trades})
        
        
        #temp to test
        if(pol["_politicianId"] == "P000197"):
            print(trades)

    
    return politicianTrades


def rankPolitician(politician):
    #Go through trades to see if politician made money or lost money based on their trades
    trades = politician["trades"]
    tradeByTickers = {}



    return


def groupBuySell(trades):
    buySellTrades = []




t1 = time.time()
collectPoliticianTrades()
t2 = time.time()
print(t2-t1)

#Grading system for politicians that calculates performance of individual 
#Who's consistently increasing their wealth vs who got lucky on big gamble 

#NP code: P000197