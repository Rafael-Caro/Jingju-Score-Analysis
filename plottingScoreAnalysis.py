# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:08:27 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
import jingjuScoreAnalysis as jSA
import pickle

#diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

lyricsData = 'scores/lyricsdata.4.0.csv'

# All entities for reference
# hd=['laosheng', 'dan']
# sq=['erhuang', 'xipi']
# bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban', 'erliu',
#      'liushui', 'kuaiban']
# ju = ['s', 's1', 's2', 'x']

hangdang = ['laosheng', 'dan']
shengqiang = ['erhuang', 'xipi']
banshi = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban', 'erliu',
          'liushui', 'kuaiban']
line = ['s', 's1', 's2', 'x']

material = jSA.collectMaterial(lyricsData, hd=hangdang, sq=shengqiang,
                               bs=banshi, ju=line)

# PITCH HISTOGRAM
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)

# INTERVAL HISTOGRAM
#jSA.intervalHistogram(material, count='sum', directedInterval=False,
#                      silence2ignore=0.25, ignoreGraceNotes=False)

# MELODIC DENSITY
#totalCount = jSA.melodicDensity(material, includeGraceNotes=True,
#                                notesOrDuration='notes')