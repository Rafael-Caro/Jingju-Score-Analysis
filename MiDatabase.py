# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:47:55 2017

@author: Rafael.Ctt
"""

import numpy as np
import os

path = 'C:/Users/Rafael.Ctt/Desktop/Annatations/annatations/'

allfiles = os.listdir(path)
ann = []
for f in allfiles:
    if f[-3:] == 'csv':
        ann.append(f)

mi = 60
mif = ''
mii = 0
ma = 0
maf = ''
mai = 0

total = []
singles = []

for file in ann:
    temp = np.array([])
    with open(path+file, 'r') as x:
        data = x.readlines()
    prev = float(data[0].strip())
    for i in range(1, len(data)):
        val = float(data[i].strip())
        dif = val - prev
        total.append(dif)
        temp = np.append(temp, dif)
        if dif < mi:
            mi = dif
            mif = file
            mii = i
        if dif > ma:
            ma = dif
            maf = file
            mai = i
        prev = val
    m = np.mean(temp)
    sd = np.std(temp)
    singles.append([file, m, sd])

t = np.array(total)
tm = np.mean(t)
tsd = np.std(t)

txt = ''
for i in singles:
    txt += i[0]+'\t'+str(round(i[1], 2))+'\t'+str(round(i[2], 2))+'\n'
    
with open('mi.txt', 'w') as f:
    f.write(txt)
    
seven = []
with open(path+ann[21], 'r') as f:
    data = f.readlines()
    print(len(data))
prev = float(data[0].strip())
for i in range(1, len(data)):
    val = float(data[i].strip())
    dif = val - prev
    seven.append(dif)
    prev = val
print(len(seven))

    