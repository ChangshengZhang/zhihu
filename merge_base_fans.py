#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: merge.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Oct 16 02:32:39 2018

#########################################################################

import os

def merge(fp, fans_min = 0, fans_max = 99999999):

    count = 0
    flag = 0

    fans_index = 1
    for fn in os.listdir(fp):

        line = open(fp+fn).readlines()
        header = line[0]
        if len(line) <2:
            continue
        line_list = line[1].strip('\n').split(',')
        if int(line_list[fans_index]) >= fans_min and int(line_list[fans_index]) <= fans_max:

            # write header
            if flag == 0:
                f = open('merged_base_fans.csv','w')
                f.write('id,'+header)
                f.close()
                flag = 1

            f = open('merged_base_fans.csv','a')
            f.write(fn.split('.')[0]+','+line[1])
            f.close()
            count += 1

    print(count)



if __name__ == "__main__":

    fp = './data/basic_user/'
    merge(fp,10000)
