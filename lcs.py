#-*- coding:utf-8 -*-
#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import re
import math
import pandas
from time import sleep

#首頁
sess=requests.Session()
url="https://gis.land.ntpc.gov.tw/lcs/default/01.aspx"
res=sess.get(url,verify=False)
soup=BeautifulSoup(res.content,'html.parser')
# print soup
__VIEWSTATE=soup.find('input',attrs={'name':'__VIEWSTATE'})['value']
__VIEWSTATEGENERATOR= soup.find('input',attrs={'name':'__VIEWSTATEGENERATOR'})['value']
__EVENTVALIDATION=soup.find('input',attrs={'name':'__EVENTVALIDATION'})['value']

url="https://gis.land.ntpc.gov.tw/lcs/default/0101.aspx?id=80"

def page_info(url):
    #進到各分頁找筆數準備撈
    res=sess.get(url,verify=False)
    soup=BeautifulSoup(res.content,'html.parser')
    __VIEWSTATE=soup.find('input',attrs={'name':'__VIEWSTATE'})['value']
    __VIEWSTATEGENERATOR= soup.find('input',attrs={'name':'__VIEWSTATEGENERATOR'})['value']
    __EVENTVALIDATION=soup.find('input',attrs={'name':'__EVENTVALIDATION'})['value']
    temp=soup.find('div',attrs={'alert alert-success'}).text
    m=re.search(u'全部共有 (.*?) 標',temp)
    page=int(math.ceil(int(m.group(1))/10.0))

    print page

    for i in range(8,page):
        if i<10:
            count='0'+str(i)
        elif count==10:
            count=str(i)
        elif i>=11:
            count=str(i-3)
            
            print count
            if int(count)<10:
                count='0'+str(count)
        a="DataGrid1$ctl01$ctl{}".format(count)
        headers={
                 "Host": "gis.land.ntpc.gov.tw",
                 "Referer": "https://gis.land.ntpc.gov.tw/lcs/default/01.aspx",
                 "Upgrade-Insecure-Requests": "1",
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36",
                 }
        form={
              "__EVENTTARGET": a,
              "__EVENTARGUMENT":"",
              "__LASTFOCUS":"",
              "__VIEWSTATE":__VIEWSTATE,
              "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
              "__VIEWSTATEENCRYPTED":"",
              "__EVENTVALIDATION":__EVENTVALIDATION,
              "filtertype": "RadioButton1",
              "ddlma_sal_no":"", 
               
              }


        url="https://gis.land.ntpc.gov.tw/lcs/default/0101.aspx?id=80"
        res=sess.post(url,data=form,headers=headers,verify=False)
        soup=BeautifulSoup(res.content,'html.parser')
        __VIEWSTATE=soup.find('input',attrs={'name':'__VIEWSTATE'})['value']
        __VIEWSTATEGENERATOR= soup.find('input',attrs={'name':'__VIEWSTATEGENERATOR'})['value']
        __EVENTVALIDATION=soup.find('input',attrs={'name':'__EVENTVALIDATION'})['value']

        pd=pandas.read_html(res.content)
        pd=pd[1]
        pd=pd.drop([0,1])

#         for id,town,Segment,land_num in zip(pd[0],pd[1],pd[2],pd[3]):
#             print id,town,Segment,land_num
#         
        sleep(3)

page_info(url)
