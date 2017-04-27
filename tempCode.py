# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingjuScoreAnalysis as jSA
import jingjuScores as jS

#lyricsData = 'scores/lyricsdata.4.0.csv'
#lyricsData = 'scores/lyricsdataTest.csv'

# All entities for reference
#hd_default = ['laosheng', 'dan']
#sq_default = ['erhuang', 'xipi']
#bs_default = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
#              'erliu', 'liushui', 'kuaiban']
#ju_default = ['s', 's1', 's2', 'x']
#
#hangdang = hd_default
#shengqiang = sq_default
#banshi = bs_default
#line = ju_default
#
#material = jSA.collectMaterial(lyricsData, hd=hangdang, sq=shengqiang,
#                    bs = banshi, ju = line)
#
#jSA.findScoreByInterval(material, ['m7', 'P8', 'M9', 'm10', 'P11'])
#jSA.findScoreByPitch(material, ['C##4', 'A#4'])

#dous = jS.judouSegmentation(lyricsData, 'todelete.csv')

with open('scores/corpus.csv', 'r', encoding='utf-8') as f:
    corpus = f.readlines()
    
recordings = 0

for l in corpus:
    line = l.strip().split(',')
    if line[-1] != '--':
        recordings += 1

line = corpus[0].strip().split(',')

for i in range(len(line)):
    print(i, line[i])

acc = 0

for l in corpus:
    line = l.strip().split(',')
    if line[5] == 'yes':
        acc += 1