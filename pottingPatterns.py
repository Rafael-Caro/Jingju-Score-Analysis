# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:27:51 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
import jingjuScorePatterns as jSP
import pickle

lyricsData = 'scores/lyricsdata.4.0.csv'

path = '../CONFERENCES/2017.10 ISMIR/Patterning/'
core = 'laosheng-xipi-yuanban'
inputScoreFile = path + 'scores/' + core + '.pkl'
materialFile = path + 'scores/' + core + '_material.pkl'
rongs_results = path + 'results/Rong/knn5_' + core + '.pkl'
toms_results = path + 'results/Tom/' + core + '_SIARCT-C.txt'
merediths_results = path + 'results/Meredith/' + core + '.txt'
concatenatedScore = path + 'scores/' + core + '.xml'

# MEREDITH'S RESULTS
#jSP.showPatternsFromText(merediths_results, morpheticPitch=False, 
#                         concatenatedScore=None)

# TOM'S RESULTS
#jSP.showPatternsFromText(toms_results, morpheticPitch=True, 
#                         concatenatedScore=None)

# RONG'S RESULTS
jSP.showPatternsFromPickle(lyricsData, materialFile, inputScoreFile,
                           rongs_results)