import json
from bs4 import BeautifulSoup
import requests

senUrl = "https://bff.capitoltrades.com/politicians?page="
pNum = 1
urlEnder = "&pageSize=15"

req = requests.get(senUrl + str(pNum) + urlEnder)
senList = list(json.loads(req.text)["data"])

for sen in senList:
    print(sen["fullName"])


#poli = input("Input the name of the politicion you would like to track: ")

# req = requests.get("https://bff.capitoltrades.com/politicians?page=1&pageSize=15")

# formReq = json.loads(req.text)

# list = list(formReq["data"])

# first = list[0]["party"]

# print(first)





#https://www.capitoltrades.com/politicians?page=2

# url = "https://www.capitoltrades.com/trades?politician="

# result = requests.get(url)
# doc = BeautifulSoup(result.text, "html.parser")

# print(doc.prettify())