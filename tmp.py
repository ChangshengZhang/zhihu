#!/usr/bin/python
# File Name: tmp.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# -*- coding: utf-8 -*-
# Created Time: 2018年10月27日 星期六 17时53分28秒
#########################################################################

import os

id_list = open('./merged_id.csv').readline().split(',')

for ii in range(len(id_list)):

    f = open('./id/'+str(int(ii/1000)),'a')
    f.write(id_list[ii])
    if (ii+1)%1000 !=0:
        f.write(',')
    f.close()
