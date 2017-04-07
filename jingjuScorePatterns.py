# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:32:36 2017

@author: Rafael.Ctt
"""

import copy
import jingjuScoreAnalysis as jSA
from music21 import *

def concatenateSegments(material, title=None):
    '''list --> music21.stream.Stream, list
    It takes the list returned by the collectMaterial function, and returns
    music21.stream.Stream with all the segments conatined in the material list
    concatenated into a single stave. It also returns the material list with a
    new list appended with the information to reconstruct the segments in their
    original scores from the new concatenated score. This new list contain a
    list of integers indicating:
    [start, end, score, part, segment]
    So that,
    - start: indicates the starting offset of a segment in the concatenated
             score
    - end: indicates the ending offset of a segment in the concatenated score
    - score: indicates the index in the material list of the score from where
             the original segment came from
    - part: indicates the index of the part in the previous score
    - segment: indicates the index of the segment as stored for the previous
               part in the material list
    If a title is given, it generates an xml file with the concatenated score
    and a pickle file with the material list
    '''

    # Gather search info to name the concatenated score
    searchString = ''
    searchInfo = material[0]
    # Add hangdang info
    hd = searchInfo['hd']
    if len(hd) != 2:
        for e in hd:
            searchString += e + '/'
        searchString = searchString[:-1] + ', '
    # Add shengqiang info
    sq = searchInfo['sq']
    if len(sq) != 2:
        for e in sq:
            searchString += e + '/'
        searchString = searchString[:-1] + ', '
    # Add banshi info
    bs = searchInfo['bs']
    if len(bs) != 8:
        for e in bs:
            searchString += e + '/'
        searchString = searchString[:-1] + ', '
    # Add ju info
    ju = searchInfo['ju']
    if len(ju) != 4:
        for e in ju:
            searchString += e + '/'
        searchString = searchString[:-1]

    concatenatedScore = stream.Stream()
    concatenatedSegments = []
    
    accumulatedOffset = 0
    
    for scoreIndex in range(1, len(material)):
        score = material[scoreIndex]
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = jS.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            
            # Find segments to analyze in the current part
            for segmentIndex in range(len(score[partIndex])):
                startEnd = score[partIndex][segmentIndex]
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Reassigning offsets
                newSegment = [accumulatedOffset]
                startingOffset = segment[0].offset
                endingOffset = segment[-1].offset
                for n in segment:
                    n.offset += -startingOffset + accumulatedOffset
                    concatenatedScore.append(n)
                accumulatedOffset += (endingOffset - startingOffset)
                newSegment.append(accumulatedOffset)
                newSegment.extend([scoreIndex, partIndex, segmentIndex])
                accumulatedOffset += segment[-1].quarterLength
                concatenatedSegments.append(newSegment)
                
    extendedMaterial = copy.deepcopy(material)
    extendedMaterial.append(concatenatedSegments)
    
    # Check that the newSegments are equally long to the original segments:
    for newSegment in material[-1]:
        newSegmentStart = newSegment[0]
        newSegmentEnd = newSegment[1]
        length1 = newSegmentEnd - newSegmentStart
        score = newSegment[2]
        part = newSegment[3]
        segment = newSegment[4]
        originalSegment = material[score][part][segment]
        originalSegmentStart = originalSegment[0]
        originalSegmentEnd = originalSegment[1]
        length2 = originalSegmentEnd - originalSegmentStart
        if length1 != length2:
            print('Possible error with '+material[score][0]+', part '+str(part)
                  +', segment '+str(material[score][part][segment])+
                  ', and the new segment '+str(newSegment[:2]))
    
    if title != None:
        print('Segments concatenated\nCreating files')
        concatenatedScore.write(fp=title+'.xml')
        with open(title+'.pkl', 'wb') as f:
            pickle.dump(material, f, protocol=2)
    
    print('Done!')
    
    return concatenatedScore, material
    
def plotPatterns(resultsFile, concatenatedScore):#, extendedMaterial):
    '''str, str, str --> dic
    {str:{str:[[float, float]]}}
    '''
    with open(resultsFile, 'r') as f:
        data = f.readlines()
    
    patterns = {}
    
    # Storing the patterns in the text file into a dictionary
    for l in data:
        line = l.strip()
        if len(line) == 0: continue
        if 'pattern' in line:
            pattern = line
            patterns[pattern] = {}
        elif 'occurrence' in line:
            occurrence = line
            patterns[pattern][occurrence] = []
        else:
            pos = float(line.split(', ')[0])
            mid = float(line.split(', ')[1])
            patterns[pattern][occurrence].append([pos, mid])
            
    # Order notes in each pattern occurrence by time position
    for pat in patterns.keys():
        for occ in patterns[pat]:
            patterns[pat][occ] = sorted(patterns[pat][occ])
            
    p = patterns['pattern1']['occurrence1']
    
    # Find patterns in the concatenated score
    score = converter.parse(concatenatedScore)
    notes = score.flat.notes.stream()
    
    for i in range(len(notes)):
        if notes[i].quarterLength == 0: continue
        mid = notes[i].pitch.midi
        match = False
        if mid == p[0][1]:
            print('\n')
            print(mid, p[0][1])
            match = True
            j = 1
            while j < len(p):
                mid1 = notes[i+j].pitch.midi
                mid2 = p[j][1]
                print(mid1, mid2)
                if mid1 == mid2:
                    j += 1
                else:
                    match = False
                    break
        if match == True:
            for k in range(len(p)):
                print(notes[i+k].offset, p[k][0])
            break
                
    
    return patterns