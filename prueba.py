# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
from music21 import *
import jingjuScores as js

#s = converter.parse(f)
#
#parts = s.parts[-2:]
#
#for p in parts:
#    for m in p[1:]:
#        m.remove(m[-1])
#    notes = p.flat.notesAndRests
#    for n in notes:
#        n.quarterLength = (n.quarterLength * 2)
#        
#s.show()

#allfiles = os.listdir('./scores')
#scores = []
#for f in allfiles:
#    if f[-3:] == 'xml':
#        scores.append('scores/' + f)
#
#duration = 1
#
#for score in scores:
#    s = converter.parse(score)
#    parts = js.findVoiceParts(s)
#    for part in parts:
#        notes = part.flat.notes
#        for n in notes:
#            d = n.quarterLength
#            if (d < duration) and (d > 0):
#                duration = d

########################
###### STATISTICS ######
########################

#folders = ['../ERHUANG/erhuang-manban/scores/',
#           '../ERHUANG/erhuang-yuanban/scores/',
#           '../XIPI/xipi-manban/scores/',
#           '../XIPI/xipi-yuanban/scores/',
#           '../XIPI/xipi-kuaiban/scores/']
#
#lista = ''
#
#for folder in folders:
#    files = os.listdir(folder)
#    for f in files:
#        if f[-4:] == 'mscz':
#            lista += f + '\n'
#
#with open('lista.txt', 'w') as f:
#    f.write(lista)

tones = 'tones.csv'

with open(tones, 'r', encoding='utf-8') as f:
    data = f.readlines()

diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

texto = ''

for j in range(len(data)):
    line = data[j]
    texto += str(j) + '.\t'
    if 'Part' in line:
        texto += line.split(',')[0]+'\n'
        continue
    fix = 0    
    text = line.split(',')[0]
    tonos = line.split(',')[1]
    for i in range(len(text)):
        if text[i] in diacritics:
            fix += 1
            texto += text[i]
        else:
            texto += text[i]+tonos[i-fix]
    texto += '\n'

#print(texto)

with open('tones.txt', 'w', encoding='utf-8') as f:
    f.write(texto)
        