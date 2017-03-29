# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
from music21 import *
import jingjuScores as js

diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

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

###CREATE THE FILE TONES FROM SHUO'S COLUMN
#tones = 'tones.csv'
#
#with open(tones, 'r', encoding='utf-8') as f:
#    data = f.readlines()
#
#texto = ''
#
#for j in range(len(data)):
#    line = data[j]
#    texto += str(j) + '.\t'
#    if 'Part' in line:
#        texto += line.split(',')[0]+'\n'
#        continue
#    fix = 0    
#    text = line.split(',')[0]
#    tonos = line.split(',')[1]
#    for i in range(len(text)):
#        if text[i] in diacritics:
#            fix += 1
#            texto += text[i]
#        else:
#            texto += text[i]+tonos[i-fix]
#    texto += '\n'
#
##print(texto)
#
#with open('tones.txt', 'w', encoding='utf-8') as f:
#    f.write(texto)
#        

#f1 = 'tones2.txt'
#
#f2 = 'scores/lyricsdata.3.0.csv'
#
#with open(f1, 'r', encoding='utf-8') as f:
#    tones = f.readlines()
#    
#with open(f2, 'r', encoding='utf-8') as f:
#    lyricsdata = f.readlines()
    
## Check that tones2 has the same lyrics and punctuation than lyricsdata
#for i in range(len(tones)):
#    if 'Part' in lyricsdata[i]: continue
#    line1 = lyricsdata[i].split(',')[5]
#    line2 = ''
#    for j in tones[i].split('\t')[1][:-1]:
#        if j not in ['1','2','3','4','5']:
#            line2 += j
#    comp = line1 == line2
#    if not comp:
#        print(tones[i].split('\t')[0], line1, line2)

#newtones = ''
#
#for i in tones:
#    if 'Part' in i:
#        tonesline = '\n'
#    else:
#        tonesline = '\"'
#        line = i.split('\t')[1][:-1]
#        consider = True
#        for j in line:
#            if j == '（':
#                consider = False
#            elif (j in '12345') and consider:
#                tonesline += j
#            elif j == '）':
#                consider = True
#        tonesline += '\"\n'
#    newtones += tonesline

#for i in range(len(newtones.split('\n'))-1):
#    print(newtones.split('\n')[i] + '\n' +
#          tones[i+730].split('\t')[1][:-1])

#for i in tones:
#    line = i.split('\t')[1][:-1]
#    if '）' in line:
#        j = line.rindex('）')
#        if line[j-1] not in '12345':
#            print(i)

#for i in range(900, len(lyricsdata)):
#    preline = lyricsdata[i].split(',')[5]
#    if 'Part' in preline: continue
#    tonesline = newtones.split('\n')[i]
#    jump = 0
#    inBrackets = False
#    line = ''
#    for j in range(len(preline)):
#        ch = preline[j]
#        if ch not in diacritics:
#            line += ch
#            if not inBrackets:
#                line += tonesline[j-jump]
#            else:
#                jump += 1
#        else:
#            line += ch
#            jump += 1
#            if ch == '（':
#                inBrackets = True
#            elif ch == '）':
#                inBrackets = False
#    print(i, line)

#f1 = 'scores/lyricsdata.3.0.csv'
#
#with open(f1, 'r', encoding = 'utf-8') as f:
#    data = f.readlines()
#    
#for i in data:
#    if 'Part' in i: continue
#    strInfo = i.strip().split(',')
#    count1 = len(strInfo[5])
#    count2 = len(strInfo[9]) + len(strInfo[10]) + len(strInfo[11])
#    if count1 != count2:
#        print(data.index(i), strInfo[5], strInfo[9], strInfo[10], strInfo[11])

corpusfile = './scores/corpus.csv'

with open(corpusfile, 'r', encoding='utf-8') as f:
    corpus = f.readlines()

acc = ''

for line in corpus:
    strInfo = line.strip().split(',')
    source = strInfo[6]
    author = source[:3]
    if author=='曹宝荣':
        acc += 'yes\n'
    elif author in '刘吉典张正治':
        acc += 'no\n'
    else:
        acc += '\n'

with open('acc.csv', 'w') as f:
    f.write(acc)
    