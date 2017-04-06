# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 13:57:50 2017

@author: Rafael.Ctt
"""
import numpy as np
import matplotlib.pyplot as plt
from music21 import *
import jingjuScores as jS
import fractions
import pickle

### TO DELETE?
#f = 'scores/lsxp-LiangGuoJiao-ShiJieTing-1.xml'
#s = converter.parse(f)
#part = jS.findVoiceParts(s)[0]

def plotting(xPositions, xLabels, yValues, searchInfo, width=0.8):
    # Determing the handang and shengqiang present
    hdInfo = searchInfo['hd']
    sqInfo = searchInfo['sq']
    # Hangdang information
    if len(hdInfo) == 2:
        hd = 'sd'
    else:
        if hdInfo[0] == 'laosheng':
            hd = 'ls'
        elif hdInfo[0] == 'dan':
            hd = 'da'
    # Shengqiang information
    if len(sqInfo) == 2:
        sq = 'ex'
    else:
        if sqInfo[0] == 'erhuang':
            sq = 'eh'
        elif sqInfo[0] == 'xipi':
            sq = 'xp'
    
    # Color, hatch and limits codes
    col = {'ls':'#66CCFF', 'da':'#FF9966', 'sd':'#B2B2B2'}
    h = {'eh':'/', 'xp':'\\', 'ex':'x'} # hatch for the bars
    limX = {'ls':(54, 77), 'da':(59, 86), 'sd':(54,86)}

    plt.figure()
    plt.bar(xPositions, yValues, width, linewidth=0, zorder=1,
            color = col[hd],
            hatch = h[sq])
    plt.axvline(x=64+width/2, color='red', zorder=0) # Tonic line
    plt.axvline(x=76+width/2, color='red', ls='--', zorder=0) # High 8ve tonic
    plt.axvline(x=59+width/2, color='gray', ls=':', zorder=0) # Fifth    
    plt.axvline(x=71+width/2, color='gray', ls=':', zorder=0) # Fifth
    plt.axvline(x=83+width/2, color='gray', ls=':', zorder=0) # Fifth
    for yValue in yValues:
        plt.axhline(y=yValue, color='gray', ls=':', zorder=0)
    plt.xticks(xPositions + width/2, xLabels, rotation=90)
    plt.xlim(limX[hd][0], limX[hd][1])
    plt.ylim(0, 0.3)
    plt.tight_layout()
    print('Done!')
    plt.show()

def collectMaterial(lyricsData, hd=['laosheng', 'dan'], sq=['erhuang', 'xipi'],
                    bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
                    'yuanban', 'erliu', 'liushui', 'kuaiban'], ju = ['s', 's1',
                    's2', 'x']):
    '''str, [str], [str], [str], [str] --> [[str][str,[[float]]]]
   
    Given the path of the lyricsData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a list with the
    score segments that correspond to the lines that meet that criteria, plus a
    plotting rubric.

    If any of the four search concepts is indifferent, don't input it in when
    calling the function, so that it will retrive all the instances. For
    example, if a search does not care about the banshi, just don't specify the
    banshi list, so that it will retrieve the lines from all the banshi that
    meet the other criteria.

    In the returned list, the first element is the plotting rubric, a list of
    two strings, indicating the hangdang and shengqiang used in the search. It
    will be used in the plotting function to determine color, xlim and hatch.
    
    The remaining elements are score lists, with the following format:
    [pathToScore,
     [[float, float],  # starting and ending offset of one segment
      [float, float],
      [float, float]], # first part
     [[float, float],
      [float, float],
      [float, float]]  # second part
    ]

    For scores with multiple parts, if any of the parts doesn't have any line
    that meets the searching criteria, the part will be store in the score list
    as an empty list and in the corresponding order. For example:
    [pathToScore,
     [],               # first part
     [[float, float],
      [float, float],
      [float, float]]  # second part
    ]
    '''

    # Get the path of the folder shared by the lyricsData file and the xml
    # scores
    path = lyricsData[:lyricsData.rfind('/')+1]
    
    with open(lyricsData, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    material = []

    # Search information
    searchInfo = {'hd':hd, 'sq':sq, 'bs':bs, 'ju':ju}
    material.append(searchInfo)
    
    # Segments collection
    for line in data:
        strInfo = line.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in line: continue
    
        if (score == '') and ('Part' in line):
            material[-1].append([])
            continue
        
        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]
        
        # Get the starting and ending points of the line as floats or fractions
        start = floatOrFraction(strInfo[6])
        end = floatOrFraction(strInfo[7])
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            material[-1][-1].append([start, end])
            
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



def pitchHistogram(material, count='sum', countGraceNotes=True):
    '''list --> dict, bar plot
    
    It takes the list returned by the collectMaterial function, and returns a
    dictionary with all the existing pitches' nameWithOctave as keys and its
    aggregated duration in quarterLengths as values.
    
    For the bar diagram to be plotted, the values can be normalised according
    to count:
    - if count=='sum', they are normalised to their summation,
    - if count=='max', they are normalised to their maximun value
    - if count=='abs', they are not normalised, but absolute values given
    
    If countGraceNotes==True, the grace notes will be counted with a duration
    value equivalent to the minimum one present in the analysed segments, but
    with a maximum value of 0.25. If countGraceNotes==False, grace notes will
    be ignored and not counted.
    '''
    
    pitchCount = {}
    
    for score in material[1:]:
        # Loading the score to get the parts list
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
            notes = part.flat.notes.stream()
    
            # Set the duration of grace notes if needed
            if countGraceNotes:
                minDur = 0.25
                for n in notes:
                    noteDur = n.quarterLength
                    if noteDur!=0 and noteDur<minDur:
                        minDur = noteDur
    
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Count pitches in the current segment
                for n in segment:
                    noteName = n.nameWithOctave
                    noteDur = n.quarterLength
                    if noteDur == 0:
                        if not countGraceNotes: continue
                        noteDur = minDur
                    pitchCount[noteName] = pitchCount.get(noteName, 0) + noteDur
    
    # Sorting duration per pitch class frequency
    pitches = pitchCount.keys()
    toSort = {p:pitch.Pitch(p).midi for p in pitches}
    sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
    xPositions = np.array([p[1] for p in sortedPitches])
    xLabels = [p[0] for p in sortedPitches]
    yValues = np.array([pitchCount[l] for l in xLabels])
    
    # Normalising, if requested
    if count == 'sum':
        yValues = yValues / float(sum(yValues))
        yLabel = 'Normalized Count'
    elif count == 'max':
        yValues = yValues / float(max(yValues))
        yLabel = 'Normalized Count'
    else:
        yLabel = 'Count'
        
    print('Plotting...')

    plotting(xPositions, xLabels, yValues, material[0])



def getAmbitus(material):
    '''list --> music21.interval.Interval
    
    It takes the list returned by the collectMaterial function, and returns an
    interval from the lowest note found to the highest note found.
    '''
    
    ambitusStart = None
    ambitusEnd = None
    
    for score in material:
        # Loading the score to get the parts list
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
            notes = part.flat.notes.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                segmentAmbitus = segment.analyze('ambitus')
                if ambitusStart==None and ambitusEnd==None:
                    ambitusStart = segmentAmbitus.noteStart
                    ambitusEnd = segmentAmbitus.noteEnd
                else:
                    if segmentAmbitus.noteStart.midi < ambitusStart.midi:
                        ambitusStart = segmentAmbitus.noteStart
                    if segmentAmbitus.noteEnd.midi > ambitusEnd.midi:
                        ambitusEnd = segmentAmbitus.noteEnd

    ambitusInterval = interval.Interval(ambitusStart, ambitusEnd)

    print('Ambitus:', ambitusInterval.niceName + ', from',
          ambitusStart.nameWithOctave, 'to', ambitusEnd.nameWithOctave)

    return ambitusInterval



def findScore(material, thresholdPitch, lowHigh):
    '''list, int, str --> [music21.stream.Score]
    It takes the list returned by the collectMaterial function, a pitch midi
    value, and the string "low" or "high" to look for those scores that contain
    pitchs lower or higher than the given threshold.
    '''
    
    scores = []    

    for score in material:
        # Loading the score to get the parts list
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
            notes = part.flat.notes.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                ###############################################################
                ## Change here so that it returns scores with the notes      ##
                ## beyond the threshold colored in red.                      ##
                ###############################################################
                segmentAmbitus = segment.analyze('ambitus')
                ambitusStart = segmentAmbitus.noteStart.midi
                ambitusEnd = segmentAmbitus.noteEnd.midi
                if lowHigh == 'low':
                    if ambitusStart < pitch.Pitch(thresholdPitch).midi:
                        if scoreName not in scores:
                            scores.append(scoreName)
                if lowHigh == 'high':
                    if ambitusEnd > pitch.Pitch(thresholdPitch).midi:
                        if scoreName not in scores:
                            scores.append(scoreName)

    print('Done!')

    return scores

def getTones(lyricsData, hd=['laosheng', 'dan'], sq=['erhuang', 'xipi'],
                    bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
                    'yuanban', 'erliu', 'liushui', 'kuaiban'], ju = ['s', 's1',
                    's2', 'x']):
    '''str, [str], [str], [str], [str] --> str
    Given the path of the lyricsData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a string with the
    score name and intercalated lyrics and tones for the lines found.
    '''
    with open(lyricsData, 'r', encoding='utf-8') as f:
        data = f.readlines()
        
    tones = ''
    
    diacritics = ['，', '。', '？', '！', '；', '：', '、']
    
    # Line finding
    for line in data:
        strInfo = line.strip().split(',')
        score = strInfo[0]
        if score != '':
            scoreName = score
            scoreInTones = False
    
        if 'Part' in line: continue
        
        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]
        
        lineLyrics = strInfo[5]
        lineTones = strInfo[8]
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            # Intercalate lyrics and tones
            lyricTones = ''
            jump = 0
            ignore = False
            for i in range(len(lineLyrics)):
                if lineLyrics[i] == '（':
                    lyricTones += lineLyrics[i]
                    ignore = True
                    jump += 1
                elif lineLyrics[i] == '）':
                    lyricTones += lineLyrics[i]
                    ignore = False
                    jump += 1
                elif lineLyrics[i] in diacritics:
                    lyricTones += lineLyrics[i]
                    jump += 1
                else:
                    if not ignore:
                        lyricTones += lineLyrics[i] + lineTones[i-jump]
                    else:
                        lyricTones += lineLyrics[i]
                        jump += 1
            # Add score and lyricTones to tones
            if not scoreInTones:
                tones += '\n' + scoreName+'\n'+lyricTones+'\n'
                scoreInTones = True
            else:
                tones += lyricTones+'\n'
            
    print(tones)

    return tones
    
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
                
    material.append(concatenatedSegments)
    
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
    
def floatOrFraction(strValue):
    '''str --> fractions.Fraction or float
    Given a numeric value as a string, it returns it as a fractions.Fraction
    object if contains '/' on it, or as a float otherwise
    '''
    if '/' in strValue:
        numerator = int(strValue.split('/')[0])
        denominator = int(strValue.split('/')[1])
        value = fractions.Fraction(numerator, denominator)
    else:
        value = float(strValue)
        
    return value
        
    
###############################################################################
###############################################################################
## TO IMPROVE                                                                ##
## 1. Keep the banshi information in material, so that the graceNoteDur can  ##
##    be adjusted accordingly.                                               ##
###############################################################################
###############################################################################