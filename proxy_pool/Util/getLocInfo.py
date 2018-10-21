#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: get_proxy_loc.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Fri Oct 12 11:06:02 2018

#########################################################################

import os
import requests
from bs4 import BeautifulSoup 

class GetProxyLocInfo():

    proxy = ''
    header_fp = './lib/profile/header/geoipview'
    header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Connection':'keep-alive',
            'Cookie':'_ga=GA1.2.427400570.1539308565; _gid=GA1.2.1182895956.1539308565; _gat_gtag_UA_123650444_1=1',
            'Host':'cn.geoipview.com',
            'Referer':'https://cn.geoipview.com/?q=120.50.27.182&x=0&y=0',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }

    def __init__(self,proxy):
        self.proxy = proxy

    def get_proxy_loc_info(self):

        proxy = self.proxy
        proxy_loc_info = []
        url = 'https://cn.geoipview.com/?q={}&x=9&y=20'.format(proxy.split(':')[0])

        res = requests.get(url,headers = self.header, proxies = {'https':'https://{}'.format(proxy)}, timeout = 5).text
        soup = BeautifulSoup(res,'html.parser')
        tmp_proxy_loc_info = soup.findAll('td',class_='show2')
        your_ip = soup.findAll('div',id ='yourip')[0].get_text().split(':')[1].strip(' ')

        # 0:nation, 1:city
        proxy_loc_info.append(tmp_proxy_loc_info[0].get_text())
        proxy_loc_info.append(tmp_proxy_loc_info[1].get_text())
    
        return proxy_loc_info


if __name__ == "__main__":

    proxy = '120.55.49.41:8080'
    a = GetProxyLocInfo(proxy)
    print(a.get_proxy_loc_info())
