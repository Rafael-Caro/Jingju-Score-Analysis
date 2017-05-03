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

linesData = 'scores/lines_data.csv'

# All entities for reference
hd_default = ['laosheng', 'dan']
sq_default = ['erhuang', 'xipi']
bs_default = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
              'yuanban', 'erliu', 'liushui', 'kuaiban']
ju_default = ['s', 's1', 's2', 'x']

hangdang = ['laosheng']
shengqiang = ['xipi']
banshi = ['liushui']
line = ['x']

# MATERIAL PER LINE
#material = jSA.collectLineMaterial(linesData, hd=hangdang, sq=shengqiang,
#                                   bs=banshi, ju=line)

# MATERIAL PER JUDOU
#judouMaterial = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
#                                         sq=shengqiang, bs=banshi, ju=line)

# PITCH HISTOGRAM
#pitchHist = jSA.pitchHistogram(material, count='sum', countGraceNotes=True,
#                               makePlot=True)

# INTERVAL HISTOGRAM
#intvlHist = jSA.intervalHistogram(material,count='sum',directedInterval=False,
#                                  silence2ignore=0.125, ignoreGraceNotes=False,
#                                  makePlot=True)

# MELODIC DENSITY
#totalCount = jSA.melodicDensity(material, filename, includeGraceNotes=True,
#                                notesOrDuration='notes')

# MATERIAL FOR CADENTIAL NOTES
if 'erhuang' in shengqiang:
    material_s1 = jSA.collectJudouMaterial(linesData, hd=hangdang,
                                           sq=shengqiang, bs=banshi, ju=['s1'])
    material_s2 = jSA.collectJudouMaterial(linesData, hd=hangdang,
                                           sq=shengqiang, bs=banshi, ju=['s2'])
    material_x = jSA.collectJudouMaterial(linesData, hd=hangdang,
                                          sq=shengqiang, bs=banshi, ju=['x'])
    judouMaterialList = [material_s1, material_s2, material_x]
    
elif 'xipi' in shengqiang:
    material_s = jSA.collectJudouMaterial(linesData, hd=hangdang,
                                          sq=shengqiang, bs=banshi, ju=['s'])
    material_x = jSA.collectJudouMaterial(linesData, hd=hangdang,
                                          sq=shengqiang, bs=banshi, ju=['x'])
    judouMaterialList = [material_s, material_x]

#jSA.cadentialNotes(judouMaterialList, includeGraceNotes=True, makePlot=True)
y = jSA.cadentialNotes(judouMaterialList)