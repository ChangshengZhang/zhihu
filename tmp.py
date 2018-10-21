#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: tmp.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Oct 16 16:33:57 2018

#########################################################################

import os
import requests

url = 'https://www.zhihu.com/people/tong-mark-0217/activities'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

ip = '185.62.188.84:80'

data = requests.get(url,proxies = {'https':'https://{}'.format(ip)},headers = headers).text

print(data)

