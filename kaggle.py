import re
import numpy as np
import os
import json
import requests
import time
import random
import pymysql
from config import dbinfo
#from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED, FIRST_COMPLETED

def GetNotebookURL():
    db = pymysql.connect(**dbinfo)
    cursor = db.cursor()
    sql = "select scripturl from notebook where medal<>'none' and isdownload=0"
    #sql = "select distinct scripturl from notebook_list where dataurl not like '/c/%' and dataname <> 'multiple data sources' and label='{}';".format(tag)
    cursor.execute(sql)
    r = cursor.fetchall()
    cursor.close()
    db.close()
    return r

def DownloadFromURL(url):
    # download the notebook from one url
    #print(url[1:])
    r = os.system("kaggle kernels pull "+url[1:])
    time.sleep(1)
    if(r==0):
        print("success "+url)
        db = pymysql.connect(**dbinfo)
        cursor = db.cursor()
        sql = "update notebook set isdownload=1 where scriptUrl='{}'".format(url);
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    else:
        print("fail "+url)
        db = pymysql.connect(**dbinfo)
        cursor = db.cursor()
        sql = "update notebook set isdownload=-1 where scriptUrl='{}'".format(url);
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

def main():
    save_dir = './notebook/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    os.chdir(save_dir)
    urls = GetNotebookURL()
    for url in urls:
        URL = url[0]
        #all_result.append(executor.submit(DownloadFromURL,(URL,tag)))
        DownloadFromURL(URL)
        time.sleep(random.randint(2,5))
        '''if signal == True:
            db = connect()
            cursor = db.cursor()
            sql = "update notebook_list set download=1 where scripturl='{}'".format(url[0]);
            cursor.execute(sql)
            db.commit()
            close(cursor,db)'''
    #print("start waiting ...")
    #wait(all_result, return_when=ALL_COMPLETED)
if __name__ == '__main__':
    main()
