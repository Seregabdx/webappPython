import csv
import requests
import re
from bs4 import BeautifulSoup
import json
import urllib.parse
import numpy as np
import pandas as pd
import nltk
import string
import gensim
import gensim.downloader as api
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import classification_report

def maxCountUniv(nameSpecial, educationLevel):
    url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/speciality/page?pageNumber=0&pageSize=1&search=name_name::"+urllib.parse.quote_plus(nameSpecial)+";name_educationLevel_code::"+educationLevel+"&sort="
    print(url)
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    req = req.json()
    return req["totalElements"]

def searchSpecial(nameSpecial, pageSize, educationLevel):
    url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/speciality/page?pageNumber=0&pageSize="+str(pageSize)+"&search=name_name::"+urllib.parse.quote_plus(nameSpecial)+";name_educationLevel_code::"+educationLevel+"&sort="
    #print(url)
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    req = requests.get(url, headers = headers)
    req = req.json()
    return req

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


def input_csv(filename, data):
    with open(f"data/{filename}.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                "Название",
                "Средний балл ЕГЭ",
                "Рост/Падение",
                "Количество студентов, зачисленных на бюджет",
                "Количество БВИ",
                "Средний балл с вычетом ИД?",
                "Форма обучения",
                "Количество бюджетных мест на специальности",
                "Средний балл",
                "Стоимость",
                "Форма обучения",
                "Количество бюджетных мест на специальности",
                "Средний балл",
                "Стоимость",
                "Id лого",
                "Адрес",
                "Наличие военной кафедры",
                "Наличие отсрочки от армии",
                "Ссылка на документ о приеме"
            )
        )
    for university in data:
        with open(f"data/{filename}.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            print(university)
            writer.writerow(
                university
            )

def output_csv(filename):
    data = []
    for row in csv.reader(open(f'data/{filename}.csv', "r"), delimiter=';'):
        data.append(row)
    return data

def stringCorrection(str):
    correctUniversity = str
    correctUniversity = correctUniversity.replace('гос.', "государственный")
    correctUniversity = correctUniversity.replace('Моск.', "Московский")
    correctUniversity = correctUniversity.replace('Гос.', "Государственный")
    correctUniversity = correctUniversity.replace('ин-т.', "институт")
    correctUniversity = correctUniversity.replace('Ин-т.', "Институт")
    correctUniversity = correctUniversity.replace('ун-т.', "университет")
    correctUniversity = correctUniversity.replace('Ун-т.', "Университет")
    correctUniversity = correctUniversity.replace('им.', "имени")
    correctUniversity = correctUniversity.replace('техн.', "технический")
    correctUniversity = correctUniversity.replace('технол.', "технологический")
    #correctUniversity = correctUniversity.replace('г.', "город")
    correctUniversity = correctUniversity.replace(',', "")
    startPosition = correctUniversity.find("г.")
    if(startPosition != -1):
        #print(correctUniversity)
        correctUniversity = correctUniversity[0:startPosition]
        #print(correctUniversity)
    return correctUniversity

def dataCorrection(filename):
    # for row in csv.reader(open(f'data/{filename}.csv', "r", encoding="utf-8"), delimiter=';'):
    #     print(row)

    with open("index.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_university = soup.find("tbody").find_all("tr")

    university_list = []
    for item in all_university:
        university = item.find_all("td")
        correctUniversity = stringCorrection(university[0].text)
        #print(correctUniversity)

        university_info_value = [
            correctUniversity,
            university[1].text,
            university[2].text,
            university[3].text,
            university[4].text,
            university[5].text
        ]

        university_info = []
        for field in university_info_value:
            field = field.replace('\n', "")
            field = re.sub(r'\s+', ' ', field)
            university_info.append(field)
        university_list.append(university_info)

    input_csv(filename, university_list)

def collectionData(specialName, educationLevels):
    universityName = []
    data = searchSpecial(specialName, maxCountUniv(specialName, educationLevels), educationLevels)
    for i in range(maxCountUniv(specialName, educationLevels)):
        univ = dataShaping(data, i)
        universityName.append(univ)#["universityShortName"])

    arrayWord = []
    for univ in universityName:
        arrayWord.append(univ["universityShortName"].split())
        #print(arrayWord)
    return universityName

def universityСomparison(filename, educationLevels, univSpeciality):
    #dataCorrection(filename)
    universityListFirst = output_csv(filename);
    #print(universityListFirst)
    splitUnivNameFirst = wordBreaking(universityListFirst)
    splitUnivNameSecond = collectionData(univSpeciality, educationLevels)
    #print(splitUnivNameSecond)


    #firstNameUniv = splitUnivNameFirst[157]#155

    finalResult = []
    for firstNameUniv in splitUnivNameFirst:
        finalResult.append(searchMatches(splitUnivNameSecond, firstNameUniv))


    empty = 0;
    counter = 0;
    for i in finalResult:
        if(len(i) != 0):
            #print(i)
            if (i[1] == "Не найдено"):
                empty = empty + 1

        counter = counter +1
    #print(counter, empty)
    #name = input()
    #print(universityListFirst[10])


    specialName = univSpeciality
    universityName = []
    data = searchSpecial(specialName, maxCountUniv(specialName, educationLevels), educationLevels)
    for i in range(maxCountUniv(specialName, educationLevels)):
        univ = dataShaping(data, i)
        universityName.append(univ)

    final = compilingCSV(finalResult, universityListFirst, universityName)
    #input_csv("final", final)

    return final


def compilingCSV(finalResult, universityListFirst, universityName):
    final = []
    #print(universityListFirst[1])
    #print(len(universityName))
    for i in range(len(finalResult)):
        if(len(finalResult[i]) != 0):
            if(finalResult[i][1] != "Не найдено"):
                universityListFirst[i].append(finalResult[i][1]['educationLevel'])
                universityListFirst[i].append(finalResult[i][1]['availablePlacesBudget'])
                universityListFirst[i].append(finalResult[i][1]['passingScoreBudget'])

                universityListFirst[i].append(finalResult[i][1]['costFrom'])
                #print(finalResult[i][1]['costFrom'])
                #universityListFirst[i].append(finalResult[i][1]['universityShortName'])
                universityListFirst[i].append(finalResult[i][1]['universityId'])


                finalValue = universityListFirst[i]#, finalResult[i][1]['educationLevel'], finalResult[i][1]['availablePlacesBudget'], finalResult[i][1]['passingScoreBudget']]
                final.append(finalValue)
                #print(finalValue)
    return final

def searchMatches(splitUnivNameSecond, firstNameUniv):
    result = "Не найдено"
    res = []
    lastCounter = 0

    # train = pd.read_csv("data/univ1.csv", delimiter="\t", quoting=3)
    # test = pd.read_csv("data/univ2.csv", delimiter="\t", quoting=3)
    # tokenizer = nltk.WordPunctTokenizer()
    # wordnet_lemmatizer = WordNetLemmatizer()
    # train_sents = [i.split() for i in train]
    # test_sents = [i.split() for i in test]
    # word2vec = Word2Vec(sentences=train_sents + test_sents,
    #                     min_count=20,
    #                     window=5,
    #                     sample=6e-5,
    #                     vector_size=300,
    #                     workers=4)
    # X = []
    # y = []
    # for i, sent in enumerate(train_sents):
    #     y.append(train['sentiment'][i])
    #     vectors = []
    #     for word in sent:
    #         if word in word2vec.wv:
    #             vectors.append(word2vec.wv[word])
    #         else:
    #             vectors.append(list(np.zeros(300)))
    #     X.append(np.mean(vectors, axis=0))
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    # model = SGDClassifier(alpha=0.00007, l1_ratio=0.15)
    # model.fit(X_train, y_train)
    #
    # y_pred = model.predict(X_test)
    #
    # X_sub = []
    # ids = []
    # for i, sent in enumerate(test_sents):
    #     ids.append(test['id'][i].replace('"', ''))
    #     vectors = []
    #     for word in sent:
    #         if word in word2vec.wv:
    #             vectors.append(word2vec.wv[word])
    #         else:
    #             vectors.append(list(np.zeros(300)))
    #     X_sub.append(np.mean(vectors, axis=0))
    #
    # res1 = model.predict(X_sub)


    for univNameSecond in splitUnivNameSecond:
        counterWord = 0
        for univNameWordFirst in firstNameUniv:
            if (univNameSecond["universityShortName"].find(univNameWordFirst) != -1):
                counterWord = counterWord + 1
                # print(counterWord)
        if (counterWord > lastCounter and univNameSecond["universityShortName"].lower().find("филиал") == -1):
            result = univNameSecond #добавить счетчик для добавления еще одного списка
            #print(counterWord, lastCounter)
            lastCounter = counterWord
            # print(counterWord)
            res = []
            res.append(firstNameUniv)
            if (len(firstNameUniv) != counterWord):
                res.append("Не найдено")
            else:
                res.append(result)
            res.append(counterWord)
    #print(res, "-------------")
    return res


def wordBreaking(universityList):
    arrayWord = []
    for univ in universityList:
        arrayWord.append(univ[0].split())
    #print(arrayWord[155])
    return arrayWord


def addUnivInfo(matchList):
    returnData = []
    for elemList in matchList:
        univData = elemList[:14]
        partURL = elemList[14]
        #print(partURL)
        url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/university/?id=" + partURL
        print(url)
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }

        req = requests.get(url, headers=headers)
        req = req.json()
        univData.append(req["logo"])
        univData.append(req["physicalAdress"])
        univData.append(req["hasMilitaryDepartment"])
        univData.append(req["hasArmyRespite"])
        univData.append(req["linkPlaces"])
        #univData.append(req["linkOrder"])
        print(univData)
        returnData.append(univData)

    return returnData

def finalData(univSpeciality):
    matchList1 = universityСomparison("test", "BACHELOR", univSpeciality)
    matchList2 = universityСomparison("test", "MAGISTRACY", univSpeciality)
    # print(matchList1)
    matchList = []
    # for i in range(len(matchList2)):
    #     matchList.append(matchList1[i] + matchList2[i])

    # print(matchList2[0][0])

    for i in matchList1:
        res = 0
        for j in matchList2:
            if (i[0] == j[0]):
                res = i[0:10] + j[6:10] + [i[10]]

        if (res != 0):
            matchList.append(res)
        else:
            res = i[0:10] + [0] + [0] + [0] + [0] + [i[10]]
            matchList.append(res)

    final = addUnivInfo(matchList)

    input_csv(univSpeciality, final)

    final = importJSON(univSpeciality, final)
    return final


def importJSON(filename, data):
    result = []
    for i in data:
        resultData = {
            "universityName" : i[0],
            "universityLogo" : i [14],
            "universityAdress" : i[15],
            "linkPlaces": i[18],
            "universityInfo" : {
                "gradePointAverage" : i[1],
                "ratingChange" : i[2],
                "budgetPlaces" : i[3],
                "withoutEntranceTests" : i[4],
                "minusID" : i[5],
                "hasMilitaryDepartment" : i[16],
                "hasArmyRespite": i[17]
            },
            "bachelor" : {
                "name" : i[6],
                "budgetPlaces" : i[7],
                "gradePointAverage" : i[8],
                "educationCost" : i[9]
            },
            "magistracy":{
                "name": i[10],
                "budgetPlaces": i[11],
                "gradePointAverage": i[12],
                "educationCost": i[13]
            }
        }
        result.append(resultData)

    out_file = open(f"{filename}.json", "w")
    json.dump(result, out_file, indent=6)

    return result

#dataShaping(searchSpecial("Прикладная информатика", maxCountUniv("Прикладная информатика")), 0)
#dataCorrection("test")

# for i in matchList:
#     print(i)
data = []
for row in csv.reader(open(f'data/speciality.csv', "r"), delimiter=';'):
    data.append(row[0].split("!")[1])
    print(row[0].split("!")[1])
for i in data:
    print(i)
#print(finalData(urllib.parse.quote_plus(str("Биология".split(",")[0]))))
    try:
        print(str(i).split(",")[0])
        print(finalData(str(i).split(",")[0]))
    except Exception:
        print("Error")


in_file = open("myfile.json", "r")
abc = json.load(in_file)

print(abc)
input("fd")
#finalData("")
#finalData("Прикладная математика и информатика")

