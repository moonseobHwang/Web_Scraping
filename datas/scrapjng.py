from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

res = requests.get('http://media.daum.net/economic/')
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    links = soup.find_all('a', class_='link_txt')
    print('task_crawling_daum : ', type(links), len(links))
    dates = list()
    title = str()
    link = str()
    for link in links:
        title = str.strip(link.get_text())
        link = link.get('href')
        data = {"title": title, "link": link, "create_date": datetime.datetime.now()}
        dates.append(data)

    with MongoClient('mongodb://172.17.0.1:27017/')  as client:
        mydb = client.mydb
        res = mydb.economic.insert_many(dates)