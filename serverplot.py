# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:37:52 2017

@author: Rafael.Ctt
"""

import jingjuScores as jS
import jingjuScoreAnalysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']
    
    parser = argparse.ArgumentParser(description='Create a concatenated score')
    parser.add_argument('csvfile', help='the csv file with the scores info')
    parser.add_argument('--hd', nargs='*', help='hangdang', default=default_hd)
    parser.add_argument('--sq', nargs='*', help='shengqiang', default=default_sq)
    parser.add_argument('--bs', nargs='*', help='banshi', default=default_bs)
    parser.add_argument('--ju', nargs='*', help='ju', default=default_ju)
    args = parser.parse_args()
    
    material = jSA.collectMaterial(args.csvfile, hd=args.hd, sq=args.sq,
                                   bs=args.bs, ju=args.ju)
    s, m = jSA.concatenateSegments(material, title='prueba')
    
