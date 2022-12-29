# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import json
import random
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#-------------------------------------------------写入文件-------------------------------------------------
path = os.getcwd() + "/yqkx_data2022.csv"
csvfile = open(path, 'a', newline='', encoding = 'utf-8-sig')
writer = csv.writer(csvfile)
writer.writerow(('序号','文章标题','发布时间','文章链接','文章内容')) 

#--------------------------------------------疫情快讯-数据抓取---------------------------------------------
url = "http://society.people.com.cn/GB/369130/431577/431608/index.html"
# driver = webdriver.Chrome() #chromedriver.exe置于python37根目录
driver = webdriver.Chrome(r'C:\Users\Roy\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver.exe')

driver.implicitly_wait(5)
chrome_option = webdriver.ChromeOptions()
driver.get(url) #打开网页网页
driver.implicitly_wait(6) #等待加载六秒

#-------------------------------------------------获取标题-------------------------------------------------
titles = driver.find_elements(By.XPATH,value='//div[@class=" p2j_list_lt fl"]/ul/li') # 利用xpath定位
for t in titles:
    print(t.text)

links = driver.find_elements(By.XPATH,value='//div[@class=" p2j_list_lt fl"]/ul/li/a')
for link in links:
    print(link.get_attribute('href'))

print("\n\n==========================================================")

#-------------------------------------------------获取正文-------------------------------------------------
def get_content(url):
    print(url)
    time.sleep(random.randint(1000,3000)/1000.0)
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content,"html.parser")
        #来源
        ly = soup.find(attrs={"class":"fl"}).get_text()
        #print(ly)
        #正文
        zw = soup.find(attrs={"class":"box_con"})
        #防止某些文章仅图片
        if zw is not None:
            zw = zw.get_text()
            zw = zw.replace("\n", "")
        else:
            zw = ""
        print(zw)
        print("succeed")
        return ly,zw
    except Exception as e:
        zw = e.partial
        ly = ""
        print("except")
        print(zw)
    return ly, zw
    
#-------------------------------------------------写入文件-------------------------------------------------
k = 0
while k<len(titles):
    #序号
    num = str(k+1)
    #文章标题和发布时间
    value = titles[k].text.split('\n')
    con_title = value[0]
    con_time = value[1]
    #文件链接
    url = links[k].get_attribute('href')
    #获取来源和正文
    ly,zw = get_content(url)
    content = (num, con_title, con_time, url, zw)
    #文件写入操作
    writer.writerow((content))
    k = k + 1

#文件关闭
csvfile.close() 
