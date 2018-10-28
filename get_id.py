#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: get_id.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Mon Oct 15 20:45:31 2018

#########################################################################

import os
import requests
import datetime
from bs4 import BeautifulSoup
import time
import re
import random
import sys
import asyncio
import concurrent.futures as cf
import json
from multiprocessing import Process


def _write_list_to_file(data,fp,mode = 'w',new_line_flag = 1):

    f = open(fp,mode)
    op_line = ''
    for item in data:
        op_line = op_line + str(item) + ','
    op_line = op_line.strip(',')
    if new_line_flag:
        op_line = op_line+'\n'
    f.write(op_line)
    f.close()

def _get_num_from_str(data):

    return re.findall(r'(\d+(,\s*\d+)*)',data)

def _get_valid_proxy():

    valid_flag = False
    try_count = 0
    while (not valid_flag) and try_count < 3:
        proxy = requests.get('http://127.0.0.1:5010/get/').json()['proxy']
        valid_flag = requests.get('http://127.0.0.1:5010/validate_proxy/?proxy={}'.format(proxy)).json()['result']
        try_count += 1

    return proxy

def _get_html(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    try:
        proxy = _get_valid_proxy()
        print(proxy,url)
        data = requests.get(url,proxies = {'https':'https://{}'.format(proxy)},headers = headers, timeout = 10).text
        return data
    except:
        proxy = _get_valid_proxy()
        data = requests.get(url,proxies = {'https':'https://{}'.format(proxy)},headers = headers, timeout = 10).text
        return data

# get:
#   关注了,关注者,赞同，感谢
#   关注了和关注者的 url_token

class GetZhihuUser():

    url_token = ''
    agree_num = 0
    thanks_num = 0
    collect_num = 0
    public_edit_num = 0

    following_num = 0
    follower_num = 0

    last_update = ''
    user_name = ''

    def __init__(self,url_token):
        
        self.url_token = url_token
        try:
            user_info_flag = self.get_user_info()
        except:
            user_info_flag = 0
        if user_info_flag:
            try:
                flag = self.get_follow_info()
            except:
                pass
        
    def get_user_info(self):

        user_url = 'https://www.zhihu.com/people/{}/activities'.format(self.url_token)
        main_pg = _get_html(user_url)
        soup = BeautifulSoup(main_pg,'html5lib')

        self.user_name = str(soup.findAll('span', class_ = 'ProfileHeader-name')[0].get_text())
        
        user_profile = str(soup.findAll('div',class_ = 'Profile-sideColumnItems')[0])

        for item in user_profile.split('/'):
            if '赞同' in item:
                self.agree_num = _get_num_from_str(item)[0][0].replace(',','')
            if '感谢' in item:
                self.thanks_num = _get_num_from_str(item)[0][0].replace(',','')
                self.collect_num = _get_num_from_str(item)[1][0].replace(',','')
            if '公共编辑' in item:
                self.public_edit_num = _get_num_from_str(item)[0][0].replace(',','')

        follow = soup.findAll('strong',class_ = 'NumberBoard-itemValue')
        if len(follow) == 0:
            return 0

        self.following_num = str(follow[0].get_text()).replace(',','')
        self.follower_num = str(follow[1].get_text()).replace(',','')

        activity_info = str(soup.findAll('div', class_ = 'ActivityItem-meta')[0].get_text())
        self.last_update = activity_info
        print('get user info.',self.follower_num, ' ',self.following_num)
    
        user_url = 'https://www.zhihu.com/people/{}/activities'.format(self.url_token)
    
        _write_list_to_file(['user_name','follower_num','last_update','agree_num','thanks_num','collect_num','public_edit_num','following_num','url'],'./data/basic_user/{}.csv'.format(self.url_token),mode = 'w')
        _write_list_to_file([self.user_name,self.follower_num,self.last_update,self.agree_num,self.thanks_num,self.collect_num,self.public_edit_num,self.following_num,user_url],'./data/basic_user/{}.csv'.format(self.url_token),mode = 'a')
        print('user info wrote.')
        return 1

    def get_follow_url_token(self,url,ii,op):

        ii = int(ii)
        html = _get_html(url+str(ii))

        soup = BeautifulSoup(html,'html5lib')
        follower_info = str(soup.findAll('div',style = 'display:none')[0])

        follower_url_token = []
        follower_count = []

        op_lines = []

        for tmp in follower_info.split(','):

            if 'urlToken' in tmp and not ('loading' in tmp) and not(self.url_token in tmp):
                tmp_token = tmp.split(':',1)[1].strip('"')
                if 'quot' in tmp_token:
                    follower_url_token.append(tmp_token.split(';')[1].split('&')[0])
                else:
                    follower_url_token.append(tmp_token)
        
            if 'followerCount' in tmp:
                follower_count.append(_get_num_from_str(tmp)[0][0])

        if self.follower_num == follower_count[-1]:
            for jj in range(len(follower_url_token)):
                op_lines.append(follower_url_token[jj]+','+follower_count[jj]+'\n')
        else:
            for jj in range(len(follower_url_token)):
                op_lines.append(follower_url_token[jj]+','+follower_count[jj+1]+'\n')

        f = open(op+'/'+str(ii)+'.csv', 'w')
        f.writelines(op_lines)
        f.close()
            
    def get_follow_info(self):

        print('get following info')
        url_following = 'https://www.zhihu.com/people/{}/following?page='.format(self.url_token)
        following_pg_max_num = int((int(self.following_num) - 1)/20 + 1)
        following_op = './data/following/{}'.format(self.url_token)

        if os.path.exists(following_op):
            existed_file = os.listdir('./data/following/'+self.url_token)
            if len(existed_file) == following_pg_max_num:
                print('{} already exists.'.format(self.url_token))
                return 0
        else:
            os.system('mkdir '+following_op)

        #if following_pg_max_num < 5:
        for ii in range(1, following_pg_max_num+1):
            print('get {}/{}th following info.'.format(ii,following_pg_max_num))
            self.get_follow_url_token(url_following,ii,following_op)

        return 0
        #else:
        #    loop = asyncio.get_event_loop()
        #    loop.run_until_complete(self.run_thread(url_following, following_op, following_pg_max_num))
        #    loop.close()


        #print('get follower info')
        #url_follower = 'https://www.zhihu.com/people/{}/followers?page='.format(self.url_token)
        #follower_pg_max_num = int((int(self.follower_num) -1)/20 + 1)
        #follower_op = './data/follower/{}'.format(self.url_token)

        #if follower_pg_max_num < 5:
        #    for ii in range(1, follower_pg_max_num+1):
        #        print('get {}/{}th follower info.'.format(ii,follower_pg_max_num))
        #        self.get_follow_url_token(url_follower,ii,follower_op)
        #else:
        #    loop = asyncio.get_event_loop()
        #    loop.run_until_complete(self.run_thread(url_follower, follower_op, follower_pg_max_num))
        #    loop.close()

async def run_thread():

    fn_list = open('./merged_id.csv').readlines()[0].split(',')

    with cf.ThreadPoolExecutor(max_workers = 3) as executor:
        loop = asyncio.get_event_loop()
        futures = (loop.run_in_executor(executor, get_follow_, fn) for fn in fn_list)
        for result in await asyncio.gather(*futures):
            pass

# get follow list
def get_follow_(fn):

    try:
        a = GetZhihuUser(fn)
    except:
        print(fn+' has some error.')

if __name__ =="__main__":

    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(run_thread())
    #loop.close()

    #fn_list = open('./merged_id.csv').readlines()[0].split(',')
    kk = sys.argv[1]
    fn_list = open('./id/{}'.format(kk)).readline().split(',')

    for ii in range(len(fn_list)):
        print('get {}:{}/{}th following info.'.format(kk,ii,len(fn_list)))
    #for fn in fn_list:
        get_follow_(fn_list[ii])

