# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:37:52 2017

@author: Rafael.Ctt
"""

import jingjuScores as jS
import jingjuScoreAnalysis as jSA

import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Create a concatenated score')
    parser.add_argument('csvfile', help='the csv file with the scores info')
    args = parser.parse_args()
    
    material = jSA.collectMaterial(args.csvfile, hd=['laosheng'], sq=['erhuang'])
    s, m = jSA.concatenateSegments(material, title='prueba')
    
