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
    sql = "select scripturl from notebook"
    #sql = "select distinct scripturl from notebook_list where dataurl not like '/c/%' and dataname <> 'multiple data sources' and label='{}';".format(tag)
    cursor.execute(sql)
    r = cursor.fetchall()
    cursor.close()
    db.close()
    return r

def DownloadFromURL(url):
    # download the notebook from one url
    os.system("kaggle kernels pull "+url[1:])
    time.sleep(1)
    print("success download "+url)
    
def main():
    save_dir = './notebooks/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    os.chdir(save_dir)
    urls = GetNotebookURL()
    for url in urls:
        URL = url[0]
        #all_result.append(executor.submit(DownloadFromURL,(URL,tag)))
        DownloadFromURL(URL)
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
