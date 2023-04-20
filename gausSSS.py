import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


class Car:
    def __init__(self, title, price, p_year, i_year, distance, motor, color):
        self.title = title
        self.price = price
        self.produced_year = p_year
        self.imported_year = i_year
        self.distance = distance
        self.motor = motor
        self.color = color


def findFeature(li_list, header):
    ref = None
    for li in li_list:
        text = li.text.strip()
        if text.startswith(header):
            ref = text[len(header):].strip()
            break
    return ref


baseurl = "https://www.unegui.mn/avto-mashin/-avtomashin-zarna//?page="
car_list = []
for i in range(1, 5):
    url = baseurl + str(i)

    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print('error', url)
        continue
    soup = BeautifulSoup(response.text, "html.parser")

    li_list = soup.find_all("li", {"class": "announcement-container"})
    for li in li_list:
        a = li.find('a')
        car_url = "https://www.unegui.mn" + a['href']
        car_list.append(car_url)

print(len(car_list))
car_set = set(car_list)
print(len(car_set))

it = 0
cars_data = []
for url in car_set:
    it += 1
    if it > 10:
        break

    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print('error', url)
        continue
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1", {"class": "title-announcement"}).text.strip()
    price = soup.find("div", {"class": "announcement-price__cost"}).text.strip()
    price = float(price.split('сая ₮')[0])
    li_class = soup.find_all("li")
    p_year = findFeature(li_class, "Үйлдвэрлэсэн он:")
    motor = findFeature(li_class, "Мотор багтаамж:")
    color = findFeature(li_class, "Дотор өнгө:")
    i_year = findFeature(li_class, "Орж ирсэн он:")
    distance = findFeature(li_class, "Явсан:")
    
    print(title, price, p_year, i_year, distance, motor, color)
    #car = Car(title, price, p_year, i_year, distance, motor, color)
    #cars_data.append(car.__dict__)
    #print(car)
#df = pd.DataFrame(cars_data)
#df.to_csv('gausar1.tsv', sep="\t", index=False)
