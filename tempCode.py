# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 15:42:10 2017

@author: Rafael.Ctt
"""

import jingjuScoreAnalysis as jSA
import jingjuScores as jS

lyricsData = 'scores/lyricsdata.4.1.csv'

hangdang = ['laosheng', 'dan']
shengqiang = ['erhuang', 'xipi']
banshi = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan']
material_s1 = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
                                       sq=shengqiang, bs=banshi, ju=['s1'])
material_s2 = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
                                       sq=shengqiang, bs=banshi, ju=['s2'])
material_s = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
                                      sq=shengqiang, bs=banshi, ju=['s'])
material_x = jSA.collectJudouMaterial(lyricsData, hd=hangdang,
                                      sq=shengqiang, bs=banshi, ju=['x'])
judouMaterialList = [material_s1, material_s2, material_x]
jSA.cadentialNotes(judouMaterialList, includeGraceNotes=True, makePlot=True)