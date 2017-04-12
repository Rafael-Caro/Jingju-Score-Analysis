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

diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

lyricsData = 'scores/lyricsdata.4.0.csv'

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

#a = jSA.getAmbitus(material)

#scores = jSA.findScore(material, 'E4', 'low')

#allfiles = os.listdir('scores/')
#
#shengscores = []
#
#for f in allfiles:
#    if f[:2] == 'ls':
#        shengscores.append('scores/' + f)
#
#scores2change = []
#
#for score in shengscores:
#    includeScore = False
#    s = converter.parse(score)
#    print(score.split('/')[-1], 'parsed')
#    p = jS.findVoiceParts(s)[0]
#    notes = p.flat.notes.stream()
#    for n in notes:
##        if n.nameWithOctave == 'C##4':
##            n.color = 'red'
##            includeScore = True
##    if includeScore: s.show()
#        m = n.pitch.midi
#        if m > pitch.Pitch('C#5').midi:
#            includeScore = True
#            n.color = 'red'
#    if includeScore:
#        scores2change.append(score)
#        s.show()

lyricsDataTest = 'scores/lyricsdataTest.csv'
material = jSA.collectJudouMaterial(lyricsData, sq=['xipi'], bs=['sanyan'],
                                    ju=['x'])
recodedScore = jSP.recodeScore(material, noteName='midi')