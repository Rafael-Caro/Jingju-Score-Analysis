# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingjuScoreAnalysis as jSA
import jingjuScores as jS

linesData = 'scores/lines_data.csv'

x = [['laosheng', 'erhuang', 'manban'],
     ['laosheng', 'erhuang', 'sanyan'],
     ['laosheng', 'erhuang', 'kuaisanyan'],
     ['laosheng', 'erhuang', 'yuanban'],
     ['laosheng', 'xipi', 'manban'],
     ['laosheng', 'xipi', 'sanyan'],
     ['laosheng', 'xipi', 'kuaisanyan'],
     ['laosheng', 'xipi', 'yuanban'],
     ['laosheng', 'xipi', 'liushui'],
     ['laosheng', 'xipi', 'kuaiban'],
     ['dan', 'erhuang', 'manban'],
     ['dan', 'erhuang', 'zhongsanyan'],
     ['dan', 'erhuang', 'kuaisanyan'],
     ['dan', 'erhuang', 'yuanban'],
     ['dan', 'xipi', 'manban'],
     ['dan', 'xipi', 'yuanban'],
     ['dan', 'xipi', 'erliu'],
     ['dan', 'xipi', 'liushui'],
     ['dan', 'xipi', 'kuaiban']]

i = x[18]
material = jSA.collectLineMaterial(linesData, hd=[i[0]], sq=[i[1]], bs=[i[2]])
results = jSA.melodicDensity(material, notesOrDuration='duration')
print('\t', i[0], i[1], i[2], results['Avg']['upper fence'], '\n')

