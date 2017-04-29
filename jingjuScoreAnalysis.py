# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from music21 import *
import fractions



###############################################################################
## FUNCTIONS FOR GATHERING MATERIAL                                          ##
###############################################################################

def collectLineMaterial(lyricsData, hd=['laosheng', 'dan'], sq=['erhuang',
                        'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                        'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                        'kuaiban'], ju = ['s', 's1', 's2', 'x']):
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
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
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


    
def collectJudouMaterial(lyricsData, hd=['laosheng', 'dan'], sq=['erhuang',
                         'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                         'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                         'kuaiban'], ju = ['s', 's1', 's2', 'x']):

    # Get the path of the folder shared by the lyricsData file and the xml
    # scores
    path = lyricsData[:lyricsData.rfind('/')+1]
    
    with open(lyricsData, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    material = []

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
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
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)
            
            if strInfo[10] != '':
                ju1_start = floatOrFraction(strInfo[10])
                ju1_end = floatOrFraction(strInfo[11])
                ju1 = [ju1_start, ju1_end]
                material[-1][-1].append(ju1)
            if strInfo[13] != '':
                ju2_start = floatOrFraction(strInfo[13])
                ju2_end = floatOrFraction(strInfo[14])
                ju2 = [ju2_start, ju2_end]
                material[-1][-1].append(ju2)
            if strInfo[16] != '':
                ju3_start = floatOrFraction(strInfo[16])
                ju3_end = floatOrFraction(strInfo[17])
                ju3 = [ju3_start, ju3_end]
                material[-1][-1].append(ju3)
            
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



###############################################################################
## MAIN FUNCTIONS                                                            ##
###############################################################################  

def pitchHistogram(material, filename, count='sum', countGraceNotes=True,
                   makePlot=True):
    '''list --> dict, bar plot
    
    It takes the list returned by the collectLineMaterial function, and returns
    a dictionary with all the existing pitches' nameWithOctave as keys and its
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
        parts = findVoiceParts(loadedScore)
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
    
    # Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)
    
    if makePlot:
        # Start plotting
        print('Plotting...')

        # Setting y limits
        limY = None
        if count == 'sum':
            limY = [0, 0.31]
    
        plotting(filename, xPositions, xLabels, yValues, limX=limX,
                 xLabel='Pitch', limY=limY, yLabel=yLabel, col=col, h=h,
                 scaleGuides=True, width=0.8)
        
    # List to return
    results = []
    for i in range(len(xLabels)):
        results.append([xLabels[i], yValues[i]])

    return results



def intervalHistogram(material, filename, count='sum', directedInterval=False,
                      silence2ignore=0.25, ignoreGraceNotes=False,
                      makePlot=True):
    '''list --> , bar plot
    
    It takes the list returned by the collectLineMaterial function, and returns
    
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
        parts = findVoiceParts(loadedScore)
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

    ## Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)
    
    if makePlot:
        # Start plotting
        print('Plotting...')
        
        # Setting x limits
        limX = None
        
        # Setting y limits
        limY = None
        if count == 'sum':
            if directedInterval:
                limY = [0, 0.27]
            else:
                limY = [0, 0.5]
    
        plotting(filename, xPositions, xLabels, yValues, limX=limX,
                 xLabel='Interval',limY=limY, yLabel=yLabel, col=col, h=h,
                 scaleGuides=True, width=0.8)
        
    # List to return
    results = []
    for i in range(len(xLabels)):
        results.append([xLabels[i], yValues[i]])

    return results



def plotting(filename, xPositions, xLabels, yValues, title=None, limX=None,
             xLabel=None, limY=None, yLabel=None, col=None, h=None,
             scaleGuides=False, width=0.8):

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
    plt.xticks(xPositions + width/2, xLabels, rotation=90, fontsize=20)
    plt.yticks(fontsize=18)
    if limX != None:
        plt.xlim(limX[0]-(1-width), limX[1]+1)
    else:
        plt.xlim(xPositions[0]-(1-width), xPositions[-1]+1)
    if limY != None:
        plt.ylim(limY[0], limY[1])
    if xLabel != None:
        plt.xlabel(xLabel, fontsize=26)
    if yLabel != None:
        plt.ylabel(yLabel, fontsize=26)
    plt.tight_layout()
    print('Done!')
    plt.savefig(filename)
#    plt.show()


    
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



