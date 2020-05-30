 si# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:24:58 2020

@author: Qinliang Xue
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pymysql
import time

ifhave = 0

db = pymysql.connect(
        host = "202.112.113.26",
        port= 3306,
        user = "test",
        password = "123456",
        database = "kaggle",
        charset = "utf8mb4")

def getInfo(soup):
    try:
        soup1 = soup.div
        retdict = {}
        retdict['scripturl'] = soup1.a['href']
        soup2 = soup1.span.div.select('div[class="kernel-list-item__synopsis"]')[0].div
        retdict['scriptname'] = soup2.span.div.get_text()
        soup3 = soup2.select('div[class="kernel-list-item__details"]')[0].find_all('span',recursive=False)
        retdict['dataurl'] = soup3[1].span.a['href']
        retdict['dataname'] = soup3[1].span.a.get_text()
        retdict['tags'] = soup3[-1].get_text()
        return retdict
    except:
        return {}

driver = webdriver.Chrome()     # 创建Chrome对象.
# 操作这个对象.
driver.get('http://kaggle.com/notebooks')
time.sleep(10)
#driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/span').click()
#time.sleep(10)
#driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div[1]/span[1]/div').click()
#driver.find_element_by_class_name('category-filter__search-box').send_keys(LABEL)
#time.sleep(5)
#driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div[2]/div/div[2]/span/div/span').click()
#time.sleep(5)
num = 10000
notend = True
cursor = db.cursor()
while notend:
    htmlstr = driver.page_source
    soup = BeautifulSoup(htmlstr,'lxml')
    contents = soup.body.main.div.div.select("#site-content")[0].div.next_sibling.div.next_sibling.div.div.div.div.next_sibling.div.next_sibling.div.div.contents
    print(len(contents))
    while num < len(contents):
        print(len(contents))
        if contents[num].get_text() != 'Loading more notebooks...':
            infodict = getInfo(contents[num])
            if infodict == {}:
                num += 1
                continue
            searchsql = "select * from all_notebook where scripturl = %s"
            try:
                cursor.execute(searchsql,[infodict['scripturl']])
            except:
                db.commit()
                cursor.close()
                db.close()
                db = pymysql.connect(
                    host = "202.112.113.26",
                    port= 3306,
                    user = "test",
                    password = "123456",
                    database = "kaggle",
                    charset = "utf8mb4")
                cursor = db.cursor()
                cursor.execute(searchsql,[infodict['scripturl']])
            ifin = cursor.fetchmany(1)
            if ifin != ():
                num += 1
                continue
            cursor.execute('set names utf8mb4;')
            sql = "insert all_notebook values (%s,%s,%s,%s,%s,%s)"
            data = [ifhave,*infodict.values()]
            try:
                cursor.execute(sql,data)
            except:
                db.commit()
                cursor.close()
                db.close()
                db = pymysql.connect(
                    host = "202.112.113.26",
                    port= 3306,
                    user = "test",
                    password = "123456",
                    database = "kaggle",
                    charset = "utf8mb4")
                cursor = db.cursor()
                cursor.execute(sql,data)
            print(num,infodict)
            num += 1
        elif contents[num].get_text() == 'No more notebooks to show':
            notend = False
            break
        else:
            break
    db.commit()
    #继续往下翻
    if not notend:
        break
    itemend = driver.find_element_by_class_name('smart-list__message')
    ActionChains(driver).move_to_element(itemend).perform()#定位鼠标到指定元素
    time.sleep(5)
cursor.close()
db.close()