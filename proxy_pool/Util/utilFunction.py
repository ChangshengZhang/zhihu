# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
import os
import time
from lxml import etree

from Util.LogHandler import LogHandler
from Util.WebRequest import WebRequest

# logger = LogHandler(__name__, stream=False)


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
            # logger.info(u"sorry, 抓取出错。错误原因:")
            # logger.info(e)

    return decorate


# noinspection PyPep8Naming
def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


# noinspection PyPep8Naming
def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()

    # delay 2s for per request
    time.sleep(2)

    html = wr.get(url=url, header=header).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


# noinspection PyPep8Naming
def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"https": "https://{proxy}".format(proxy=proxy)}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    tg_url = 'https://www.baidu.com'
    lines = open(os.path.join(os.path.dirname(__file__),'./../Config.ini')).readlines()
    for line in lines:
        if 'tg_url' in line:
            tg_url = line.strip('\n').split(' ')[-1]
    try:
        # 超过20秒的代理就不要了
        r = requests.get(tg_url, proxies=proxies, headers = headers, timeout=10, verify=False)

        if '感谢' in r.text:
            return True

        #if r.status_code == 200:
            # logger.info('%s is ok' % proxy)
            #return True
    except Exception as e:
        # logger.error(str(e))
        return False
