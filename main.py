import csv

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import time
from bs4 import BeautifulSoup
import json
import ssl

def input_csv(filename, data):
    with open(f"data/{filename}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            data
        )

def input_csv2(filename, data):
    with open(f"data/{filename}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9]
            )
        )

def find_speciality(url, spec):
    #print(url)
    # headers = {
    #     "accept": "*/*",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    # }

    #req = requests.get(url, headers=headers)
    req = ''
    while req == '':
        try:
            req = requests.get(url)
            break
        except:
            print("Error connection!")
            break
    if(req != ""):
        #print(req.status_code)
        src = req.text

        # print(src)
        soup = BeautifulSoup(src, "lxml")
        find_element = soup.find_all(string=spec)
        #print(find_element)


def links(url, pattern):
    new_set = set()
    len_url = len(url)
    print(pattern)
    for element in url:
        all_url = find_all_links(element, pattern)
        print(element, " --- ", all_url)
        new_set = new_set.union(all_url)
        #print(len(new_set))
    url = url.union(new_set)
    #print(len(url), url)
    while(len_url != len(url)):
        #print(url, len(url))
        sec = input('Let us wait for user input. Let me know how many seconds to sleep now.\n')
        print('Going to sleep for', sec, 'seconds.')
        time.sleep(int(sec))

        url = links(url, pattern)
    return url


def find_pattern(url):
    count = 0
    i = 0
    begin = 0
    end = 0
    #print(url, "urlll")
    while (count < 3 and i <= len(url) + 1):
        if (url[i] == "/"):
            # print(count, i)
            count += 1
            if (count == 2):
                begin = i
            if (count == 3):
                end = i
        i += 1

    pattern = url[begin + 1: end]
    if ("www" in pattern):
        pattern = pattern[4:]
    #print(pattern)
    url = url[:end]
    return pattern

def find_all_links(url, pattern):
   # university_list[13][6]#"https://www.altstu.ru/structure/unit/pk/" #university_list[13][6]
    #print(url)
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    req = requests.get(url, headers=headers)

    src = req.text

    soup = BeautifulSoup(src, "lxml")
    url_list = []
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        url_list.append(href)
    url1 = set(url_list)
    #print(url1)



    #print(url)

    url = "https://" + pattern + "/"
    all_url = set()
    for url_elem in url1:
        if (url_elem is not None and len(url_elem)!=0): #and  url_elem[len(url_elem)-1]=="/"):
            if (url_elem[0] == "/"):
                url_elem = url + url_elem
                if (pattern in url_elem):
                    all_url.add(url_elem)
            else:
                if (url_elem.find("http") != -1):
                    if (pattern in url_elem):
                        all_url.add(url_elem)
    return all_url

def parsing_Google(url_list):
    with open(f"data/output_with_link_bach.csv", "w", encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                "university",
                "average exam score",
                "rise/fall",
                "number of enrolled students",
                "no exams",
                "average score minus individual achievements",
                "link",
                "link to file"
            )
        )
    for url_value in url_list:
        if(url_value[6] != "link"):
            pattern = find_pattern(url_value[6])
            url = "https://google-search3.p.rapidapi.com/api/v1/search/q=site%3A"+pattern+"+%2809.03.01+OR+09.03.04+OR+01.03.02%29+AND+%282022+OR+2021%29+AND+мест+AND+план+приема+AND+%28направления+OR+программы%29"
            print(url)

            headers = {
                "X-User-Agent": "desktop",
                "X-Proxy-Location": "EU",
                "X-RapidAPI-Host": "google-search3.p.rapidapi.com",
                "X-RapidAPI-Key": "5053e03947mshae28242a2233da2p184758jsnf3886c2b3bf6"
            }

            req = requests.get(url, headers = headers)

            data = json.loads(req.text)
            print(len(data["results"]))

            if(len(data["results"]) != 0):
                if(len(data["results"])>10):
                    length = 10;
                else: length = len(data["results"]);
                for i in range(length) :
                    url_value.append(data["results"][i]["link"])
            else:
                url_value.append("0")

            input_csv("output_with_link_bach", url_value)
#url = "https://ege.hse.ru/rating/2021/87872953/all/?rlist=&ptype=0&vuz-abiturients-budget-order=ge&vuz-abiturients-budget-val=300"
#
#headers = {
#    "accept": "*/*",
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
#}
#
#req = requests.get(url, headers = headers)
#src = req.text
#print(src)
#
#with open("index.html", "w", encoding="utf-8") as file:
#   file.write(src)

#ssl._create_default_https_context = ssl._create_unverified_context

university_list = []

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_university = soup.find("tbody").find_all("tr")

for item in all_university:
    university = item.find_all("td")
    university_info_value = [
        university[0].text,
        university[1].text,
        university[2].text,
        university[3].text,
        university[4].text,
        university[5].text
    ]


    university_info = []
    for field in university_info_value:
        field = field.replace('\n',"")
        field = re.sub(r'\s+', ' ', field)
        university_info.append(field)

    university_list.append(university_info)

#print(university_list[200][0])

#university_list[200][0] = university_list[200][0].strip().replace(" ","+")
#print(university_list[200][0])

##################################################################################
################## получен список вузов с инфой о них  ###########################

# url = "https://www.google.com/search?q=" + university_list[200][0] + "+приемная+комиссия"
# print(url)
# headers = {
#     "accept": "*/*",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
# }

