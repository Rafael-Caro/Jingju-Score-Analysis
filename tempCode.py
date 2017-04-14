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
import pickle

#diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

#lyricsData = 'scores/lyricsdata.4.0.csv'

path = '../CONFERENCES/2017.10 ISMIR/Patterning/'
inputScoreFile = path + 'scores/laosheng-xipi-yuanban.pkl'
materialFile = path + 'scores/laosheng-xipi-yuanban_material.pkl'
resultsFile = path + 'results/Rong/knn5_laosheng-xipi-yuanban.pkl'

with open(inputScoreFile, 'rb') as f:
    inputScore = pickle.load(f)

with open(materialFile, 'rb') as f:
    material = pickle.load(f)

with open(resultsFile, 'rb') as f:
    results = pickle.load(f)

lyricsData = 'scores/lyricsdata.4.0.csv'

#path = lyricsData[:lyricsData.rindex('/')+1]
#print(path)

with open(lyricsData, 'r', encoding='utf-8') as f:
    data = f.readlines()

def findLine(a, b):
    line = results[a][b]
    for n in line:
        print(n)
    loc = line[-1][0]
    x = material[-1][loc]
    score = material[x[0]][0]
    segment = material[x[0]][x[1]][x[2]]
    print(segment)
    segStart = float(segment[0])
    segEnd = float(segment[1])
    s = converter.parse(score)
    parts = jS.findVoiceParts(s)
    part = parts[x[1]-1]
    notes = part.flat.notesAndRests.stream()
    seg2show = notes.getElementsByOffset(segStart, segEnd)
    seg2show.show()
    

dataDict = {}
currentScore = ''

for l in data:
    strInfo = l.strip().split(',')
    score = strInfo[0]
    if score != '':
        currentScore = score
        dataDict[currentScore] = [[]]
        if 'Part' in l: continue
    else:
        if 'Part' in l:
            dataDict[currentScore].append([])
            continue
    info = strInfo[1]+', '+strInfo[2]+', '+strInfo[3]+', '+strInfo[4]
    start = strInfo[6]
    end = strInfo[7]
    dataDict[currentScore][-1].append([start, end, info])

i = 0
pat = results[i]
s1 = stream.Score()
s1.insert(0, metadata.Metadata(movementName='Pattern ' + str(i+1)))
for j in range(len(pat)):
    occ = pat[j]
    locator = occ[-1]
    line = locator[0]
    init = locator[1]
    # Chek if the occurrence retrieved coincides with a fragment of the input
    # score
    origLine = inputScore[line]
    for k in range(len(occ)-1):
        if occ[k] != origLine[k+init]:
            print(origLine)
            print(occ)
            raise Exception('No match in result ' + str(i) + ', ' + str(j))
    lineCoordinates = material[-1][line]
    s = lineCoordinates[0]
    p = lineCoordinates[1]
    l = lineCoordinates[2]
    scorePath = material[s][0]
    segStart = material[s][p][l][0]
    segEnd = material[s][p][l][1]
    
    s2 = converter.parse(scorePath)
    parts = jS.findVoiceParts(s2)
    part = parts[p-1]
    notes = part.flat.notesAndRests.stream()
    seg2red = notes.getElementsByOffset(segStart, segEnd)
#    adj = 0
#    for n in seg2red:
#        if n.tie != None and n.tie.type != 'start':
#            print('tie')
#            adj += 1
#    x = -1
#    while seg2red[x].isRest:
#        adj += 1
#        print('final rest')
#        x += -1
#    print(len(occ)-1, init, len(seg2red)-adj)
#    for x in occ:
#        print(x)
#    seg2red.show()
    
    tieJump = 0
    for n in range(len(occ)-1):
        note2red = seg2red[n+init+tieJump]
        while note2red.tie != None and note2red.tie.type != 'start':
            tieJump += 1
            note2red = seg2red[n+init+tieJump]
        if note2red.isRest:
            noteName = note2red.name
        else:
            noteName = note2red.nameWithOctave
        if noteName != occ[n][0]:
            raise Exception("Notes doesn't match at", i, j, k)
        note2red.color = 'red'
        tieHop = 1
        if note2red.tie != None:
            while seg2red[n+init+tieJump+tieHop].tie != None:
                seg2red[n+init+tieJump+tieHop].color = 'red'
                tieHop += 1

    scoreName = scorePath.split('/')[-1]
    score = dataDict[scoreName]
    print(scoreName)
    for ñ in score[p-1]:
        print(ñ)
    print(segStart, segEnd)
    lineHop = 0
    dataLine = score[p-1][lineHop]
    while (float(dataLine[0]) < segStart) and (lineHop < len(score[p-1])-1):
        lineHop += 1
        dataLine = score[p-1][lineHop]

    segmentStart = float(dataLine[0])
    segmentEnd = float(dataLine[1])
    print(segmentStart, segmentEnd)
    print()
    seg2add = notes.getElementsByOffset(segmentStart, segmentEnd)
    offsetHop = seg2add[0].offset    
    for nn in seg2add:
        nn.offset += -offsetHop
    s1.insert(0, seg2add)

#s1.show()