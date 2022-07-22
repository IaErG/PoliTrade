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

# Recieves all politicians
def getPoliticians():
    pols = []

    # Recieves the data from the API and loads said data
    rawData = requests.get(POLITICIANS_API, politician_API_params).text
    data = json.loads(rawData)[API_KEYWORDS[0]]

    # Cycles through the data gathered to collect politician ID's used by API
    # and the name associated with the ID's, all stored in a dictionary 
    for polData in data:
        countTrades = polData[API_KEYWORDS[1]][API_KEYWORDS[3]]

        # Minimum amount of trades required as too few trades isn't going to work for the program
        if(countTrades > MIN_TRADES_WANTED):
            fullName = " ".join([polData[API_KEYWORDS[4]], polData[API_KEYWORDS[5]]])
            pols.append({API_KEYWORDS[6] : polData[API_KEYWORDS[6]], "fullName" : fullName})    

    # The array containing the politician name and ID Dictionaries is returned
    return pols


# Uses politicianId in order to see what trades they have made
def getPoliticianTrades(polID):

    # The politician ID is set in the API params in order to fetch their trades
    trade_API_params["politician"] = polID
    req = requests.get(TRADE_API, trade_API_params)
    
    # The data collected from the API is filtered to keep only what is wanted
    trades = filterData(json.loads(req.text)[API_KEYWORDS[0]])

    # Page number is stored in a variable to help know how many trades need to be cycled through 
    meta = json.loads(req.text)[API_KEYWORDS[2]]
    pages = meta[API_KEYWORDS[7]][API_KEYWORDS[8]]

    # If there's more than 1 page to check
    if (pages > trade_API_params["page"]):

        # The trades gathered is stored
        allTrades = []
        allTrades.append(trades)

        trade_API_params["page"] += 1

        # While loop to run until pages are all checked
        while trade_API_params["page"] <= pages:

            # Data is retrieved based on page number
            req = requests.get(TRADE_API, trade_API_params)
            trades = json.loads(req.text)[API_KEYWORDS[0]]

            # Trades are filtered and added to array of trades, page number is incrimented
            filtTrades = filterData(trades)
            allTrades.append(filtTrades)
            

        # Page number in API params is reset and the trades gathered are returned
        trade_API_params["page"] = PAGE_START_NUM
        return allTrades
    
    # The trades gathered are returned
    else:
        return trades
   

# FilterData method removes fields gathered from API which are unnecessary 
def filterData(data):
    results = []
    for dataPoint in data:
        if (isOption(dataPoint)):
            dataPoint.pop("labels")
            dataPoint.pop("politician")
            dataPoint.pop("issuer")
            results.append(dataPoint)   
    
    return results


# Method checks to see if asset bought/sold was of type 'stock-options'
def isOption(data):
    if (data["asset"]["assetType"] != "stock-options"):
        return True
    else:
        return False


# This method combines all valid politicians and their trades into an Array of Dictionaries using the results from getPoliticians 
# and utilizing the getPoliticianTrades method
def collectPoliticianTrades():
    politicianTrades = []
    politicians = getPoliticians()

    # For loop combines politician trades and politician info (Name, _politiciainId) using politician ID
    for pol in politicians:
        trades = getPoliticianTrades(pol[API_KEYWORDS[6]])
        politicianTrades.append({"politician" : pol, "trades" : trades})
        
        
        #temp to test
        if(pol["_politicianId"] == "P000197"):
            print(trades[0])

    
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