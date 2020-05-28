# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from config import headers
from config import dbinfo
import pymysql
import random
import time
#global config
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 10
requests.keep_alive = False

def getdata(afterarg):
    h = random.randint(0, len(headers) - 1)
    try:
        data = requests.get('https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&after=' \
                        +str(afterarg)+'&language=Python&kernelType=Notebook',
                        headers = headers[h],timeout = (5, 15),verify = False)
    #    print('https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=20&after=' \
    #                    +str(afterarg)+'&language=Python&kernelType=Notebook')
        jsondata = data.json()
        conn = pymysql.connect(**dbinfo)
        cursor = conn.cursor()
        for js in jsondata:
            ID = js['id']
            bestPublicScore = js['bestPublicScore']
            if bestPublicScore == None:
                bestPublicScore = -1
            medal = js['medal']
            scriptUrl = js['scriptUrl']
            title = js['title']
            for i in title:
                if ord(i) >=256:
                    title = title.replace(i," ")
            totalComments = js['totalComments']
            totalForks = js['totalForks']
            totalScripts = js['totalScripts']
            totalViews = js['totalViews']
            totalVotes = js['totalVotes']
            totalLines = js['totalLines']
            isGpuEnabled = js['isGpuEnabled']
            isFork = js['isFork']
    #            print(ID, bestPublicScore, medal, scriptUrl, title, \
    #               totalComments, totalForks, totalScripts, totalViews, totalVotes, totalLines, \
    #               isGpuEnabled, isFork)
            searchsql = "SELECT * FROM notebook WHERE id='%s'" % ID
            cursor.execute(searchsql)
            ret = cursor.fetchmany(1)
            if ret!=():
                continue
            notebooksql = "INSERT INTO notebook(id, \
               bestPublicScore, medal, scriptUrl, title, \
               totalComments, totalForks, totalScripts, totalViews, totalVotes, totalLines, \
               isGpuEnabled, isFork) \
               VALUES (\"%s\", %s, \"%s\", \"%s\", \"%s\", %s, %s ,%s, %s, %s, %s, \"%s\", \"%s\")" % \
               (ID, bestPublicScore, medal, scriptUrl, title, \
               totalComments, totalForks, totalScripts, totalViews, totalVotes, totalLines, \
               isGpuEnabled, isFork)
            cursor.execute(notebooksql)
            for dataset in js['dataSources']:
                sourceId = dataset['sourceId']
                notebook_id = ID
                name = dataset['name']
                dataSourceUrl = dataset['dataSourceUrl']
                sourceType = dataset['sourceType']
                datasetsql = "INSERT INTO datasources(notebook_id,sourceId,name,dataSourceUrl,sourceType) \
                VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % \
                (notebook_id,sourceId,name,dataSourceUrl,sourceType)
                cursor.execute(datasetsql)
            for tag in js['categories']:
                notebook_id = ID
                tagid = tag['id']
                name = tag['name']
                fullpath = tag['fullPath']
                description = tag['description']
                tagsql = "INSERT INTO tags(notebook_id,tagid,name,fullpath,description) \
                VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % \
                (notebook_id,tagid,name,fullpath,description)
                cursor.execute(tagsql)
            print(scriptUrl + " download")
            conn.commit()
            time.sleep(random.randint(1,5))
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()

for i in range(100):
    getdata(i)
