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



def toneContour(material, countGraceNotes=True):
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
                print(tones)
                
                lyrIndex = 0
                toneJump = 0
                
                syl = []
                graceNotes = [] # Store grace notes to be added to a note with
                                # lyrics
                inBrackets = False
                
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
                        elif inBrackets == True:
                            syl.append(n.pitch.midi)
                            toneJump += len(char)
                        elif '）' in char:
                            inBrackets = False
                            syl.append(n.pitch.midi)
                            toneJump += len(char)
                        else:
                            currentTone = tones[lyrIndex-toneJump]
                            if len(syl) != 0: # it is not the first syllable
                                contour = defineContour(syl)
                                temp[-1][-1][-1].append(contour)
                                temp[-1][-1][-1].append(syl)
                                if currentTone != '5':
                                    c = contours[currentTone]
                                    c[contour] = c.get(contour, 0) + 1
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
                            # If not, check if the next note has lyrics
                            elif segment[i+jump].hasLyrics():
                                if '（' in segment[i+jump].lyric or inBrackets:
                                    syl += buffer
                                else:
                                    graceNotes = buffer
                            # If not, check if it is a mordent
                            elif (not segment[i-1].isRest and
                                  segment[i-1].pitch.midi ==
                                  segment[i+jump].pitch.midi):
                                pass
                            # If not, it is just a note's grace note(s)
                            else:
                                syl += buffer
                        else: # it is the last note of the segment
                            syl.append(n.pitch.midi)
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
                                    pass
                                else:
                                    syl.append(mid)
                            else:
                                syl.append(mid)
                        else:
                            syl.append(mid)
                
                temp[-1][-1][-1].append(defineContour(syl))
                temp[-1][-1][-1].append(syl)
                for i in temp[-1][-1]:
                    print(i)
#                segment.show()
                    
    for i in range(1, 5):
        print(i, sorted(contours[str(i)].items(), key=lambda x:x[1],
                        reverse=True))

    return temp, contours
    
    
    
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