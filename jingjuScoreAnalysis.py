# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 13:57:50 2017

@author: Rafael.Ctt
"""
import numpy as np
import matplotlib.pyplot as plt
from music21 import *
import jingjuScores as jS

f = 'scores/lsxp-LiangGuoJiao-ShiJieTing-1.xml'
s = converter.parse(f)
part = jS.findVoiceParts(s)[0]

def plotting(xPositions, xLabels, yValues, width=0.8):

    plt.figure()
    plt.bar(xPositions, yValues, width)
    plt.xticks(xPositions + width/2, xLabels)
    plt.show()

#def collectMaterial():
#   '''
#   '''
lyricsData = 'scores/lyricsdata-test.csv'

with open(lyricsData, 'r', encoding='utf-8') as f:
    data = f.readlines()

#hd = ['laosheng', 'dan']
#sq = ['erhuang', 'xipi']
#bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban', 'erliu',
#      'liushui', 'kuaiban']
#ju = ['s', 's1', 's2', 'x']

hd = ['laosheng']
sq = ['erhuang']
bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban', 'erliu',
      'liushui', 'kuaiban']
ju = ['x']

material = []

for line in data:
    strInfo = line.strip().split(',')
    score = strInfo[0]
    if score != '':
        material.append([score,[]])
        if 'Part 1' in line: continue

    if (score == '') and ('Part' in line):
        material[-1].append([])
        continue
    
    hd0 = strInfo[1]
    sq0 = strInfo[2]
    bs0 = strInfo[3]
    ju0 = strInfo[4]
    
    start = float(strInfo[6])
    end = float(strInfo[7])
    
    if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
        material[-1][-1].append([start, end])
        
# Delete empty lists
score2remove = []
for i in range(len(material)):
    score = material[i]
    partsLength = 0
    for j in range(1, len(score)):
        part = score[j]
        partsLength += len(part)
    if partsLength == 0:
        score2remove.insert(0, i)
if len(score2remove) != 0:
    for l in score2remove:
        material.pop(l)

#def pitchHistogram(part, count='sum', countGraceNotes=True):
#    '''
#    '''

#count='abs'
#countGraceNotes=True
#
#notes = part.flat.notes.stream()
#
#if countGraceNotes:
#    minDur = 0.25
#    for n in notes:
#        noteDur = n.quarterLength
#        if noteDur!=0 and noteDur<minDur:
#            minDur = noteDur
#
#pitchCount = {}
#
#for n in notes:
#    noteName = n.nameWithOctave
#    noteDur = n.quarterLength
#    if noteDur == 0:
#        if not countGraceNotes: continue
#        noteDur = minDur
#    pitchCount[noteName] = pitchCount.get(noteName, 0) + noteDur
#
## Sorting duration per pitch class frequency
#pitches = pitchCount.keys()
#toSort = {p:pitch.Pitch(p).midi for p in pitches}
#sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
#xPositions = np.array([p[1] for p in sortedPitches])
#xLabels = [p[0] for p in sortedPitches]
#yValues = np.array([pitchCount[l] for l in xLabels])
#
## Normalising, if requested
#if count == 'sum':
#    yValues = yValues / float(sum(yValues))
#    yLabel = 'Normalized Count'
#elif count == 'max':
#    yValues = yValues / float(max(yValues))
#    yLabel = 'Normalized Count'
#else:
#    yLabel = 'Count'
#    
#plotting(xPositions, xLabels, yValues)