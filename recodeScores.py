# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 16:32:27 2017

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
    
    parser = argparse.ArgumentParser(description='Recode the scores that satisfy the given parameters per judou')
    parser.add_argument('csv', help='path to the csv file with the annotations of the scores')
    parser.add_argument('-t', '--title', help="title of the resulting file (pickle). If not given, the score won't be save as file", default=None)
    parser.add_argument('--hd', nargs='*', help='hangdang which the search would be restricted to', default=default_hd)
    parser.add_argument('--sq', nargs='*', help='shengqiang which the search would be restricted to', default=default_sq)
    parser.add_argument('--bs', nargs='*', help='banshi which the search would be restricted to', default=default_bs)
    parser.add_argument('--ju', nargs='*', help='line type which the search would be restricted to', default=default_ju)
    parser.add_argument('-g', '--graceNoteDuration', help='duration given to grace notes', default='2.0')
    parser.add_argument('-n', '--noteName', help='note pitch can be output as pitch name or midi value', default='pitch')
    
    args = parser.parse_args()
    
    material = jSA.collectJudouMaterial(args.csv, hd=args.hd, sq=args.sq,
                                   bs=args.bs, ju=args.ju)
    s, m = jSP.recodeScore(material, title=args.title,
                           graceNoteValue=float(args.graceNoteDuration),
                           noteName=args.noteName)