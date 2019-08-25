#encoding；utf-8
import requests
import random
import time
from bs4 import BeautifulSoup
import lxml
import re
from selenium import webdriver
import csv
import json

def getlnglat(add):
    '''构造函数获取经纬度'''
    dz = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '这里放入自己的账号码'
    uri = dz + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    res = requests.get(uri).content  #将api返回的搜索经纬度坐标存放
    temp = json.loads(res)  #对json数据进行解析
    return temp     #解析字典的格式

def write_dzdp_bjhg(url):
    '''将数据写入csv'''
    driver=webdriver.Chrome()
    for i in range(1,51):
        driver.get('http://www.dianping.com/beijing/ch10/g110p'+str(i))
        soup=BeautifulSoup(driver.page_source,'lxml')
        #print(soup)
        infos=soup.find_all('div',class_='txt')
        for info in infos:
            title=info.h4.text
            #print(title)
            address_area=info.find_all('span',class_='tag')[1].text
            address=info.find('span',class_='addr').text
            #print(address)
            try:
                price=info.find('a',onclick="LXAnalytics('moduleClick', 'shopprice')").find('b')
                mean_price=price.text
            except:
                price=None
                print('辣鸡')
                mean_price=0
            try:
                num = info.find('div', class_='comment').find('b')
                rate_num=num.text
            except:
                rate_num=None
                print('辣鸡')
            #print(rate_num)
            #print(mean_price)
            kw=info.find('span',class_='comment-list').find_all('b')[0].text    #口味
            hj=info.find('span',class_='comment-list').find_all('b')[1].text    #环境
            fw=info.find('span',class_='comment-list').find_all('b')[2].text    #服务
            recommendations=info.find('div',class_='recommend').find_all('a')
            list_1=[]
            for s in range(0,len(recommendations)-1):
                recommendation=recommendations[s].text
                #print(recommendation)
                list_1.append(recommendation)
            recommendation_t=" ".join(list_1)
            try:
                lng = getlnglat(address)['result']['location']['lng']  # 采用构造的函数来获取经度
                lat = getlnglat(address)['result']['location']['lat']  # 获取纬度
            except:
                lng = 0
                lat = 0

            info_total=[title,address_area,address,rate_num,mean_price,kw,hj,fw,recommendation_t,lng,lat]
            # 打开文件，追加a
            out = open('大众点评_北京火锅.csv', 'a', newline='',encoding='gb18030')
            # 设定写入模式
            csv_write = csv.writer(out, dialect='excel')
            # 写入具体内容
            csv_write.writerow(info_total)
        time.sleep(random.randint(0,3))

write_dzdp_bjhg('http://www.dianping.com/beijing/ch10/g110p')   #运行主程序
