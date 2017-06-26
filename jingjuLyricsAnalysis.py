# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 10:47:11 2017

@author: Rafael.Ctt
"""

from music21 import *
import jingjuScoreAnalysis as jSA



def countLineType(linesData, hd=['laosheng', 'dan'], sq=['erhuang',
                        'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                        'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                        'kuaiban'], ju = ['s', 's1', 's2', 'x']):
    '''str, [str], [str], [str], [str] --> [{str:list}, [str,[[{str:str},str]]]
   
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a list with the
    lyrics from the lines that meet the search criteria. The lyrics are given
    per line and per each judou.

    If any of the four search concepts is indifferent, don't input it in when
    calling the function, so that it will retrive all the instances. For
    example, if a search does not care about the banshi, just don't specify the
    banshi list, so that it will retrieve the lines from all the banshi that
    meet the other criteria.

    The first element of the returned list is a dictionary of all the search
    criteria for which lines have been found (no all the combinations of the
    given search criteria might retrieve results). The keys of the dictionary
    are 'hd', 'sq', 'bs', and 'ju'.
    
    Afther this, the list contain a list for each score in which a line meeting
    the search criteria has been found. The first item of the list is the path
    to the score, and then a list for each of the parts of the score. Each of
    these part-lists cotains a list for each line that meets the search
    criteria. These line-lists contain a dictionary with the lyrics for the
    line and each judou. Keys are 'line', 'jd1', 'jd2', and 'jd3'. After the
    dictionary, the line-list contains a string with the structure of the line:
    the total number of syllables and the syllables for each judou (e.g.
    '10:3+3+4').
    
    Finally, the returned list contains a list with the count of line types.
    Each line type is given in a tuple containing a string with the line tipe,
    an integer with the total count, and a float with the percentage of that
    count for the total of lines retrieved.
    '''

    # Get the path of the folder shared by the linesData file and the xml
    # scores
    path = linesData[:linesData.rfind('/')+1]
    
    with open(linesData, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    material = []

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
    material.append(searchInfo)
    
    # Count line structure types
    str_types = {}
    
    # Segments collection
    for row in data:
        strInfo = row.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in row: continue
    
        if (score == '') and ('Part' in row):
            material[-1].append([])
            continue
        
        # Get the information to check the search criteria
        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]
        
        # Get the lyrics from the line and each judou
        line = strInfo[5]
        ll = countCharacters(line)
        jd1 = strInfo[9]
        jd1l = countCharacters(jd1)
        jd2 = strInfo[12]
        jd2l = countCharacters(jd2)
        jd3 = strInfo[15]
        jd3l = countCharacters(jd3)
        
        # Define the line type as a string
        line_structure = str(ll)+':'+str(jd1l)+'+'+str(jd2l)+'+'+str(jd3l)
        
        # Check if the length of the line is equal to the sum of the judou
        if ll != jd1l + jd2l + jd3l:
            print(line, 'is not equal to', jd1, '+', jd2, '+', jd3)
        
        # Check if the search criteria are met
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            
            material[-1][-1].append([{'line':line, 'jd1':jd1, 'jd2':jd2,
                                     'jd3':jd3}, line_structure])
            
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)
            
            str_types[line_structure] = str_types.get(line_structure, 0) + 1
            
    # Delete empty lists
    score2remove = []
    for i in range(1, len(material)):
        score = material[i]
        partsLength = 0
        for j in range(1, len(score)):
            part = score[j]
            partsLength += len(part)
        if partsLength == 0:
            score2remove.insert(0, i)
    if len(score2remove) != 0:
        for l in score2remove:
            material.pop(l)
            
    sort_count = sorted(str_types.items(),key=lambda x: x[1],reverse=True)
    
    total = 0
    for i in sort_count:
        total += i[-1]
        
    final_count = []
    for i in sort_count:
        percent = round(i[-1] / (total / 100), 2)
        final_count.append((i[0], i[1], percent))
    
    material.append(final_count)

    print('All material collected')

    return material



def collectTonesMaterial(linesData, hd=['laosheng', 'dan'], sq=['erhuang',
                         'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                         'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                         'kuaiban'], ju = ['s', 's1', 's2', 'x']):

    '''str, [str], [str], [str], [str] --> [{str:list}, ______________
   
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns 
    
    
    
    
    
    '''

    # Get the path of the folder shared by the linesData file and the xml
    # scores
    path = linesData[:linesData.rfind('/')+1]
    
    with open(linesData, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    material = []

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
    material.append(searchInfo)
    
    # Segments collection
    for row in data:
        strInfo = row.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in row: continue
    
        if (score == '') and ('Part' in row):
            material[-1].append([])
            continue
        
        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]
        
        # Get the information to store in material
        line = strInfo[5]
        start = jSA.floatOrFraction(strInfo[6])
        end = jSA.floatOrFraction(strInfo[7])
        tones = strInfo[8]
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            material[-1][-1].append([line, start, end, tones])
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)
            
    # Delete empty lists
    score2remove = []
    for i in range(1, len(material)):
        score = material[i]
        partsLength = 0
        for j in range(1, len(score)):
            part = score[j]
            partsLength += len(part)
        if partsLength == 0:
            score2remove.insert(0, i)
    if len(score2remove) != 0:
        for l in score2remove:
            material.pop(l)

    print('All material collected')

    return material



def tonesPerJudou(linesData, hd=['laosheng', 'dan'], sq=['erhuang', 'xipi'],
                  bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
                  'yuanban', 'erliu', 'liushui', 'kuaiban'],
                  ju = ['s', 's1', 's2', 'x']):

    '''str, [str], [str], [str], [str] --> [{str:list}, ______________
   
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns 
    
    
    
    
    
    '''

    # Get the path of the folder shared by the linesData file and the xml
    # scores
    path = linesData[:linesData.rfind('/')+1]
    
    with open(linesData, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    material = []

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
    material.append(searchInfo)
    
    # Segments collection
    for row in data:
        strInfo = row.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in row: continue
    
        if (score == '') and ('Part' in row):
            material[-1].append([])
            continue
        
        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]
        
        # Get the information to store in material
        tones = strInfo[8]
        jd1 = strInfo[9]
        jd1tones = tones[0:countCharacters(jd1)]
        jd1start = jSA.floatOrFraction(strInfo[10])
        jd1end = jSA.floatOrFraction(strInfo[11])
        jd2 = strInfo[12]
        jd2tones = tones[countCharacters(jd1):
                         countCharacters(jd1)+countCharacters(jd2)]
        jd2start = jSA.floatOrFraction(strInfo[13])
        jd2end = jSA.floatOrFraction(strInfo[14])
        jd3 = strInfo[15]
        jd3tones = tones[countCharacters(jd1)+countCharacters(jd2):]
        jd3start = jSA.floatOrFraction(strInfo[16])
        jd3end = jSA.floatOrFraction(strInfo[17])
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            if len(jd1) > 0:
                material[-1][-1].append([jd1, jd1start, jd1end, jd1tones])
            if len(jd2) > 0:
                material[-1][-1].append([jd2, jd2start, jd2end, jd2tones])
            if len(jd3) > 0:
                material[-1][-1].append([jd3, jd3start, jd3end, jd3tones])
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)
            
    # Delete empty lists
    score2remove = []
    for i in range(1, len(material)):
        score = material[i]
        partsLength = 0
        for j in range(1, len(score)):
            part = score[j]
            partsLength += len(part)
        if partsLength == 0:
            score2remove.insert(0, i)
    if len(score2remove) != 0:
        for l in score2remove:
            material.pop(l)

    print('All material collected')

    return material



def toneContour(material, countGraceNotes=True, query=[]):
    '''list --> dict
    
    It takes the list returned by the collectTonesMaterial function, and
    returns
    '''
    
    contours = {'1':{}, '2':{}, '3':{}, '4':{}}
    temp = []
    
    for score in material[1:]:
        # Loading the score to get the parts list
        temp.append([])
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = jSA.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            
            for line in score[partIndex]:
                temp[-1].append([])
                lyrics = line[0]
                start = line[1]
                end = line[2]
                tones = line[3]
#                print(tones)
                
                lyrIndex = 0
                toneJump = 0
                
                syl = []
                graceNotes = [] # Store grace notes to be added to a note with
                                # lyrics
                inBrackets = False # Flag to check if the lyrics syllabe is
                                   # within a bracket
                toRed = [] # Stores indexes of the notes to show in red
                showSegment = False # True if a search has been found in this
                                    # segment
                
                segment = notes.getElementsByOffset(start, end)
                
                for i in range(len(segment)):
                    n = segment[i]
                    if n.isRest:
                        syl += graceNotes
                    elif n.hasLyrics():
                        char = n.lyric
                        currentChar = lyrics[lyrIndex:lyrIndex+len(char)]
                        # Check that the lyric in the score and the one from
                        # the annotations coincide
                        if char != currentChar:
                            print('Problem with', char)
                            segment.show()
                        
                        if ('（' in char) and ('）' not in char):
                            inBrackets = True
                            syl.append(n.pitch.midi)
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        elif inBrackets == True:
                            syl.append(n.pitch.midi)
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        elif '）' in char:
                            inBrackets = False
                            syl.append(n.pitch.midi)
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        else:
                            # First, solve the accumulated pitches in syl from
                            # the previous syllable
                            if len(syl) > 0:
                                contour = defineContour(syl)
                                if (len(query)>0 and contour==query[1]
                                    and len(toRed)>0):
                                    for n2r in toRed:
                                        segment[n2r].color = 'red'
                                    showSegment = True
                                temp[-1][-1][-1].append(contour)
                                temp[-1][-1][-1].append(syl)
                                if currentTone != '5':
                                    c = contours[currentTone]
                                    c[contour] = c.get(contour, 0) + 1
                            currentTone = tones[lyrIndex-toneJump]
                            toRed=[]
                            if len(query)>0 and currentTone == query[0]:
                                toRed.append(i)
                                preGrace = 1
                                while (i-preGrace >= 0 and
                                       segment[i-preGrace].quarterLength==0):
                                    toRed.append(i-preGrace)
                                    preGrace += 1
                            temp[-1][-1].append([char,currentChar,currentTone])
                            toneJump += len(char) - 1
                            syl = graceNotes + [n.pitch.midi] # Add preceding
                                                              # grace notes
                            graceNotes = [] # Grace notes buffer empty
                        lyrIndex += len(char)
                    elif n.quarterLength == 0:
                        # Store grace notes pitches while cheking other stuff
                        buffer = [n.pitch.midi]
                        # Check that is not preceded by other grace notes,
                        # because in that case it's already been taken care of
                        if i>0 and segment[i-1].quarterLength==0: continue
                        # If it is not the last note of the segment...
                        if i != len(segment)-1:
                            # ...check if there are more grace notes following
                            jump = 1
                            while ((i+jump<len(segment)) # is not over segment
                                   and (segment[i+jump].quarterLength==0)):
                                mid = segment[i+jump].pitch.midi
                                # Check mordent
                                if (i+jump < len(segment)-1 # not the last note
                                    and not segment[i+jump-1].isRest
                                    and not segment[i+jump+1].isRest):
                                    preMid = segment[i+jump-1].pitch.midi
                                    postMid = segment[i+jump+1].pitch.midi
                                    if preMid == postMid: # it's mordent, then
                                        jump += 1
                                    else:
                                        buffer.append(mid)
                                        jump += 1
                                else: # it is the last note
                                    buffer.append(mid)
                                    jump += 1
                            # There are not more grace notes following
                            # Check if the grace notes are at the end
                            if (i+jump >= len(segment)
                                  or segment[i+jump].isRest):
                                syl += buffer
                                if len(toRed)>0: toRed.append(i)
                            # If not, check if the next note has lyrics
                            elif segment[i+jump].hasLyrics():
                                if '（' in segment[i+jump].lyric or inBrackets:
                                    syl += buffer
                                    if len(toRed)>0: toRed.append(i)
                                else:
                                    graceNotes = buffer
                            # If not, check if it is a mordent
                            elif (not segment[i-1].isRest and
                                  segment[i-1].pitch.midi ==
                                  segment[i+jump].pitch.midi):
                                if len(toRed)>0: toRed.append(i)
                            # If not, it is just a note's grace note(s)
                            else:
                                syl += buffer
                                if len(toRed)>0: toRed.append(i)
                        else: # it is the last note of the segment
                            syl.append(n.pitch.midi)
                            if len(toRed)>0: toRed.append(i)
                    else: # A note without lyrics
                        # Check if it could be a mordent
                        # So, check if it's not the last and has a shorter
                        # duration than a quaver
                        mid = n.pitch.midi
                        if (i<len(segment)-1 and n.quarterLength<0.5
                            and not segment[i-1].isRest):
                            premid = segment[i-1].pitch.midi
                            if (not segment[i+1].hasLyrics()
                                and not segment[i+1].isRest):
                                postmid = segment[i+1].pitch.midi
                                if mid != premid and premid == postmid:
                                    if len(toRed)>0: toRed.append(i)
                                else:
                                    syl.append(mid)
                                    if len(toRed)>0: toRed.append(i)
                            else:
                                syl.append(mid)
                                if len(toRed)>0: toRed.append(i)
                        else:
                            syl.append(mid)
                            if len(toRed)>0: toRed.append(i)
                
                temp[-1][-1][-1].append(defineContour(syl))
                temp[-1][-1][-1].append(syl)
#                for i in temp[-1][-1]:
#                    print(i)

                if showSegment: segment.show()
                    
    for i in range(1, 5):
        print(i, sorted(contours[str(i)].items(), key=lambda x:x[1],
                        reverse=True))

    return temp, contours



def tonePair(material, comparisonPoint=[1, 0], query=[]):
    '''list --> dict
    
    It takes the list returned by the tonePair function, and returns

    comparisonPoint:
        0: first note
        1: last note
        
    query has include first the tones pair, in the form '1-2' for first tone
    followed by a second tone, and then the shape; for example: ['1-2', 'A']
    '''
    
    pairs = {'1-1':{}, '1-2':{}, '1-3':{}, '1-4':{}, '1-5':{},
             '2-1':{}, '2-2':{}, '2-3':{}, '2-4':{}, '2-5':{},
             '3-1':{}, '3-2':{}, '3-3':{}, '3-4':{}, '3-5':{},
             '4-1':{}, '4-2':{}, '4-3':{}, '4-4':{}, '4-5':{},
             '5-1':{}, '5-2':{}, '5-3':{}, '5-4':{}, '5-5':{}}
    dous = []
    
    for score in material[1:]:
        s = []
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = jSA.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            p = []
            if len(score[partIndex]) > 0:
                # Get the notes from the current part
                part = parts[partIndex-1]
                notes = part.flat.notes.stream()
                
                for line in score[partIndex]:
                    lyrics = line[0]
                    start = line[1]
                    end = line[2]
                    tones = line[3]
                    
                    lyrIndex = 0
                    toneJump = 0
                    
                    dou = []
    
                    inBrackets = False # Flag to check if the lyrics syllabe is
                                       # within a bracket
                    
                    segment = notes.getElementsByOffset(start, end)
                    
                    for i in range(len(segment)):
                        n = segment[i]
                        if n.quarterLength == 0: continue
                        elif n.hasLyrics():
                            char = n.lyric
                            currentChar = lyrics[lyrIndex:lyrIndex+len(char)]
                            # Check that the lyric in the score and the one
                            # from the annotations coincide
                            if char != currentChar:
                                print('Problem with', char)
                                segment.show()
                            
                            if ('（' in char) and ('）' not in char):
                                toneJump += len(char)
                                inBrackets = True
                            elif inBrackets == True:
                                toneJump += len(char)
                            elif '）' in char:
                                toneJump += len(char)
                                inBrackets = False
                            else:
                                currentTone = tones[lyrIndex-toneJump]
                                if len(dou) > 0:
                                    jump = 1
                                    while segment[i-jump].quarterLength == 0:
                                        jump += 1
                                    last = segment[i-jump].pitch.midi
                                    dou[-1].append(last)
                                first = n.pitch.midi
                                dou.append([currentChar, currentTone,
                                                   first])
                                toneJump += len(char) - 1
                            lyrIndex += len(char)
                    jump = 0
                    while segment[i-jump].quarterLength == 0:
                        jump += 1
                    last = segment[i-jump].pitch.midi
                    dou[-1].append(last)
                    p.append(dou)
            s.append(p)    
        dous.append(s)
        
    queryMessage = True

    for s in range(len(dous)):
        score = dous[s]
        for p in range(len(score)):
            part = score[p]
            for d in range(len(part)):
                dou = part[d]
                for i in range(len(dou)-1):
                    syl1 = dou[i]
                    syl2 = dou[i+1]
                    pair = syl1[1] + '-' + syl2[1]
                    note1 = syl1[comparisonPoint[0]+2]
                    note2 = syl2[comparisonPoint[1]+2]
                    if note1 > note2:
                        shape = 'D'
                    elif note1 == note2:
                        shape = 'F'
                    elif note1 < note2:
                        shape = 'A'
                    pairs[pair][shape] = pairs[pair].get(shape, 0) + 1
                    
                    if len(query) > 0:
                        if query[0] == pair and query[1] == shape:
                            if queryMessage:
                                print('\nRetrieving found queries')
                                queryMessage = False
                            scorePath = material[s+1][0]
                            loadedScore = converter.parse(scorePath)
                            print(scorePath.split('/')[-1], 'loaded')
                            parts = jSA.findVoiceParts(loadedScore)
                            parte = parts[p]
                            notes = parte.flat.notesAndRests.stream()
                            segmentInfo = material[s+1][p+1][d]
                            print(segmentInfo[0], segmentInfo[-1])
                            start = segmentInfo[1]
                            end = segmentInfo[2]
                            segment = notes.getElementsByOffset(start, end)
                            segment.show()                            

    return dous, pairs



def defineContour(pitches):
    '''
    [int] --> str
    
    I takes a list of midi pitches and returns a string defining the melodic
    contour
    A : ascending
    D : descending
    F : flat
    '''
    
    if len(pitches) == 1:
        contour = 'dF'
        
    elif len(pitches) == 2:
        if pitches[0] > pitches[1]:
            contour = 'D'
        elif pitches[0] == pitches[1]:
            contour = 'F'
        elif pitches[0] < pitches[1]:
            contour = 'A'

    elif len(pitches) > 2:
        first = pitches[0]
        last = pitches[-1]
        if first > last:
            contour = 'D'
        elif first == last:
            contour = 'F'
        elif first < last:
            contour = 'A'
        midPitches = pitches[1:-1]
        h = max(midPitches) # Highest pitch
        l = min(midPitches) # Lowest pitch
        if contour == 'D':
            if (first >= h >= last) and (first >= l >= last):
                contour = 'D'
            elif (h > first) and (l > last):
                contour = 'AD'
            elif (first > h) and (last > l):
                contour = 'DA'
            else:
                if h-first > last-l:
                    contour = 'AD'
                elif h-first < last-l:
                    contour = 'DA'
                else:
                    contour = 'D'
        elif contour == 'A':
            if (first <= h <= last) and (first <= l <= last):
                contour = 'A'
            elif (h > last) and (l > first):
                contour = 'AD'
            elif (last > h) and (first > l):
                contour = 'DA'
            else:
                if first-l > h-last:
                    contour = 'DA'
                elif first-l < h-last:
                    contour = 'AD'
                else:
                    contour = 'A'
        elif contour == 'F':
            if h-first > first-l:
                contour = 'AD'
            elif first == h == l:
                contour = 'F'
            else:
                contour = 'DA'

    else:
        print('Invalid sequence of pitches. Possibly empty list.')          
    
    return contour



diacritics = ['，', '。', '？', '！', '；', '：', '、']

def countCharacters(str):
    '''str --> int
    
    Given a string from jingju lyrics it counts the characters that are not
    diacritics and are not in brackets
    '''
    
    length = 0
    inBrackets = False
    
    for c in str:
        if c in diacritics: continue
        elif c == '（':
            inBrackets = True
        elif c == '）':
            inBrackets = False
        else:
            if inBrackets: continue
            length += 1
    
    return length