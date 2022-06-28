import json
import requests
import time

PAGE_START_NUM = 1
MIN_TRADES_WANTED = 20
POLITICIANS_API = "https://bff.capitoltrades.com/politicians"
TRADE_API = "https://bff.capitoltrades.com/trades"

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

politician_API_params = {
    "page" : PAGE_START_NUM,
    "pageSize" : "all",
    "metric" : ["countTrades", 
                "countIssuers", 
                "dateLastTraded", 
                "volume"]
}

trade_API_params = {
    "page" : PAGE_START_NUM,
    "pageSize" : 100,
    "politician" : None,
    "txType" : ["buy", "sell"]
}

def getPoliticians():
    pols = []
    rawData = requests.get(POLITICIANS_API, politician_API_params).text
    data = json.loads(rawData)[API_KEYWORDS[0]]

    for polData in data:
        countTrades = polData[API_KEYWORDS[1]][API_KEYWORDS[3]]
        if(countTrades > MIN_TRADES_WANTED):
            fullName = " ".join([polData[API_KEYWORDS[4]], polData[API_KEYWORDS[5]]])
            pols.append({API_KEYWORDS[6] : polData[API_KEYWORDS[6]], "fullName" : fullName})    

    return pols


# Uses politicianId in order to see what trades they have made
def getPoliticianTrades(polID):
    trade_API_params["politician"] = polID
    req = requests.get(TRADE_API, trade_API_params)
    
    trades = filterData(json.loads(req.text)[API_KEYWORDS[0]])
    meta = json.loads(req.text)[API_KEYWORDS[2]]
    pages = meta[API_KEYWORDS[7]][API_KEYWORDS[8]]

    if (pages > trade_API_params["page"]):
        allTrades = []
        allTrades.append(trades)
        trade_API_params["page"] += 1

        while trade_API_params["page"] <= pages:
            req = requests.get(TRADE_API, trade_API_params)
            trades = json.loads(req.text)[API_KEYWORDS[0]]
            filtTrades = filterData(trades)
            allTrades.append(filtTrades)
            trade_API_params["page"] += 1
        

        trade_API_params["page"] = PAGE_START_NUM
        return allTrades
    
    else:
        return trades
   

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




t1 = time.time()
collectPoliticianTrades()
t2 = time.time()
print(t2-t1)

#Grading system for politicians that calculates performance of individual 
#Who's consistently increasing their wealth vs who got lucky on big gamble 

#NP code: P000197