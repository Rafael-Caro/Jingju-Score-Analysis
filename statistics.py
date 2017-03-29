# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 21:37:51 2017

@author: Rafael.Ctt
"""

lyricsdata = './scores/lyricsdata.4.0.csv'
corpusfile = './scores/corpus.csv'

with open(lyricsdata, 'r', encoding='utf-8') as f:
    data = f.readlines()

with open(corpusfile, 'r', encoding='utf-8') as f:
    corpus = f.readlines()

daeh = {}
daxp = {}
lseh = {}
lsxp = {}
others = {}

for line in data:
    strInfo = line.strip().split(',')
    hd = strInfo[1]
    sq = strInfo[2]
    bs = strInfo[3]
    ju = strInfo[4]
    if (hd=='dan') and (sq=='erhuang') and (ju in ['s','s1','s2','x']):
        daeh[bs] = daeh.get(bs, 0) + 1
        
    elif (hd=='dan') and (sq=='xipi') and (ju in ['s','x']):
        daxp[bs] = daxp.get(bs, 0) + 1
        
    elif (hd=='laosheng') and (sq=='erhuang') and (ju in ['s','s1','s2','x']):
        lseh[bs] = lseh.get(bs, 0) + 1
        
    elif (hd=='laosheng') and (sq=='xipi') and (ju in ['s','x']):
        lsxp[bs] = lsxp.get(bs, 0) + 1
        
    else:
        others[hd+sq+bs+ju] = others.get(hd+sq+bs+ju, 0) + 1

categories = {'hd':[],'sq':[],'bs':[],'ju':[]}

for line in data:
    strInfo = line.strip().split(',')
    hd = strInfo[1]
    sq = strInfo[2]
    bs = strInfo[3]
    ju = strInfo[4]
    if (hd not in categories['hd']) and (hd != ''):
        categories['hd'].append(hd)
    if (sq not in categories['sq']) and (sq != ''):
        categories['sq'].append(sq)
    if (bs not in categories['bs']) and (bs != ''):
        categories['bs'].append(bs)
    if (ju not in categories['ju']) and (ju != ''):
        categories['ju'].append(ju)

arias = {}

for line in data:
    strInfo = line.strip().split(',')
    aria = strInfo[0]
    if aria != '':
        label = aria.split('-')[0]
        arias[label] = arias.get(label, 0) + 1

books = {}
otherSources = []
accompaniment = {}

for line in corpus:
    strInfo = line.strip().split(',')
    source = strInfo[6]
    author = source[:3]
    if author in '曹宝荣刘吉典张正治':
        books[author] = books.get(author, 0) + 1
    else:
        otherSources.append(source)
        label = source[:7]
        books[label] = books.get(label, 0) + 1
    acc = strInfo[5]
    accompaniment[acc] = accompaniment.get(acc, 0) + 1
otherSources = sorted(otherSources)
