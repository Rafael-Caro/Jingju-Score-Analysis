# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 21:37:51 2017

@author: Rafael.Ctt
"""

lyricsdata21 = './scores/lyricsdata.2.1.csv'

with open(lyricsdata21, 'r', encoding='utf-8') as f:
    data = f.readlines()

daeh = {}
daxp = {}
lseh = {}
lsxp = {}

for i in data:
    x = i.split(',')
    bs = x[3]
    if (x[1] == 'dan') and (x[2] == 'erhuang'):
        daeh[bs] = daeh.get(bs, 0) + 1
    if (x[1] == 'dan') and (x[2] == 'xipi'):
        daxp[bs] = daxp.get(bs, 0) + 1
    if (x[1] == 'laosheng') and (x[2] == 'erhuang'):
        lseh[bs] = lseh.get(bs, 0) + 1
    if (x[1] == 'laosheng') and (x[2] == 'xipi'):
        lsxp[bs] = lsxp.get(bs, 0) + 1
