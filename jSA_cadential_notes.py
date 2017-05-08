# -*- coding: utf-8 -*-

import jingjuScoreAnalysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']

    parser = argparse.ArgumentParser(description='Plot a bar chart with the percentage of cadential notes for each section of the opening and closing lines in the scores that match the given search criteria')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('file', help='Path and name for file to be saved, including extension')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to either erhuang or xipi')
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
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
    
if 'erhuang' in args.shengqiang:
    material_s1 = jSA.collectJudouMaterial(linesData, args.hangdang,
                                           sq=args.shengqiang, bs=args.banshi,
                                           ju=['s1'])
    material_s2 = jSA.collectJudouMaterial(linesData, args.hangdang,
                                           sq=args.shengqiang, bs=args.banshi,
                                           ju=['s2'])
    material_x = jSA.collectJudouMaterial(linesData, args.hangdang,
                                          sq=args.shengqiang, bs=args.banshi,
                                          ju=['x'])
    judouMaterialList = [material_s1, material_s2, material_x]
    
elif 'xipi' in args.shengqiang:
    material_s = jSA.collectJudouMaterial(linesData, args.hangdang,
                                          sq=args.shengqiang, bs=args.banshi,
                                          ju=['s'])
    material_x = jSA.collectJudouMaterial(linesData,  args.hangdang,
                                          sq=args.shengqiang, bs=args.banshi,
                                          ju=['x'])
    judouMaterialList = [material_s, material_x]

jSA.cadentialNotes(judouMaterialList, filename=args.file,
                   includeGraceNotes=gn)