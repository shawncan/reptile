#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import os
import logging
import time
import datetime


def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print('爬取失败')


def getImageDownload(file_path, img_name, imageURL):
    """
    图片下载函数
    接收存放地址、文件名、图片链接
    通过设置headers（防止反爬虫）下载图片
    """
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/OtakuGirlPicture.txt',
                        filemode='a')

    logger = logging.getLogger()

    headers = {
        'Referer': 'https://wwww.nvshens.com/g/22377/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    address = file_path + '/' + img_name

    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        if not os.path.exists(address):
            r = requests.get(imageURL, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            with open(address, 'wb') as f:
                f.write(r.content)
                f.close()
        else:
            print("文件已存在")
    except Exception:
        logger.exception("Crawling Baidu {} stock data failed".format(img_name))



def getGoddessList(dict, GoddessURL):
    """
    排行榜提取函数
    接收字典、排行榜网页链接
    提取排行榜女神的名字，详情页短链接，添加进字典中
    """
    html = getHTMLText(GoddessURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', attrs={'target': '_blank'})
    for i in a:
        try:
            href = i.attrs['href']
            font = i.find('font')
            if font is not None:
                name = font.string
                dict[name] = href
            else:
                continue
        except:
            print('')


def getGalleryList(link_list, numbering):
    """
    全部写真提取函数
    接收写真链接列表、详情页短链接
    提取女神全部写真页面短链接，传递回getGalleryDetails()函数继续操作
    """
    set_url = 'https://www.nvshens.com' + numbering + '/album/'
    html = getHTMLText(set_url)
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.find_all(attrs={'class': 'igalleryli_link'})
    for i in li:
        link = i.attrs['href']
        link_list.append(link)
    return link_list


def getGalleryDetails(dict, GoddessURL):
    """
    详情页函数
    接收女神字典、网址
    提取详情页写真链接，传递getGalleryImage()函数操作
    """
    path = '/Users/wangjiacan/Desktop/shawn/爬取资料/宅男女神/'

    for (i, m) in dict.items():
        url = GoddessURL + m
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        file_path = path + i
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        try:
            li = soup.find('a', attrs={'title': '全部图片'}).text.split()[0]
            s = re.findall(r'\d{2}', li)
            if int(s[0]) > 6:
                link_list = []
                getGalleryList(link_list, m)
                for l in link_list:
                    Goddess_url = GoddessURL + l
                    getGalleryImage(file_path, i, Goddess_url)
                    time.sleep(60)
            else:
                gallery_link = soup.find_all(attrs={'class': 'igalleryli_link'})
                for l in gallery_link:
                    link = l.attrs['href']
                    Goddess_url = GoddessURL + link
                    getGalleryImage(file_path, i, Goddess_url)
                    time.sleep(60)
        except:
            print("错误")


def getGalleryImage(file_path, file_name, PortraitURL):
    """
    写真函数
    接收文件存储路径，写真链接
    提取写真页面每张图片链接，传递给ggetImageDownload()函数下载
    """
    count = 0
    try:
        html = getHTMLText(PortraitURL)
        soup = BeautifulSoup(html, 'html.parser')

        portrait_name = soup.find(attrs={'id': 'dinfo'}).text.split()[3]
        file_path = file_path + '/' + portrait_name

        page = soup.find(attrs={'id': 'pages'})
        single_page = page.find_all('a')[:-1]

        print("{}文件夹下载共{}页".format(file_name, len(single_page)))

        for img_page in single_page:
            src = img_page.attrs['href']
            url = 'https://www.nvshens.com' + src

            img_html = getHTMLText(url)
            img_soup = BeautifulSoup(img_html, 'html.parser')
            img_set = img_soup.find(attrs={'id': 'hgallery'})
            img = img_set.find_all('img')

            for link in img:
                img_link = link.attrs['src']
                img_name = re.findall(r'\d*.jpg', img_link)[0]
                getImageDownload(file_path, img_name, img_link)
                time.sleep(10)

            count = count + 1
            print("\r当前进度: {:.2f}%".format(count / len(single_page) * 5), end="")
            print('下载完成')
    except:
        print("图片链接爬取失败")



def main():
    goddess_list_url = 'https://www.nvshens.com/rank/sum/'
    goddess_detail_url = 'https://www.nvshens.com'
    gdict = {}
    gdict_1 = {'sugar小甜心CC(杨晨晨)': '/girl/22162/'}

    start = datetime.datetime.now()
    # getGoddessList(gdict, goddess_list_url)
    getGalleryDetails(gdict_1, goddess_detail_url)
    end = datetime.datetime.now()
    print(end - start)



if __name__ == "__main__":
    main()
