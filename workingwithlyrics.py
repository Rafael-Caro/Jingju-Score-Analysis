# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 10:56:39 2017

@author: Rafael.Ctt
"""

import jingjuLyricsAnalysis as jLA

linesData = 'scores/lines_data.csv'

#material = jLA.countLineType(linesData, hd=['dan'], sq=['erhuang'])
#
#for i in material[-1]:
#    if i[0].index(':') == 2:
#        x = i[0]
#    else:
#        x = ' ' + i[0]
#    print(x + '\t' + str(i[1]) + '\t' + str(i[2]))

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

material = jLA.collectTonesMaterial(linesData, bs=['erliu'])
temp, n = jLA.toneContour(material)