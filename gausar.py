import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

baseurl="https://www.unegui.mn/avto-mashin/-avtomashin-zarna//?page="
car_list=[]
for i in range(1,10):
    url = baseurl +str(i)

    response=requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print('error', url)
        continue
    #print(i)
    soup=BeautifulSoup(response.text, "html.parser")
    #print(soup)

    li_list = soup.find_all("li", {"class": "announcement-container"})
    for li in li_list:
        a = li.find('a')
        car_url = "https://www.unegui.mn"+a['href']
        #print(car_url)
        car_list.append(car_url)
print(len(car_list))
car_set=set(car_list)
print(len(car_set))

class Car:
    def __init__(self, title, price, p_year, i_year, url):
        self.title=title
        self.price=price
        self.produced_year=p_year
        self.imported_year=i_year
        self.url=url
def findFeature(li_list, header):
    ref = "li"
    for li in li_list:
        text = li.text.strip()
        if text.startswith(header):
            return text[len(header)].strip()
        return ref
it = 0
for url in car_set:
    it += 1
    if it > 50:
        break
    #print(url)
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print('error', url)
        continue
    soup=BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1", {"class": "title-announcement"}).text.strip()
    price = soup.find("div", {"class": "announcement-price__cost"}).text.strip()
    price = float(price.split('сая ₮')[0])
    #li_class = soup.find_all("li")
    #produced_year = findFeature(li_class, "Үйлдвэрлэсэн он: ")
    #import_year = findFeature(li_class, "Орж ирсэн он: ")
    #price=soup.find('div', class_="announcement-block__price").text.strip()
    # zoriulalt=soup.find("div", {"class": "announcement-block__description"}).text.strip()
    # hugatsaa=soup.find("div", {"class": "announcement-block__date"}).text.strip()
    #print(title, price)

    car_objects = []
    import csv

    with open('car_data1.csv', 'w', newline='', encoding='utf-8') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(['Title', 'Price'])
     for car in car_list:
        writer.writerow([title, price])
    

