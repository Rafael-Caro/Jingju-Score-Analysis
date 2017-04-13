# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
from music21 import *
import jingjuScores as jS
import jingjuScoreAnalysis as jSA
import jingjuScorePatterns as jSP

#diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

#lyricsData = 'scores/lyricsdata.4.0.csv'

#hd=['laosheng', 'dan']
#sq=['erhuang', 'xipi']
#bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban', 'erliu',
#      'liushui', 'kuaiban']
#ju = ['s', 's1', 's2', 'x']

#material = jSA.collectMaterial(lyricsData, bs=['erliu'])
#jSA.pitchHistogram(material)
#jSA.intervalHistogram(material, directedInterval=False)
#jSA.findInterval(material, ['m7'], directedInterval=False, ignoreGraceNotes=True)

#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)



#lyricsData = 'scores/lyricsdata4-unique.csv'
#material = jSA.collectMaterial(lyricsData, hd=['laosheng'], sq=['xipi'],
#                               bs=['yuanban'], ju=['s'])
#syllables, notesPerSyl = jSA.melodicDensity(material, includeGraceNotes=False)
#concatenatedScore, extendedMaterial = jSP.concatenateSegments(material)

path = '../CONFERENCES/2017.10 ISMIR/Patterning/'

concatenatedScore = path + 'scores/laosheng-erhuang-yuanban.xml'

#resultsFile = path + 'results/Tom/laosheng-erhuang-yuanban_SIARCT-C.txt'
resultsFile = path + 'results/Rong/knn5_laosheng-erhuang.pkl'

#results = jSP.showResultPatterns(resultsFile, concatenatedScore)
jSP.plotFoundPatterns(resultsFile, showScore=False)