def findCadentialNotes(judouMaterial, includeGraceNotes=True):
    '''
    '''

    cadNotCount = [{}, {}, {}]
    
    for score in judouMaterial[1:]:
        scorePath = score[0]
        loadedScore = converter.parse(scorePath)
        scoreName = scorePath.split('/')[-1]
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for segInd in range(len(score[partIndex])):
                startEnd = score[partIndex][segInd]
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                i = -1
                lastNote = segment[i]
                while lastNote.isRest:
                    i += -1
                    lastNote = segment[i]
                if includeGraceNotes:
                    cadenceNote = lastNote.nameWithOctave
                else:
                    while lastNote.quarterLength == 0:
                        print('Grace note omitted in ' + scoreName + ', '
                              + str(partIndex))
                        i += -1
                        lastNote = segment[i]
                    cadenceNote = lastNote.nameWithOctave
                secInd = segInd % 3
                sec = cadNotCount[secInd]
                sec[cadenceNote] = sec.get(cadenceNote, 0) + 1

    noteNames = {}

    for secCount in cadNotCount:
        for noteName in secCount.keys():
            noteNames[pitch.Pitch(noteName).midi] = noteName
            
    sortedNoteNames = [noteNames[j] for j in sorted(noteNames.keys())]
    
    for secCount in cadNotCount:
        counts = np.array([k for k in secCount.values()])
        toPerCent = 100 / sum(counts)
        for noteName in secCount:
            secCount[noteName] = secCount[noteName] * toPerCent
    
    sortedValues = []
    
    for noteName in sortedNoteNames:
        row = []
        for secCount in cadNotCount:
            row.append(secCount.get(noteName, 0))
        sortedValues.append(np.array(row))

#    for i in range(len(cadNotCount)):
#        toDiscard, noteNames, noteCount = sortDict(cadNotCount[i])
#        noteCount = np.array(noteCount)
#        toPerCent = 100 / np.sum(noteCount)
#        notePerCent = noteCount * toPerCent

    return sortedNoteNames, sortedValues



def cadentialNotes(judouMaterialList, filename, includeGraceNotes=True,
                   makePlot=True):

    xLabels = ['Sec 1', 'Sec 2', 'Sec 3']
    pos = np.arange(len(xLabels))

    colors = {'G#3':['#F4D03F','x'],'B3':['#76D7C4','x'],'C#4':['#2E86C1','x'],
              'C##4':['#5B2C6F','x'],'D#4':['#BB8FCE','x'],'E4':['#E74C3C',''],
              'F#4':['#F39C12',''], 'G#4':['#F4D03F',''], 'A4':['#2ECC71',''],
              'A#4':['#117864',''], 'B4':['#76D7C4',''], 'C#5':['#2E86C1',''],
              'D#5':['#BB8FCE',''],'E5':['#E74C3C','O'],'F#5':['#F39C12','O']}              

    legendCode = {}
    width = 0.5
    
    if len(judouMaterialList) == 2:
        titles = ['Opening line', 'Closing line']
    
    elif len(judouMaterialList) == 3:
        titles = ['Opening line 1', 'Opening line 2', 'Closing line']

    y = True
    plt.figure()
    for i in range(len(judouMaterialList)):
        material = judouMaterialList[i]
        sortedNoteNames, sortedValues = findCadentialNotes(material,
                                                           includeGraceNotes)
        bot = np.array([0, 0, 0])
        plotNumber = '1' + str(len(judouMaterialList)) + str(i+1)
        plt.subplot(int(plotNumber))
        for j in range(len(sortedValues)):
            val = sortedValues[j]
            colHatch = colors[sortedNoteNames[j]]
            p = plt.bar(pos, val, width, color=colHatch[0],
                        hatch = colHatch[1], bottom=bot, align='center')
            bot = bot + val
            # Prepare the legend
            noteName = sortedNoteNames[j]
            mid = pitch.Pitch(noteName).midi
            legendCode[mid] = [p[0], noteName]
        if not y:
            plt.yticks(np.array([]), ())
        y = False
        plt.ylim(0, 100)
        plt.title(titles[i])
        plt.xticks(pos, xLabels)

    legendColors = []
    legendNotes = []
    for k in sorted(legendCode.keys(), reverse=True):
        lcode = legendCode[k]
        legendColors.append(lcode[0])
        legendNotes.append(lcode[1])
    plt.legend(legendColors, legendNotes, bbox_to_anchor=(1, 1), loc=2)
    plt.tight_layout(rect=(0, 0, 0.83, 1))
    plt.savefig(filename)
#    plt.show()



