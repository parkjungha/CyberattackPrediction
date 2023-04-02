from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import re

date_30 = [4, 6, 9, 11]
date_28 = [2]
date_31 = [1, 3, 5, 7, 8, 10, 12]

def datetime(y,m1,m2):  # 2017,9,12 하면 2017년 9월에서 12월까지의 일별 url
    url_result=dict() #결과

    for i in range(m1,m2+1):
        month=i
        if i in date_31:
            for j in range(1,32):
                day=j
                month_day=str(y)+"-"+str(i)+"-"+str(j)
                date = [str(y),str(i),str(j)]
                duration = '%2Ccd_min%3A{0}%2F{1}%2F{2}%2Ccd_max%3A{3}%2F{4}%2F{5}'.format(date[1], date[2], date[0], date[1], date[2], date[0])
                base_url = 'https://www.google.com/search?q=hit+by+cyber+attack&biw=1536&bih=722&source=lnt&tbs=cdr%3A1'+ duration + '&tbm=nws'
                url_result[month_day]=base_url
                
        elif i in date_28:
            for j in range(1,29):
                day=j
                month_day=str(y)+"-"+str(i)+"-"+str(j)
                date = [str(y),str(i),str(j)]
                duration = '%2Ccd_min%3A{0}%2F{1}%2F{2}%2Ccd_max%3A{3}%2F{4}%2F{5}'.format(date[1], date[2], date[0], date[1], date[2], date[0])
                base_url = 'https://www.google.com/search?q=hit+by+cyber+attack&biw=1536&bih=722&source=lnt&tbs=cdr%3A1'+ duration + '&tbm=nws' 
                url_result[month_day]=base_url
        else:
            for j in range(1,31):
                day=j
                month_day=str(y)+"-"+str(i)+"-"+str(j)
                date = [str(y),str(i),str(j)]
                duration = '%2Ccd_min%3A{0}%2F{1}%2F{2}%2Ccd_max%3A{3}%2F{4}%2F{5}'.format(date[1], date[2], date[0], date[1], date[2], date[0])
                base_url = 'https://www.google.com/search?q=hit+by+cyber+attack&biw=1536&bih=722&source=lnt&tbs=cdr%3A1'+ duration + '&tbm=nws'
                url_result[month_day]=base_url
    return url_result

d1= datetime(2017,1,12)
d2= datetime(2018,1,12)
d3= datetime(2019,1,12)
d1.update(d2)
d1.update(d3) 
DATE= [a for a in d1.keys()]
url_list=[a for a in d1.values()]

def get_company_url(a):
    driver.get(a)
    # driver를 이용하여 가져오기
    contents_url = driver.find_elements_by_css_selector("a.l.lLrAF")
    contents_comp = driver.find_elements_by_css_selector('div.gG0TJc')


    # 각 url과 뉴스사를 리스트로 만들기
    list_company = []
    for i in contents_comp:
        a = i.find_elements_by_css_selector('span.xQ82C.e8fRJf')
        for j in a:
            list_company.append(j.text)
        
    list_url = []
    for i in contents_url:
        list_url.append(i.get_attribute('href'))
    
    list_title = []
    for i in contents_url:
        list_title.append(i.text)

    # dataframe으로 만들기
    list_merge = [list_company, list_title, list_url]
    col_names = ['company', 'title', 'url']
    df_ = pd.DataFrame(list_merge)
    df = df_.T
    df.columns = col_names
    
    return df
    # company filtering 함수로 보내기
    # filter_company(df)
    date_column(df)

def date_column(c):
    date_list = []
    for i in range(len(c.index)):
        date_list.append(DATE)
    c.insert(0, 'date', date_list)
    return c

if __name__ == '__main__':
    # 페이지 넘기며 신문사, 뉴스, 날짜 수집
    driver = webdriver.Chrome(r"C:/Users/jungh/Downloads/chromedriver.exe")
    driver.set_page_load_timeout("10")
    
    
    FINAL=[]
    for DATE, URL in zip(DATE[:], url_list[:]): 
        
        time.sleep(1)
        driver.get(URL) # 페이지 입장
        time.sleep(3)
        
        print("웹페이지 인덱스" , url_list.index(URL), "/",len(url_list) )
        r1 = get_company_url(URL)
        r2 = date_column(r1)
        FINAL.append(r2)
    
        for count in range(999):
            if count==0:
                try:
                    soup = BeautifulSoup(driver.page_source)
                    h1= soup.find_all("a", class_="pn")
                    h2='http://www.google.com'+h1[0]['href'] # 다음버튼 url
                    driver.get(h2)
                    time.sleep(3)
                except Exception as ex:
                    print('더이상 "페이지" 없음', ex)
                    break
            else:
                try:
                    soup = BeautifulSoup(driver.page_source)
                    h1= soup.find_all("a", class_="pn")
                    h2='http://www.google.com'+h1[1]['href'] # 다음버튼 url
                    driver.get(h2)
                    time.sleep(3)
                except Exception as ex:
                    print('더이상 "페이지" 없음', ex)
                    break
        
    driver.close()    
    
    
    result = pd.concat(FINAL)
    print(result)