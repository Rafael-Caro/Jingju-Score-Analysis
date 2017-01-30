# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
from music21 import *
import jingjuScores as js

f = '../XIPI/xipi-yuanban/scores/da-xp-yb-x-2.xml'

s = converter.parse(f)

parts = s.parts[-2:]

for p in parts:
    for m in p[1:]:
        m.remove(m[-1])
    notes = p.flat.notesAndRests
    for n in notes:
        n.quarterLength = (n.quarterLength * 2)
        
s.show()

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