def melodicDensity(material, filename, includeGraceNotes=True,
                   notesOrDuration='notes'):
    '''list --> box plot
    
    It takes the list returned by the collectLineMaterial function, and returns
    '''
    
    if notesOrDuration not in ['notes', 'duration']:
        raise Exception('The given value for notesOrDuration is not correct')

    syllables = []
    totalCount = []
    accumulatedCount = []
    
    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        localCount = []
        parts = findVoiceParts(loadedScore)
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
                openParenthesis = False
                graceNote = False
                for i in range(len(segment)):
                    n = segment[i]
                    if notesOrDuration == 'notes':
                        value = 1
                    else:
                        value = n.quarterLength
                    if n.isRest: continue
                    if n.quarterLength==0:
                        if not includeGraceNotes: continue
                        j = 1
                        while (i+j<len(segment) and
                               segment[i+j].quarterLength==0):
                            j += 1
                        if i+j == len(segment): continue
                        n2 = segment[i+j]
                        if n2.hasLyrics():
                            if (('（' in n2.lyric) or ('）' in n2.lyric) or
                                openParenthesis):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                            else:
                                if graceNote:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                else:
                                    localCount.append(value)
                                    accumulatedCount.append(value)
                                    syllables.append(n2.lyric)
                                    graceNote = True
                        else:
                            localCount[-1] += value
                            accumulatedCount[-1] += value
                    else:
                        if n.hasLyrics():
                            # Check if the lyric is a padding syllable
                            if ('（' in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                            elif ('（' in n.lyric) and ('）' not in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                                openParenthesis = True
                            elif ('（' not in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                                openParenthesis = False
                            else:
                                if openParenthesis:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                elif graceNote:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                    graceNote = False
                                else:
                                    localCount.append(value)
                                    accumulatedCount.append(value)
                                    syllables.append(n.lyric)
                        else:
                            localCount[-1] += value
                            accumulatedCount[-1] += value
        totalCount.append(localCount)

#    for i in range(len(syllables)):
#        print(syllables[i], notesPerSyl[i])

    totalCount.append(accumulatedCount)

#    notesPerSyl = np.array(notesPerSyl)

    xLabels = [str(i) for i in range(1, len(totalCount))]
    xLabels.append('Avg')

    plt.boxplot(totalCount)
    plt.xticks(range(1, len(totalCount)+1), xLabels, fontsize=20)
    plt.yticks(fontsize=18)
    plt.axvline(x=len(totalCount)-0.5, ls='--', color='red')
    plt.ylim(0, 27)
    plt.xlabel('Sample scores', fontsize=26)
    plt.ylabel('Duration per quarter note', fontsize=26)
    plt.tight_layout()
    plt.savefig(filename)
#    plt.show()

    return totalCount



###############################################################################
## AUXILIARY FUNCTIONS                                                       ##
###############################################################################

def findVoiceParts(score):
    '''music21.stream.Score --> [music21.stream.Part]
    
    Given a music21.stream.Score with one or more parts, it returns a list of
    the parts that contain lyrics
    '''
    
    voiceParts = []
    
    for p in score.parts:
        if len(p.flat.notes) == 0: continue
        i = 0
        n = p.flat.notes[i]
        while n.quarterLength == 0:
            i += 1
            n = p.flat.notes.stream()[i]
        if n.hasLyrics():
                if p.hasElementOfClass('Instrument'):
                    p.remove(p.getInstrument())
                voiceParts.append(p)
    return voiceParts



def getAmbitus(material):
    '''list --> music21.interval.Interval
    
    It takes the list returned by the collectLineMaterial function, and returns
    an interval from the lowest note found to the highest note found.
    '''
    
    ambitusStart = None
    ambitusEnd = None
    
    for score in material:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
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



def findScoreByPitchThreshold(material, thresholdPitch, lowHigh):
    '''list, int, str --> [music21.stream.Score]
    It takes the list returned by the collectLineMaterial function, a pitch
    midi value, and the string "low" or "high" to look for those scores that
    contain pitchs lower or higher than the given threshold.
    '''
    
    scores = []    

    for score in material:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
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



def findScoreByPitch(material, pitchList):
    '''
    '''

    scores = []

    for score in material[1:]:
        showScore = False
        pitchesFound = {}
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
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
                for n in segment:
                    noteName = n.nameWithOctave
                    if noteName in pitchList:
                        n.color = 'red'
                        pitchesFound[noteName] = pitchesFound.get(noteName,0)+1
                        showScore = True
                        if scorePath not in scores:
                            scores.append(scorePath)
        if showScore:
            for p in pitchesFound:
                print('\t' + str(pitchesFound[p]), 'samples of', p,
                  'found in this score')
            print('\tShowing', scoreName)
            loadedScore.show()

    return(scores)



def findScoreByInterval(material, intvlList, directedInterval=False,
                 silence2ignore=0.25, ignoreGraceNotes=False):
    '''
    '''
    for score in material[1:]:
        showScore = False
        intvlsFound = {}
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
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
                    currentIntvl = interval.Interval(n1, n2)
                    if directedInterval:
                        intvlName = currentIntvl.directedName
                    else:
                        intvlName = currentIntvl.name
                    if intvlName in intvlList:
                        n1.color = 'red'
                        n2.color = 'red'
                        intvlsFound[intvlName] = intvlsFound.get(intvlName,0)+1
                        showScore = True
        if showScore:
            for k in intvlsFound:
                print('\t' + str(intvlsFound[k]), 'samples of', k,
                  'found in this score')
            print('\tShowing', scoreName)
            loadedScore.show()