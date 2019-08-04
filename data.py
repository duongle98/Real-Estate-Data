# -*- coding: utf-8 -*-
import sys
import codecs
import json


from bs4 import BeautifulSoup
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

link = "https://batdongsan.com.vn"
t = "/nha-dat-ban/p"
r = requests.get(link+t[0])
soup = BeautifulSoup(r.text, 'html.parser')

data = {}

def find_link(soup, link):
    l = []
    for i in soup.find_all("div", attrs={"class" : "p-title"}):
        for j in i.find_all("h3"):
            for k in j.find_all('a',href=True):
                l.append(link+k['href'])
    return l

def find_data(soup):
    address = soup.find_all('div', {"class": "right"})[1].text.strip()
    title = price = soup.find_all('span', {"class":"gia-title"})
    price = title[0].find('strong').text.strip()
    area = title[1].find('strong').text.strip()
    d = {'address': address, 'price': price, 'area': area}
    return d

l = []
i = 1
while i < 5000:
    r = requests.get(link+t+str(i))
    soup = BeautifulSoup(r.text, 'html.parser')
    l.extend(find_link(soup, link))
    i+=1

nha = []
for i in l:
    re = requests.get(i)
    s = BeautifulSoup(re.text, 'html.parser')
    res = find_data(s)
    nha.append(res)

with open('RealEstate.json', 'w') as file:
    json.dump(nha, file)

print("Done")