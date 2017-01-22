# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
from music21 import *

with open('scores/lyricsdata.csv', 'r', encoding='utf-8') as f:
    linesdata = f.readlines()

f = 'scores/lseh-YiLunMing-ZhuoFangCao-1.xml'

s = converter.parse(f)

p = s.parts[0]
toRemove = list(p.recurse().getElementsByClass(['PageLayout', 'SystemLayout',
                'Barline']))
p.remove(toRemove, recurse=True)

for i in linesdata[548:555]:
    datacolumns = i.split(',')
    startStr = datacolumns[-2]
    endStr = datacolumns[-1]
    if '/' in startStr:
        start = float(startStr.split('/')[0]) / float(
                                            startStr.split('/')[1])
    else:
        start = float(startStr)
    
    if '/' in endStr:
        end = float(endStr.split('/')[0]) / float(
                                              endStr.split('/')[1])
    else:
        end = float(endStr)
        
    line = p.getElementsByOffset(start, end, mustBeginInSpan=False,
                                           includeElementsThatEndAtStart=False)
    
    line.show()