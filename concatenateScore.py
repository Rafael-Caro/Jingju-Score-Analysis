# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:37:52 2017

@author: Rafael.Ctt
"""

import jingjuScoreAnalysis as jSA
import jingjuScorePatterns as jSP

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']
    
    parser = argparse.ArgumentParser(description='Create a score with all the segments that satisfy the given arguments concatenated in one stave')
    parser.add_argument('csv', help='path to the csv file with the annotations of the scores')
    parser.add_argument('-t', '--title', help="title of the resulting score. If not given, the score won't be save as an xml file", default=None)
    parser.add_argument('--hd', nargs='*', help='hangdang which the search would be restricted to', default=default_hd)
    parser.add_argument('--sq', nargs='*', help='shengqiang which the search would be restricted to', default=default_sq)
    parser.add_argument('--bs', nargs='*', help='banshi which the search would be restricted to', default=default_bs)
    parser.add_argument('--ju', nargs='*', help='line type which the search would be restricted to', default=default_ju)
    args = parser.parse_args()
    
    material = jSA.collectMaterial(args.csv, hd=args.hd, sq=args.sq,
                                   bs=args.bs, ju=args.ju)
    s, m = jSP.concatenateSegments(material, title=args.title)
    
