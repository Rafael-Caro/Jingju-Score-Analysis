# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 11:27:08 2017

@author: Rafael.Ctt
"""
        
allfiles = os.listdir('scores/')

corpus = 'scores/corpus.csv'
lyricsdata = 'scores/lyricsdata.4.0.csv'

with open(corpus, 'r', encoding='utf-8') as f:
    cor = f.readlines()

with open(lyricsdata, 'r', encoding='utf-8') as f:
    data = f.readlines()

daeh = []

daxp = []

lseh = []

lsxp = []

for i in allfiles:
    if i[:4] == 'daeh':
        daeh.append(i)
    elif i[:4] == 'daxp':
        daxp.append(i)
    elif i[:4] == 'lseh':
        lseh.append(i)
    elif i[:4] == 'lsxp':
        lsxp.append(i)

daehPlays = {}
for i in daeh:
    ii = i[:-4]
    play = ii.split('-')[2]
    if play in daehPlays:
        daehPlays[play].append(i)
    else:
        daehPlays[play] = [i]

daxpPlays = {}
for i in daeh:
    ii = i[:-4]
    play = ii.split('-')[2]
    if play in daxpPlays:
        daxpPlays[play].append(i)
    else:
        daxpPlays[play] = [i]

lsehPlays = {}
for i in lseh:
    ii = i[:-4]
    play = ii.split('-')[2]
    if play in lsehPlays:
        lsehPlays[play].append(i)
    else:
        lsehPlays[play] = [i]

lsxpPlays = {}
for i in lsxp:
    ii = i[:-4]
    play = ii.split('-')[2]
    if play in lsxpPlays:
        lsxpPlays[play].append(i)
    else:
        lsxpPlays[play] = [i]

toShow = []

for k in daehPlays:
    if len(daehPlays[k]) > 1:
        print(daehPlays[k])
        for i in daehPlays[k]:
            toShow.append(i)

for k in daxpPlays:
    if len(daxpPlays[k]) > 1:
        print(daxpPlays[k])
        for i in daxpPlays[k]:
            toShow.append(i)

for k in lsehPlays:
    if len(lsehPlays[k]) > 1:
        print(lsehPlays[k])
        for i in lsehPlays[k]:
            toShow.append(i)

for k in lsxpPlays:
    if len(lsxpPlays[k]) > 1:
        print(lsxpPlays[k])
        for i in lsxpPlays[k]:
            toShow.append(i)

texto = ''

toPrint = False

for l in data:
    line = l.strip().split(',')
    name = line[0]
    lyrics = line[5]
    if name != '':
        if name in toShow:
            print('\n' + name)
            texto += '\n' + name + '\n'
            toPrint = True
        else:
            toPrint = False
    if toPrint:
        print(lyrics)
        texto += lyrics + '\n'

with open('duplicates.txt', 'w', encoding='utf-8') as f:
    f.write(texto)