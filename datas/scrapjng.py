from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests, time, bs4, sqlite3, schedule

url = "https://job.incruit.com/entry/searchjob.asp?schol=50&occ1=120&occ1=150"
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
db_url='mongodb://13.125.191.54:53368'
MongoClient(db_url)['workbs4'].sampleCollection.drop()

res = requests.get(url)
soup = BeautifulSoup(res.text, "html5lib")
def jobprocess():
    for j in range(1, 2):
        now = time.gmtime(time.time())
        print(now.tm_hour,"시", now.tm_min, "분", now.tm_sec,"초")
        with MongoClient(db_url) as client:
            workbs4 = client['workbs4']
            MongoClient(db_url)['workbs4'].sampleCollection.drop()
            for i in range(1, 30):
                #incruit_contents > div.section_layout > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr:nth-child(2)
                title_data=soup.tbody
                datas = title_data.select(f"tr:nth-child({i})")
                for data in datas: # i를 key가앖으로 받아주고 그가앖을 토대로 데이터를 선별해준다
                    try:
                        #제목
                        name_data = data.select_one("td:nth-child(2) > div > span.accent > a")
                        name_data = str.strip(name_data.get_text())
                        #지원자격
                        major_data = data.select_one("td:nth-child(3) > div > p > em")
                        major_data = str.strip(major_data.get_text())
                        #근무조건
                        Condi_data = data.select_one("td:nth-child(4) > div > p > em")
                        Condi_data = str.strip(Condi_data.get_text())
                        #마가암일
                        date_data1 = data.select_one("td.lasts > div.ddays > p:nth-child(2)")
                        date_data1 = str.strip(date_data1.get_text())
                        date_data2 = data.select_one("td.lasts > div.mdays > p > span")
                        date_data2 = str.strip(date_data2.get_text())
                        date_data = date_data1 + date_data2
                        #회사명
                        id_data = data.select_one("th > div > div.check_list_r > span > a")
                        id_data = str.strip(id_data.get_text())

                        data={'id_data':id_data, 'name_data':name_data, 'Condi_data':Condi_data, 'major_data':major_data, 'date_data':date_data}
                        infor = workbs4.sampleCollection.insert_one(data)
                    except:
                        pass
            
                    print(name_data,major_data,id_data,Condi_data,date_data)
                time.sleep(0.5)
schedule.every(180).minutes.do(jobprocess)

while True:
    schedule.run_pending()
    time.sleep(1)