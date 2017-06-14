# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 10:56:39 2017

@author: Rafael.Ctt
"""

import jingjuLyricsAnalysis as jLA
import jingjuScoreAnalysis as jSA

#linesData = 'scores/lines_data.csv'
linesData = 'scores/test.csv'

#material = jLA.countLineType(linesData, hd=['dan'], sq=['erhuang'])
#
#for i in material[-1]:
#    if i[0].index(':') == 2:
#        x = i[0]
#    else:
#        x = ' ' + i[0]
#    print(x + '\t' + str(i[1]) + '\t' + str(i[2]))

material = jLA.collectTonesMaterial(linesData)
temp, n = jLA.toneContour(material)



###############################################################################

### Comprobar que han tantos tonos caracteres por verso
#with open(linesData, 'r', encoding='utf-8') as f:
#    data = f.readlines()
#
#for i in range(len(data)):
#    line = data[i]
#    if 'Part' in line: continue
#    strInfo = line.strip().split(',')
#    tones = strInfo[8]
#    lyrics = strInfo[5]
#    
#    if len(tones) != jLA.countCharacters(lyrics):
#        print('Problem at line', i+1)
#        print('\t', lyrics, jLA.countCharacters(lyrics), tones, len(tones))

### Contar tonos:
#tonesCount = {}
#for s in material[1:]:
#    for p in s[1:]:
#        for l in p:
#            tones = l[-1]
#            print(tones)
#            for i in tones:
#                tonesCount[i] = tonesCount.get(i, 0) + 1
#
#if len(tonesCount) == 5:
#    for t in '12345':
#        print(t + ': ' + str(tonesCount[t]))
#else:
#    print(tonesCount.keys())

### Ver ornaments
#
#material = material = jSA.collectLineMaterial(linesData)
#
#ornaments = {}
#
#for score in material[1:]:
#    scorePath = score[0]
#    scoreName = scorePath.split('/')[-1]
#    loadedScore = converter.parse(scorePath)
#    print(scoreName, 'parsed')
#    parts = jSA.findVoiceParts(loadedScore)
#    for partIndex in range(1, len(score)):
#        if len(score[partIndex]) == 0: continue # Skip part if it's empty
#        # Get the notes from the current part
#        part = parts[partIndex-1]
#        notes = part.flat.notes.stream()
#        for startEnd in score[partIndex]:
#            start = startEnd[0]
#            end = startEnd[1]
#            segment = notes.getElementsByOffset(start, end)
#            for n in segment:
#                if len(n.expressions) > 0:
#                    for e in n.expressions:
#                        ornaments[e.name] = ornaments.get(e.name, 0) + 1
                