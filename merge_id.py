#!/usr/bin/python
# File Name: merge_id.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# -*- coding: utf-8 -*-
# Created Time: 2018年10月22日 星期一 23时57分52秒
#########################################################################

import os

merged_id = []

print('load basic user')
for tmp_id in os.listdir('./data/basic_user'):

    merged_id.append(tmp_id.split('.')[0])

print('load following')
for tmp_id in os.listdir('./data/following'):

    merged_id.append(tmp_id.split('.')[0])

    for line in open("./data/following/"+tmp_id).readlines():

        id_ = line.split(',')[0]
        merged_id.append(id_)


print('load follower')
for tmp_id in os.listdir('./data/follower'):

    merged_id.append(tmp_id.split('.')[0])

    for line in open("./data/follower/"+tmp_id).readlines():

        id_ = line.split(',')[0]
        merged_id.append(id_)

print('begin set')
new_merged_id = list(set(merged_id))
print(len(new_merged_id), len(merged_id))

new_merged_id = ','.join(new_merged_id)

f = open('merged_id.csv','w')
f.writelines(new_merged_id)
f.close()

