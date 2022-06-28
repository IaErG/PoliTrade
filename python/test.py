import json
from bs4 import BeautifulSoup
import requests
import random

senUrl = "https://bff.capitoltrades.com/politicians"
politician_API_Params = {
    "page" : 1,
    "pageSize" : "all",
    "metric" : ["countTrades", 
                "countIssuers", 
                "dateLastTraded", 
                "volume"]
}

req = requests.get(senUrl, politician_API_Params)
senList = list(json.loads(req.text)["data"])

for sen in senList:
    print(sen["fullName"], politician_API_Params["page"])
    politician_API_Params["page"] = random.randint(0, 200)






politician_API_Params = {
    "pageSize" : "all",
    "page" : 1,
    "metric" : ["countTrades", 
                "countIssuers", 
                "dateLastTraded", 
                "volume"]
}

