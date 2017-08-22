# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingju_singing_analysis as jSA

linesData = 'scores/lines_data.csv'

material = jSA.collectJudouMaterial(linesData, hd=['laosheng'], sq=['erhuang'],
                                    bs = ['yuanban'], ju = ['x'])

results = jSA.judouPitchHistogram(material)