# req = requests.get(url, headers = headers)
# src = req.text
#
# soup = BeautifulSoup(src, "lxml")
# university_url = soup.find('div', id='search').find("a").get('href')
# university_list[200].append(university_url)
# print(university_list[200])

#input_csv("abc", university_list)

################################################## Парсинг ссылок и формирование csv #################################################

# with open(f"data/abbb.csv", "w", encoding="utf-8") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(
#         (
#             "university",
#             "average exam score",
#             "rise/fall",
#             "number of enrolled students",
#             "no exams",
#             "average score minus individual achievements",
#             "link"
#         )
#     )

#for univ_item in university_list:
# for val in range(277, len(university_list)):
#     university_list[val][0] = university_list[val][0].strip().replace(" ", "+")
#     #print(university_list[val][0])
#     url = "https://google-search3.p.rapidapi.com/api/v1/search/q=site%3Aruvuz.ru+" + university_list[val][0]
#     print(url)
#     headers = {
#         'x-user-agent': "desktop",
#         'x-proxy-location': "EU",
#         'x-rapidapi-host': "google-search3.p.rapidapi.com",
#         'x-rapidapi-key': "43b3415d78mshc6152b8d44ee9e2p1a745ajsn90b87c4575c8"
#     }
#
#     req = requests.request("GET", url, headers=headers)
#     data = json.loads(req.text)
#     #print(len(data["results"]))
#
#     if(len(data["results"]) != 0):
#         university_list[val].append(data["results"][0]["link"])
#     else:
#         university_list[val].append("0")
#
#     input_csv("abbb", university_list[val])
#     time.sleep(0.3)



##########################################  парсинг городов  ############################################
# for row in csv.reader(open('data/abb.csv', "r", encoding="utf-8"), delimiter=';'):
#       print(row)
#print(university_list)


##########################    преобразование ссылок
university_list = []
for row in csv.reader(open('data/abb.csv', "r", encoding="utf-8"), delimiter=';'):
    university_list.append(row)
#print(university_list[13][6])
#
# url = "https://www.rsvpu.ru/abitur/bachelor/" #university_list[13][6]#"https://www.altstu.ru/structure/unit/pk/" #university_list[13][6]
# print(url)
# headers = {
#     "accept": "*/*",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
# }
#
# req = requests.get(url, headers = headers, verify=False)
#
# src = req.text
#
# soup = BeautifulSoup(src, "lxml")
# url_list = []
# for a_tag in soup.find_all("a"):
#     href = a_tag.attrs.get("href")
#     url_list.append(href)
# url1 = set(url_list)
# print(url1)
#
#
# count = 0
# i = 0
# begin = 0
# end = 0
# while(count<3 and i<=len(url)+1):
#     if(url[i] == "/"):
#         print(count, i)
#         count+=1
#         if(count == 2):
#             begin = i
#         if(count == 3):
#             end = i
#     i+=1
# pattern = url[begin+1: end]
# print(pattern)
# if("www" in pattern):
#     pattern = pattern[4:]
# print(pattern)
# url = url[:end]
# print(url)
#
# all_url = set()
# for url_elem in url1:
#     if(url_elem is not None):
#         if (url_elem[0] == "/"):
#             url_elem = url + url_elem
#             if(pattern in url_elem):
#                 all_url.add(url_elem)
#         else:
#             if(url_elem.find("http")!= -1):
#                 if (pattern in url_elem):
#                     all_url.add(url_elem)
            #print(url_elem)

#pattern = find_pattern(university_list[13][6])#"https://www.rsvpu.ru/abitur/bachelor/")
#print(pattern)




url = "https://xn----7sbbi4acsqbibbdojqr6o.xn--p1ai/api/speciality/page?pageNumber=0&pageSize=1&search=&sort="
print(url)
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

req = requests.get(url, headers = headers)
print(req.json())









#parsing_Google(university_list)
#all_url = find_all_links("http://www.ds5.spb.ru/", pattern)#"https://www.rsvpu.ru/abitur/bachelor/", pattern)

#all_url = links(all_url, pattern)


#find_speciality("https://ivan.gubkin.ru/", "09.03.03")

# for url2 in all_url:
#     find_speciality(url2, "09.03.03")
###################################################################################



#
# with open(f"data/bb.csv", "w", encoding="utf-8") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(
#         (
#             "adc"
#         )
#     )
#
# with open(f"data/bb.csv", "a", encoding="utf-8") as file:
#     writer = csv.writer(file, delimiter=";")
#     for data in url:
#         print(data)
#         writer.writerow(
#             (
#                 data
#             )
#         )





# university_list = []
# for row in csv.reader(open('data/abb.csv', "r", encoding="utf-8"), delimiter=';'):
#     university_list.append(row)
# print(university_list[25][6])

# url = "https://www.altstu.ru/structure/unit/pk/article/stat2021/"
# print(url)
# headers = {
#     "accept": "*/*",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
# }
#
# req = requests.get(url, headers = headers)
# src = req.text
#
# #print(src)
# soup = BeautifulSoup(src, "lxml")
# url = soup.find_all(string= (re.compile(r'(09)\.(03)\.(03)')))
# print(url)

# for data in url:
#     #print(data.find_next("a"))
#     print(data)
#print(url)