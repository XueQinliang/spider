# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:18:51 2020

@author: Qinliang Xue
"""

import requests
from bs4 import BeautifulSoup
from config import headers
import random
import re

def getip():
    h = random.randint(0, len(headers) - 1)
    data = requests.get('https://www.xicidaili.com/nn/',headers = headers[h],timeout = (5, 15),verify = False)
    soup = BeautifulSoup(data.text,'html.parser')
    li = []
    for i in soup.find_all('tr'):
        port = ''
        ip = ''
        for j in i.find_all('td'):
            if re.match("[+-]?\d+$",j.get_text()):
                port=j.get_text().strip('\n').strip()
            if re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",j.get_text()):
                ip=j.get_text().strip('\n').strip()
        if port != '' and ip != '':
            li.append({'http':'http://'+ip+':'+port,'https':'https://'+ip+':'+port})
    p = random.randint(0, len(li)-1)
    return li[p]

if __name__ == '__main__':
    print(getip())