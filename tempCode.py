# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingju_singing_analysis as jSA

linesData = 'scores/lines_data.csv'

material = jSA.collectJudouMaterial(linesData, hd=['laosheng'], sq=['xipi'],
                                    bs = ['yuanban'], ju = ['s'])

count = jSA.judouPitchHistogram(material)