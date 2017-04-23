# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:08:27 2017

@author: Rafael.Ctt
"""

import os
os.chdir('C:/Users/Rafael.Ctt/Documents/PhD/Code')
import jingjuScoreAnalysis as jSA
import pickle

#diacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

lyricsData = 'scores/lyricsdata.4.0.csv'

# All entities for reference
hd_default = ['laosheng', 'dan']
sq_default = ['erhuang', 'xipi']
bs_default = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
              'erliu', 'liushui', 'kuaiban']
ju_default = ['s', 's1', 's2', 'x']

hangdang = ['laosheng']
shengqiang = ['xipi']
banshi = ['yuanban']
line = ['x']

# MATERIAL PER LINE
#material = jSA.collectMaterial(lyricsData, hd=hangdang, sq=shengqiang,
#                               bs=banshi, ju=line)

# MATERIAL PER JUDOU
#judouMaterial = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
#                                         sq=shengqiang, bs=banshi, ju=line)

# PITCH HISTOGRAM
#jSA.pitchHistogram(material, count='sum', countGraceNotes=True)

# INTERVAL HISTOGRAM
#jSA.intervalHistogram(material, count='sum', directedInterval=True,
#                      silence2ignore=0.25, ignoreGraceNotes=False)

# MELODIC DENSITY
#totalCount = jSA.melodicDensity(material, includeGraceNotes=True,
#                                notesOrDuration='duration')

# FIND INTERVALS
#
#intvlList = []
#
#jSA.findInterval(material, intvlList, directedInterval=False,
#                 silence2ignore=0.25, ignoreGraceNotes=False)

# MATERIAL FOR CADENTIAL NOTES
material_s = jSA.collectJudouMaterial(lyricsData, hd=hangdang, sq=shengqiang,
                                      bs=banshi, ju=['s'])
#material_s1 = jSA.collectJudouMaterial(lyricsData, hd=hangdang, sq=shengqiang,
#                                       bs=banshi, ju=['s1'])
#material_s2 = jSA.collectJudouMaterial(lyricsData, hd=hangdang, sq=shengqiang,
#                                       bs=banshi, ju=['s2'])
material_x = jSA.collectJudouMaterial(lyricsData, hd=hangdang, sq=shengqiang,
                                      bs=banshi, ju=['x'])

# CADENTIAL NOTES
#x, y, z = jSA.cadentialNotes(judouMaterial, includeGraceNotes=True)
judouMaterialList = [material_s, material_x]
x = jSA.plottingBoxPlots(judouMaterialList, includeGraceNotes=True)