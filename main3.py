import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import time
from bs4 import BeautifulSoup
import json
import ssl

def maxCountUniv(nameSpecial, educationLevel):
    url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/speciality/page?pageNumber=0&pageSize=1&search=name_name::"+nameSpecial+";name_educationLevel_code::"+educationLevel+"&sort="
    #print(url)
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    req = req.json()
    return req["totalElements"]

def searchSpecial():
    url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/speciality/page?pageNumber=0&pageSize=2692&search=&sort="
    #print(url)
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    req = requests.get(url, headers = headers)
    print(url)
    req = req.json()
    a = set()
    for i in range(len(req["content"])):
        #print(req["content"][i]["name"]["name"])
        a.add(req["content"][i]["name"]["code"] + "!" + req["content"][i]["name"]["name"])
    print(a)
    print(len(a))
    input_csv("1234567", a)
    return req

def input_csv(filename, data):
    with open(f"data/{filename}.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
    for university in data:
        with open(f"data/{filename}.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            print(university)
            writer.writerow(
                [university]
            )

def dataShaping(request, iteration):
    universityInfo = dict()

    universityInfo["educationLevel"] = request["content"][iteration]["name"]['educationLevel']['name']
    #universityInfo["educationForms"] = request["content"][iteration]['educationForms']
    universityInfo["universityShortName"] = request["content"][iteration]['universityShortName']
    universityInfo["availablePlacesBudget"] = request["content"][iteration]['subSpecialities'][0]['availablePlacesBudget']
    universityInfo["passingScoreBudget"] = request["content"][iteration]['subSpecialities'][0]['passingScoreBudget']
    universityInfo["universityId"] = request["content"][iteration]['universityId']
    universityInfo["costFrom"] = request["content"][iteration]['subSpecialities'][0]['costFrom']

    #print(universityInfo["universityShortName"])
    return universityInfo


searchSpecial()