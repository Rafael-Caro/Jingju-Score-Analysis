# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingjuScoreAnalysis as jSA
import jingjuScores as jS

linesData = 'scores/lines_data.csv'

hangdang = ['laosheng']
shengqiang = ['xipi']
banshi = ['liushui']

material = jSA.collectJudouMaterial(linesData, hd=hangdang, sq=shengqiang,
                                   bs=banshi)