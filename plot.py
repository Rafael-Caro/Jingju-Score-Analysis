# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:04:08 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
import jingjuScores as jS
import jingjuScoreAnalysis as jSA

lyricsData = 'scores/lyricsdata.4.0.csv'

#material = jSA.collectMaterial(lyricsData, hd=['laosheng'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)
#
#material = jSA.collectMaterial(lyricsData, hd=['dan'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)
#
#material = jSA.collectMaterial(lyricsData, hd=['laosheng'], sq=['erhuang'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)
#
#material = jSA.collectMaterial(lyricsData, hd=['laosheng'], sq=['xipi'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)
#
#material = jSA.collectMaterial(lyricsData, hd=['dan'], sq=['erhuang'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)
#
#material = jSA.collectMaterial(lyricsData, hd=['dan'], sq=['xipi'])
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)

#tones = jSA.getTones(lyricsData, hd=['dan'], sq=['xipi'], bs=['yuanban'],
#                     ju=['x'])

material = jSA.collectMaterial(lyricsData, hd=['laosheng'], sq=['erhuang'])
#material = jSA.collectMaterial(lyricsData, hd=['dan'], sq=['xipi'],
#                               bs=['erliu'], ju=['s'])
s, m = jSA.concatenateSegments(material, title='prueba')