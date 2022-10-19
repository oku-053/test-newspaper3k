from importlib.resources import contents
from os import link
from turtle import title
from webbrowser import get
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
        #url = targetSite + str(i) 
        url = targetSite
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        #contents = soup.find(class_ = "p-postList")
        contents = soup.find(class_ = "archive-entries")
        get_a = contents.find_all("h1")
        print(get_a[0])

        for i in range(len(get_a)):
            try:
                #title_ = get_a[i].find(class_ = "p-postList__title").text
                link_ = get_a[i].find(class_ = "entry-title-link").get("href")
                title_ = get_a[i].find(class_ = "entry-title-link").text
                
                date = getDate(link_)
                #titles.append(title_)
                title_links.append({'title':title_, 'link':link_, 'date':date})
            except:
                print("サイト情報の取得に失敗しました")
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
    #content = soup.find(class_ = "c-postTimes__modified")
    content = soup.find(class_ = "date entry-date first").find("time")
    date = content.get("datetime")

    return date

def getWebTextsForMultiPage(targetSite):
    resultLists = []
    for link in getURL(targetSite):
        url = link['link']
    
        article = Article(url,language='ja')
        try:
            article.download()
            article.parse()
            result = article.text
        except:
            print('***FAILED TO DOWNLOAD***', article.url)
            continue
        
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

def getWebText(targetSite):
    article = Article(targetSite,language='ja')
    try:
        article.download()
        article.parse()
        result = article.text
    except:
        print('***FAILED TO DOWNLOAD***', article.url)
        
    if result:
        print("記事を取得しました")
        #結果をファイルに書き込み
        with open('result.txt', 'w',encoding='utf-8',newline='')as f:
            f.write(result)
    else:
        print("記事を取得できませんでした")
    


def getWebPagination(url):
    r = requests.get(url)
    time.sleep(3)

    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        pagination = soup.find(class_ = "c-pagination")
        lastNumStr = pagination.find(class_ = "page-numbers -to-last").text
        return int(lastNumStr)
    except:
        return 2
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

    url = "https://www.takchaso.com/archive/category/%E5%86%99%E7%9C%9F%E3%83%BB%E3%82%AB%E3%83%A1%E3%83%A9-%E5%86%99%E3%83%AB%E3%83%B3%E3%81%A7%E3%81%99"

    getWebTextsForMultiPage(url)