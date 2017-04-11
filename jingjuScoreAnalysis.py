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

### TO DELETE?
#f = 'scores/lsxp-LiangGuoJiao-ShiJieTing-1.xml'
#s = converter.parse(f)
#part = jS.findVoiceParts(s)[0]

class ProcessException(Exception):
    pass

def plotting(xPositions, xLabels, yValues, limX=None, limY=None, yLabel=None,
             col=None, h=None, scaleGuides=False, width=0.8):

    plt.figure()
    plt.bar(xPositions, yValues, width, linewidth=0, zorder=1,
            color = col,
            hatch = h)
    if scaleGuides:
        plt.axvline(x=64+width/2, color='red', zorder=0) # Tonic line
        plt.axvline(x=76+width/2, color='red', ls='--', zorder=0) # 8ve tonic
        plt.axvline(x=59+width/2, color='gray', ls=':', zorder=0) # Fifth    
        plt.axvline(x=71+width/2, color='gray', ls=':', zorder=0) # Fifth
        plt.axvline(x=83+width/2, color='gray', ls=':', zorder=0) # Fifth
    for yValue in yValues:
        plt.axhline(y=yValue, color='gray', ls=':', zorder=0)
    plt.xticks(xPositions + width/2, xLabels, rotation=90)
    if limX != None:
        plt.xlim(limX[0]-(1-width), limX[1]+1)
    else:
        plt.xlim(xPositions[0]-(1-width), xPositions[-1]+1)
    if limY != None:
        plt.ylim(limY[0], limY[1])
    if yLabel != None:
        plt.ylabel(yLabel)
    plt.tight_layout()
    print('Done!')
    plt.show()
    
def plottingParameters(material, count, yValues):
    # Determing the handang and shengqiang present
    searchInfo = material[0]
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
    colors = {'ls':'#66CCFF', 'da':'#FF9966', 'sd':'#B2B2B2'}
    hatches = {'eh':'/', 'xp':'\\', 'ex':'x'} # hatch for the bars
    xLimits = {'ls':(54, 76), 'da':(59, 85), 'sd':(54,85)}
    
    # Setting x limits
    limX = xLimits[hd]

    # Setting y limits and y label
    limY = None
    
    # Normalising, if requested
    if count == 'sum':
        yValues = yValues / float(sum(yValues))
        yLabel = 'Normalized Count'
    elif count == 'max':
        yValues = yValues / float(max(yValues))
        yLabel = 'Normalized Count'
    else:
        yLabel = 'Count'
    
    # Setting bar color
    col = colors[hd]
    
    # Setting bar hatch
    h = hatches[sq]
    
    return yValues, limX, yLabel, col, h

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
                    pitchCount[noteName] = pitchCount.get(noteName, 0)+noteDur
    
    # Sorting duration per pitch class frequency
    pitches = pitchCount.keys()
    toSort = {p:pitch.Pitch(p).midi for p in pitches}
    sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
    xPositions = np.array([p[1] for p in sortedPitches])
    xLabels = [p[0] for p in sortedPitches]
    yValues = np.array([pitchCount[l] for l in xLabels])
    
    # Start plotting
    print('Plotting...')

    # Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)
    # Setting y limits
    limY = None
    if count == 'sum':
        limY = [0, 0.3]

    plotting(xPositions, xLabels, yValues, limX=limX, limY=limY, yLabel=yLabel,
             col=col, h=h, scaleGuides=True)

def intervalHistogram(material, count='sum', directedInterval=False,
                      silence2ignore=0.25, ignoreGraceNotes=False):
    '''list --> , bar plot
    
    It takes the list returned by the collectMaterial function, and returns
    
    For the bar diagram to be plotted, the values can be normalised according
    to count:
    - if count=='sum', they are normalised to their summation,
    - if count=='max', they are normalised to their maximun value
    - if count=='abs', they are not normalised, but absolute values given    
    '''
    
    intervalCount = {}
    
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
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Count intervals in the current segment
                # Find the last note that is not a grace note
                i = 1
                lastn = segment[-i]
                while lastn.quarterLength == 0:
                    i += 1
                    lastn = segment[-i]

                for j in range(len(segment)-i):
                    n1 = segment[j]
                    if n1.isRest: continue
                    if ignoreGraceNotes:
                        if n1.quarterLength == 0: continue
                    k = 1
                    while True:
                        n2 = segment[j+k]
                        if n2.isRest:
                            if n2.quarterLength <= silence2ignore:
                                k += 1
                            else:
                                n2 = None
                                break
                        elif (n2.quarterLength==0)and(ignoreGraceNotes==True):
                            j += 1
                        else:
                            break
                    if n2==None: continue
                    intvl = interval.Interval(n1, n2)
                    if directedInterval:
                        intvlName = intvl.directedName
                    else:
                        intvlName = intvl.name
                    intervalCount[intvlName] = (intervalCount.get(intvlName, 0)
                                                + 1)
    
    # Sorting intervals per size
    intvlNames = intervalCount.keys()
    toSort = {i:interval.Interval(i).semitones for i in intvlNames}
    sortedIntvl = sorted(toSort.items(), key=lambda x: x[1])
    xPositions = np.array([i[1] for i in sortedIntvl])
    # Check if there repeated positions
    for i in range(1, len(xPositions)):
        if xPositions[i] != xPositions[i-1]: continue
        for j in range(i):
            xPositions[j] += -1
    xLabels = [i[0] for i in sortedIntvl]
    yValues = np.array([intervalCount[l] for l in xLabels])
    
    # Start plotting
    print('Plotting...')

    ## Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)
    # Setting x limits
    limX = None
    
    # Setting y limits
    limY = None
    if count == 'sum':
        if directedInterval:
            limY = [0, 0.26]
        else:
            limY = [0, 0.45]

    plotting(xPositions, xLabels, yValues, limX=limX, limY=limY, yLabel=yLabel,
             col=col, h=h, scaleGuides=True)

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