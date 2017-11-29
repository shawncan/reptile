#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import openpyxl
import threading
import queue
import datetime
import time
import os
import json
import demjson


def getHTMLText(url):
    """
    下载目标网页源码
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    proxies = {
        "http": "http://106.14.241.155:80",
        "https": "http://106.14.241.155:80",
    }

    # try:
    r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
    r.raise_for_status()
    r.encoding = 'GBK'
    return r.text
    # except Exception:
    #     logger.exception("Download HTML Text failed")


def getContentExtraction():
    # page_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv445&productId=4183290&score=2&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
    # html = getHTMLText(page_url)
    # a = html[25:-2]

    # json_obj = demjson.encode(html)
    # return_josn = json.loads(a)
    # print(return_josn['comments'][0])
    a = {'userClientShow': '来自京东Android客户端', 'uselessVoteCount': 0, 'content': '智能？呵，毛线啊，连接难，说明书有像没有一样，想知道的没有说明，各种挑剔wifi，路由器要求多的很，网络ssid不能隐藏，不能设置静态ip，不能设置MAC过滤&hellip;&hellip;&hellip;否则无法连接，呵呵，智能到用户没有安全感了，虽然咱没有啥，是吧？照这设置，路由器的这些功能都可以去掉了，厂家何必还要加强路由器的安全呢？还好有一个直连模式，可特么插座自带热点没有密码，谁都可以连接，说明书也没有告诉怎么改密码！！这是目前用智能插座发现的缺点，还有待改进，其实也没什么，就怕哪天有谁在练技术，攻击路由器，或者练习远程技术，后果就呵呵了&hellip;新闻对此类问题也报道过，还不少，总之，虽然想的远了，没安全感&hellip;但是智能设备我发现真的不是很智能，有时候真心不好用，  再来说这个插座，因为没能连接成功，用的是直连，反应很快，其他功能都应该不错，使用时发热，做工挺精致的  好了就这些，我得找其他路由器试着连接看能不能远程，希望能好好改进吧，让&ldquo;智能&rdquo;家居真的变智能', 'imageCount': 1, 'secondCategory': 12345, 'orderId': 0, 'id': 10697564830, 'firstCategory': 652, 'afterDays': 2, 'viewCount': 0, 'userImage': 'misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg', 'discussionId': 245716800, 'userLevelName': 'PLUS会员', 'recommend': True, 'userProvince': '', 'guid': '61e5481a-81fa-4ced-9f08-99ade76efd62', 'replies': [{'isMobile': False, 'updateTime': '2017-08-14 12:23:26', 'creationTimeString': '2017-08-14 12:23:26', 'content': '您好，感谢您对小K的支持，如遇到使用问题可以拨打小K售后电话4008713766，或者可以加入小K交流群465868047，我们将竭诚为您服务!', 'guid': '2c27e5fc-b5d1-4c6d-8c03-6fe15b202954', 'venderShopInfo': {'appName': '//kongke.jd.com', 'venderId': 1000001912, 'id': 1000001912, 'logoUri': '', 'title': '控客京东自营旗舰店'}, 'pin': '控客137*****442', 'id': 187972857, 'userClient': 103, 'nickname': '控客137*****442', 'userLevelId': '50', 'commentId': '10697564830', 'creationTime': '2017-08-14 12:23:26', 'userImage': 'misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg', 'parentId': '-1', 'userClientShow': '', 'userProvince': '', 'userLevelName': '注册会员', 'plusAvailable': 0, 'userExpValue': 328, 'isDelete': False}], 'replyCount': 2, 'anonymousFlag': 0, 'nickname': '-游梦-', 'integral': -10, 'referenceTypeId': 0, 'referenceId': '1518586', 'userExpValue': 10561, 'productSales': [], 'referenceName': '控客 1080P高清智能云台摄像头 360远程全景监控防盗看护管家 智能家居 红外夜视语音对讲家用无线网络WIFI摄像机 ', 'afterUserComment': {'clientType': 4, 'created': '2017-08-14 18:30:29', 'productId': 1518586, 'pin': 'jd_4950f7cd79ef7', 'orderId': 60066264259, 'id': 17520332, 'ip': '121.31.250.138', 'commentId': 10697564830, 'status': 1, 'dealt': 0, 'modified': '2017-08-14 18:30:29', 'forceRead2Writer': False, 'hAfterUserComment': {'rowKey': '8617520332', 'id': 17520332, 'discussionId': 245971521, 'content': '产品本身很好，直连模式反应很迅速，在手机里操作比按压插座的按键还要快，赞一个  其次，不满意的就是，直连模式插座本身的wifi没办法加密，再者，太依赖网络，只要断网，也就和平常的定时插座稍微方便一点，连接本地局域网不联网的情况下无法进行操作，只能用直连模式控制，充电保护功能手机关机或者开启飞行模式或者wifi断网，都没有效果，需要网络连接服务器在发送指令给小k，所以，没有网络，就只是一个比普通定时插座方便一点的产品而已，希望以后能更加全面，不连网的情况下也能在家轻松的控制多个设备，希望更加人性化   变成真正的智能产品'}, 'anonymous': 0, 'tableNames': {}}, 'referenceImage': 'jfs/t3865/250/1177364832/60906/4eacd9ea/586e2358Na3dbb446.jpg', 'referenceType': 'Product', 'userImgFlag': 0, 'creationTime': '2017-08-13 23:38:52', 'thirdCategory': 12353, 'isTop': False, 'days': 1, 'score': 3, 'userImageUrl': 'misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg', 'isMobile': True, 'userLevelColor': '#e1a10a', 'usefulVoteCount': 0, 'plusAvailable': 201, 'userLevelId': '61', 'title': '', 'showOrderComment': {'isDeal': 1, 'userClientShow': '来自京东Android客户端', 'uselessVoteCount': 0, 'content': "智能？呵，毛线啊，连接难，说明书有像没有一样，想知道的没有说明，各种挑剔wifi，路由器要求多的很，网络ssid不能隐藏，不能设置静态ip，不能设置MAC过滤&amp;hellip;&amp;hellip;&amp;hellip;否则无法连接，呵呵，智能到用户没有安全感了，虽然咱没有啥，是吧？照这设置，路由器的这些功能都可以去掉了，厂家何必还要加强路由器的安全呢？还好有一个直连模式，可特么插座自带热点没有密码，谁都可以连接，说明书也没有告诉怎么改密码！！这是目前用智能插座发现的缺点，还有待改进，其实也没什么，就怕哪天有谁在练技术，攻击路由器，或者练习远程技术，后果就呵呵了&amp;hellip;新闻对此类问题也报道过，还不少，总之，虽然想的远了，没安全感&amp;hellip;但是智能设备我发现真的不是很智能，有时候真心不好用，  再来说这个插座，因为没能连接成功，用的是直连，反应很快，其他功能都应该不错，使用时发热，做工挺精致的  好了就这些，我得找其他路由器试着连接看能不能远程，希望能好好改进吧，让&amp;ldquo;智能&amp;rdquo;家居真的变智能<div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t7072/297/1937490923/55196/c79aa0b4/5990728cN05e0b68a.jpg' /></div>", 'secondCategory': 0, 'referenceType': 'Order', 'integral': -10, 'orderId': 0, 'id': 245716800, 'firstCategory': 0, 'userImgFlag': 0, 'creationTime': '2017-08-13 23:38:52', 'thirdCategory': 0, 'isTop': False, 'recommend': False, 'score': 0, 'isMobile': True, 'userLevelColor': '#666666', 'usefulVoteCount': 0, 'viewCount': 0, 'userProvince': '', 'guid': '064bdfe1-c524-4f3d-a398-a98c608833f0', 'replyCount': 0, 'anonymousFlag': 0, 'status': 1, 'userClient': 4, 'referenceTypeId': 0, 'referenceId': '1518586', 'isReplyGrade': False}, 'mergeOrderStatus': 2, 'images': [{'jShow': 0, 'imgUrl': '//img30.360buyimg.com/n0/s128x96_jfs/t7072/297/1937490923/55196/c79aa0b4/5990728cN05e0b68a.jpg', 'dealt': 0, 'isMain': 0, 'associateId': 245716800, 'productId': 0, 'pin': '', 'id': 387616922, 'available': 1, 'imgTitle': ''}], 'userClient': 4, 'status': 1, 'productColor': 'WI-FI定时插座', 'referenceTime': '2017-08-12 15:04:17', 'isReplyGrade': False, 'productSize': ''}

    # 商品名称
    referenceName = a["referenceName"]
    # 用户名
    nickname = a["nickname"]
    # 会员等级
    userLevelName = a["userLevelName"]

    # 第一次评价内容
    content = a["content"]
    # x = re.sub(r"(&hellip;|&ldquo;|&rdquo;)", "...", content)
    x = re.findall(r"&[a-z]*;", content)
    for i in set(x):
        if i == "&hellip;":
            symbol = "..."
        elif i == "&ldquo;":
            symbol = "'"
        elif i == "&rdquo;":
            symbol = "'"
        else:
            symbol = " "
        c = re.sub(i, symbol, content)
        content = c

    print(content)

    # x = unicode(content, "gbk")

    showOrderComment = ''
    afterUserComment = ''
    images = ''
    # print(content)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/kk_jd_comment.txt',
                        filemode='a')

    logger = logging.getLogger()

    getContentExtraction()