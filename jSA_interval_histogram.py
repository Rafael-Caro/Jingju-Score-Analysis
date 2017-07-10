# -*- coding: utf-8 -*-

import jingju_singing_analysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']

    parser = argparse.ArgumentParser(description='Plot a interval histogram from the scores that match the given search criteria. If none given, the whole collection is used')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('file', help='Path and name for file to be saved, including extension')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to the given shengqiang. Erhuang and xipi given by default', default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-l', '--line', nargs='*', help='Restrict the search to the given shengqiang. S1, s2, s and x given by default', default=default_ju)
    parser.add_argument('-c', '--count', help='Set the normalisation mode: sum to normalise to the summation, max to normalise to the maximun value, abs to not normalise. Sum given by default', default='sum')
    parser.add_argument('-di', '--directed', help='Set if the direction of the interval should be considered. Take True or False. Set False by default', default='False')
    parser.add_argument('-s', '--silence', help='Set a threshold of quarter note duration to count the interval between two notes separated by a rest note of equal or less duration than the threshold', default=0.25)
    parser.add_argument('-gn', '--graceNotes', help='Set if grace notes should be counted. Take True or False. Set True by default', default='True')
    
    args = parser.parse_args()
    
    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'
    
    di = args.directed
    if di == 'True':
        di = True
    elif di == 'False':
        di = False
    
    gn = args.graceNotes
    if gn == 'True':
        gn = True
    elif gn == 'False':
        gn = False
    
    material = jSA.collectLineMaterial(linesData, hd=args.hangdang,
                                       sq=args.shengqiang, bs=args.banshi,
                                       ju=args.line)
    intHist = jSA.intervalHistogram(material, filename=args.file,
                                    count=args.count,
                                    directedInterval=di,
                                    silence2ignore=float(args.silence),
                                    ignoreGraceNotes=gn)

