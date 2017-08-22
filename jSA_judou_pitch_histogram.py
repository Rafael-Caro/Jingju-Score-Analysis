# -*- coding: utf-8 -*-

import jingju_singing_analysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']

    parser = argparse.ArgumentParser(description='Plot a pitch histogram from the scores that match the given search criteria. If none given, the whole collection is used')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('file', help='Path and name for file to be saved, including extension')
    parser.add_argument('line', help='Restrict the search to the given line. Choose between s1, s2, s and x.')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to the given shengqiang. Erhuang and xipi given by default', default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-n', '--norm', help='Set the normalisation mode: sum to normalise to the summation, max to normalise to the maximun value, abs to not normalise. Sum given by default', default='sum')
    parser.add_argument('-gn', '--graceNotes', help='Set if grace notes should be counted. Take True or False. Set True by default', default='True')
    
    args = parser.parse_args()
    
    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'
    
    gn = args.graceNotes
    if gn == 'True':
        gn = True
    elif gn == 'False':
        gn = False
    
    material = jSA.collectJudouMaterial(linesData, hd=args.hangdang,
                                       sq=args.shengqiang, bs=args.banshi,
                                       ju=args.line)
    pithHist = jSA.judouPitchHistogram(material, filename=args.file,
                                  norm=args.norm, countGraceNotes=gn)