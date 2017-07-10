# -*- coding: utf-8 -*-

import jingju_tones_analysis as jTA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']

    parser = argparse.ArgumentParser(description='Print a table with the analysis of the pairwise relationship of the syllables from all the dou that match the given search parameters. If none given, the whole collection is used')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('relationship', type=int, nargs=2, help='Notes from the melodic contour of each syllable to be compared: 0 for the first, 1 for the last')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to the given shengqiang. Erhuang and xipi given by default', default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-l', '--line', nargs='*', help='Restrict the search to the given shengqiang. S1, s2, s and x given by default', default=default_ju)
    parser.add_argument('-fn', '--filename', help='Path to the file to save the results')
    parser.add_argument('-q', '--query', nargs=2, help='Show the score of the dou that contains pairs that satisfy the two query criteria, pair, given as tone numbers separated by hyphen, and direction; for example: 1-4 A')

    args = parser.parse_args()
    
    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'
        
    r1 = args.relationship[0]
    r2 = args.relationship[1]
    if r1 not in [0, 1] or r2 not in [0, 1]:
        raise Exception('The given values for the relationship argument are not valid')

    q = []
    if args.query != None:
        q = args.query
    
    material = jTA.toneMaterialPerJudou(linesData, hd=args.hangdang,
                                        sq=args.shengqiang, bs=args.banshi,
                                        ju=args.line)

    jTA.pairwiseRelationship(material, relationship=[r1, r2],
                             filename=args.filename, query=q)