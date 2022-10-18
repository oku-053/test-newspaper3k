from importlib.resources import contents
from os import link
from turtle import title
from newspaper import Article
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import csv

def getURL (targetSite):
    title_links = []
    for i in range(1, getWebPagination(targetSite + "1")+1):
        url = targetSite + str(i) 
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        contents = soup.find(class_ = "p-postList")
        get_a = contents.find_all("a")

        for i in range(len(get_a)):
            try:
                title_ = get_a[i].find(class_ = "p-postList__title").text
                link_ = get_a[i].get("href")
                date = getDate(link_)
                #titles.append(title_)
                title_links.append({'title':title_, 'link':link_, 'date':date})
            except:
                pass

        
    field_name = ['title','link','date']  
    with open('links.csv', 'w',encoding='utf-8',newline='')as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_name)
        writer.writeheader()
        writer.writerows(title_links)

    return title_links

def getDate(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(class_ = "c-postTimes__modified")
    date = content.get("datetime")

    return date

def getWebText(targetSite):
    resultLists = []
    for link in getURL(targetSite):
        url = link['link']
    
        article = Article(url,language='ja')

        article.download()

        article.parse()

        result = article.text

        if result:
            print("記事を取得しました"+"["+link['link']+"]")
            #texts.append(result)
            link['text'] = result
            resultLists.append(link)
        else:
            print("記事を取得できませんでした")
    
    #結果をファイルに書き込み
    field_name = ['title','link','date','text']  
    with open('result.csv', 'w',encoding='utf-8',newline='')as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_name)
        writer.writeheader()
        writer.writerows(resultLists)

def getWebPagination(url):
    r = requests.get(url)
    time.sleep(3)

    soup = BeautifulSoup(r.text, 'html.parser')
    pagination = soup.find(class_ = "c-pagination")
    lastNumStr = pagination.find(class_ = "page-numbers -to-last").text
    
    return int(lastNumStr)
    # title_links = []
    # titles = []
    # for i in range(len(get_a)):
    #     try:
    #         title_ = get_a[i].find(class_ = "p-postList__title").text
    #         link_ = get_a[i].get("href")
    #         #titles.append(title_)
    #         title_links.append({'title':title_, 'link':link_})
    #     except:
    #         pass



if __name__ == '__main__':

    url = "https://yosojicamp.com/category/campgaer/page/"

    getWebText(url)