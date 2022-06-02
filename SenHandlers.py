import json
import requests

def getAllPol():
    polAPI = "https://bff.capitoltrades.com/politicians?pageSize=50&page="
    polAPIEnd = "&metric=countTrades&metric=countIssuers&metric=dateLastTraded&metric=volume"

    pols = []
    initialReq = requests.get(polAPI + "1" + polAPIEnd).text
    pageNums = json.loads(initialReq)["meta"]["paging"]["totalPages"]
    for i in range(int(pageNums)):
        pageText = requests.get(polAPI + str(i+1) + polAPIEnd).text
        data = list(json.loads(pageText)["data"])
        politicians = {}

        for polData in data:
            ct = polData["stats"]["countTrades"]
            if(ct > 20):
                politicians.update({polData["firstName"] + " " + polData["lastName"] : polData["_politicianId"]})
        

        if(len(politicians) > 0):
            for key in politicians.keys():
                pols.append({key : politicians.get(key)})

    return pols







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
        print(t["asset"], t["txType"])


print(getAllPol())

#Grading system for politicians that calculates performance of individual 
#Who's consistently increasing their wealth vs who got lucky on big gamble 