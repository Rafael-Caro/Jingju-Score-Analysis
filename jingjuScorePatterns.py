# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:32:36 2017

@author: Rafael.Ctt
"""

import copy
import jingjuScores as jS
import jingjuScoreAnalysis as jSA
from music21 import *
from fractions import Fraction
import pickle

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
    for newSegment in extendedMaterial[-1]:
        newSegmentStart = newSegment[0]
        newSegmentEnd = newSegment[1]
        length1 = newSegmentEnd - newSegmentStart
        score = newSegment[2]
        part = newSegment[3]
        segment = newSegment[4]
        originalSegment = extendedMaterial[score][part][segment]
        originalSegmentStart = originalSegment[0]
        originalSegmentEnd = originalSegment[1]
        length2 = originalSegmentEnd - originalSegmentStart
        if length1 != length2:
            print('Possible error with ' + extendedMaterial[score][0] +
                  ', part ' + str(part) + ', segment ' + 
                  str(extendedMaterial[score][part][segment]) + 
                  ', and the new segment ' + str(newSegment[:2]))
    
    if title != None:
        print('Segments concatenated\nCreating files')
        concatenatedScore.insert(0, metadata.Metadata())
        concatenatedScore.title = title
        concatenatedScore.write(fp=title+'.xml')
        with open(title+'.pkl', 'wb') as f:
            pickle.dump(extendedMaterial, f, protocol=2)
    
    print('Done!')
    
    return concatenatedScore, extendedMaterial



def recodeScore(material, title=None, graceNoteValue=2.0, noteName='pitch'):
    '''
    '''

    # Check that the given noteName is valid:
    if noteName not in ['pitch', 'midi']:
        raise Exception('The given noteName is invalid')

    print('The duration unit is a 64th note')
    
    print('The duration value for grace notes is ' + str(graceNoteValue) + 
          ' duration units')

    # List the recoded score
    recodedScore = []
    
    # Store information for line retrieval
    lineInfo = []
    
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
                # For validation
                segmentDuration = 0
                for n in segment:
                    segmentDuration += n.quarterLength*16
                if segment[-1].isRest:
                    segmentDuration += -segment[-1].quarterLength*16
                    r = -2
                    while segment[r].quarterLength == 0:
                        segmentDuration += graceNoteValue
                        r += -1
                if segment[-1].quarterLength == 0:
                    segmentDuration += graceNoteValue
                
                # START RECODING
                line = []
                lineInfo.append([scoreIndex, partIndex, segmentIndex])
                graceNote = 0 # It stores the accumulated dur of grace notes
                              # to be substracted
                notePreGrace = None # It stores the index of the note before
                                    # grace notes found
                includeLyric = True # Check if there are several syllables into
                                    # brackets that shouldn't be included
                lyricAdjustment = 0 # Stores how many grace notes back the
                                    # lyric should be added
                for i in range(len(segment)):
                    n = segment[i]
                    # Check if n is note or rest    
                    if n.isRest:
                        name = n.name
                        dur = n.quarterLength*16
                        lyr = False
                    else: # If it is a note
                        # Check if it is a grace note
                        if n.quarterLength == 0: # It is a grace note, then
                            # Set name
                            if noteName == 'pitch':
                                name = n.nameWithOctave
                            elif noteName == 'midi':
                                name = n.pitch.midi
                            # Set duration with the value given
                            dur = graceNoteValue
                            # Accumulate grace note value to be subtracted
                            graceNote += graceNoteValue
                            # Store the index of the previous note, if there is
                            # one and is not a grace note
                            if (notePreGrace == None) and (len(line) > 0):
                                notePreGrace = len(line)-1
                            # Set lyric
                            lyr = False
                            # Update lyricAdjustment
                            lyricAdjustment += -1
                        else:
                        # If it's not a grace note, then
                            # Set name
                            if noteName == 'pitch':
                                name = n.nameWithOctave
                            elif noteName == 'midi':
                                name = n.pitch.midi

                            # Set duration
                            currentNoteDur = n.quarterLength*16
                            # Check if there is some grace note value to be
                            # subtracted
                            if graceNote > 0:
                            # There is grace note(s) duration to be subtracted
                                if n.hasLyrics():
                                # Subtract grace note value from the current
                                # note.
                                # But check first if its duration is bigger
                                # than the one of the grace note(s)
                                    if currentNoteDur > graceNote:
                                        dur = currentNoteDur - graceNote
                                    else:
                                    # Try to substract it from previous note
                                        if notePreGrace != None:
                                        # There is a previous note...
                                            lastNote = line[notePreGrace]
                                            lastNoteDur = lastNote[1]
                                            if lastNoteDur > graceNote:
                                            # ... and its duration is bigger
                                            # than the grace note(s) duration
                                                lastNote[1] += -graceNote
                                                dur = currentNoteDur
                                            else:
                                            # But if not, adjust
                                                adjustment = 0
                                                for j in range(notePreGrace+1,
                                                               i):
                                                    note2adjust = line[j]
                                                    note2adjust[1] += -1
                                                    adjustment += 1
                                                dur = (currentNoteDur -
                                                       graceNote + adjustment)
                                        else:
                                        # There is no previous note, so adjust
                                            adjustment = 0
                                            for j in range(i):
                                                note2adjust = line[j]
                                                note2adjust[1] += -1
                                                adjustment += 1
                                            dur = (currentNoteDur - graceNote +
                                                   adjustment)
                                else:
                                # Current note has no lyrics, the grace note(s)
                                # duration is subtracted from the previous note
                                # But check first if its duration is bigger
                                # than the one of the grace note(s)
                                    lastNote = line[notePreGrace]
                                    lastNoteDur = lastNote[1]
                                    if lastNoteDur > graceNote:
                                    # It is bigger, duration of grace note(s)
                                    # subtracted from previous note
                                        lastNote[1] += -graceNote
                                        dur = currentNoteDur
                                    else:
                                    # It is not bigger
                                    # Check if the current note duration is
                                    # bigger than the grace note(s) duration
                                        if currentNoteDur > graceNote:
                                        # It is bigger, so subtract
                                            dur = currentNoteDur - graceNote
                                        else:
                                        # It is not bigger, so adjust
                                            adjustment = 0
                                            for j in range(notePreGrace, i):
                                                note2adjust = line[j]
                                                note2adjust[1] += -1
                                                adjustment += 1
                                            lastNote[1] += (-graceNote +
                                                            adjustment)
                                            dur = currentNoteDur
                                    # Set lyricAdjustment to 0
                                    lyricAdjustment = 0
                            else:
                            # There is no grace note(s) duration to subtract
                                dur = currentNoteDur

                            #Check if it has a tie
                            if n.tie != None:
                                if n.tie.type != 'start':
                                    # Check if there is a grace note
                                    if graceNote > 0:
                                    # There is a grace note, so current note
                                    # counts as not tied
                                        dur = currentNoteDur
                                    else:
                                    # There is no grace note, so add the dur
                                    # to the previous tied note
                                        line[-1][1] += currentNoteDur
                                        continue

                            # Set lyric
                            if n.hasLyrics():
                                # Check if the lyric is a padding syllable
                                if ('（' in n.lyric) and ('）' in n.lyric):
                                    lyr = False
                                elif ('（' in n.lyric) and ('）' not in n.lyric):
                                    lyr = False
                                    includeLyric = False
                                elif ('（' not in n.lyric) and ('）' in n.lyric):
                                    lyr = False
                                    includeLyric = True
                                else:
                                    if includeLyric:
                                    # It is not a padding syllable
                                        if lyricAdjustment == 0:
                                        # It has no grace notes:
                                            lyr = True
                                        else:
                                        # It has grace note(s):
                                            line[lyricAdjustment][2] = True
                                            lyr = False
                                    else:
                                        lyr = False
                            else:
                                lyr = False
                            
                            # Set all counters to start mode
                            notePreGrace = None
                            graceNote = 0
                            lyricAdjustment = 0
                            
                    if dur <= 0:
                        pos = str(n.offset)
                        message = ('\tDuration ' + str(dur) + ' in ' +
                                   scoreName + ', ' + pos)
                        print(message)
                    line.append([name, dur, lyr])
                
                # Check if last note is a rest
                if line[-1][0] == 'rest':
                    line.pop(-1)
                
                # For validation:
                lineDuration = 0
                for n in line:
                    lineDuration += n[1]
                if segmentDuration != lineDuration:
                    print("\tDurations don't match at line", len(recodedScore))
                    print("\tSegment length: " + str(segmentDuration) +
                          ", line length: " + str(lineDuration))
                recodedScore.append(line)
    
    # Extend material list
    if len(lineInfo) != len(recodedScore):
        print('Possible problem with the information for line retrieval')
    extendedMaterial = copy.deepcopy(material)
    extendedMaterial.append(lineInfo)

    # Dump the list into a pickle file    
    if title != None:
        with open(title, 'wb') as f:
            pickle.dump(recodedScore, f, protocol=2)
        with open(title[:-4]+'_material.pkl', 'wb') as f:
            pickle.dump(extendedMaterial, f, protocol=2)

    return recodedScore, extendedMaterial



def showResultPatterns(resultsFile, concatenatedScore=None):
    '''str, str, str --> dic
    {str:{str:[[float, float]]}}
    '''

    # Equivalents of morphetic pitches as pitch names with octave in the range
    # of the corpus score for E major
    morphPitchs = {56: 'F#3', 57: 'G#3', 58: 'A3', 59: 'B3', 60: 'C#4',
                   61: 'D#4', 62: 'E4', 63: 'F#4', 64: 'G#4', 65: 'A4',
                   66: 'B4', 67: 'C#5', 68: 'D#5', 69: 'E5', 70: 'F#5',
                   71: 'G#5', 72: 'A5', 73: 'B5', 74: 'C#6'}
    
    with open(resultsFile, 'r') as f:
        resultsData = f.readlines()
    
    patterns = {}
    
    # Storing the patterns in the text file into a dictionary
    for l in resultsData:
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
    
    patternsNumber = len(patterns.keys())
    print(patternsNumber, 'patterns contained in the results file')
    
    patterns2sort = {}
    patternNames = patterns.keys()
    for patternName in patternNames:
        number = int(patternName[7:])
        patterns2sort[number] = patternName
    sortedPatterns = [patterns2sort[x] for x in sorted(patterns2sort.keys())]
    
    if concatenatedScore == None:
        for pat in sortedPatterns:
            occLengths = [len(patterns[pat][x]) for x in patterns[pat]]
            avg = round(sum(occLengths) / len(occLengths), 2)
            print(pat, 'with', len(patterns[pat]), 'occurrences (avg', avg,
                  'notes)')
        return patterns
    
    else:
        # Plot all patterns in the score
        for pat in sortedPatterns:
            pattern = patterns[pat]
            occurrencesNumber = len(pattern.keys())
            print(pat, 'with', occurrencesNumber, 'occurrences')
            # Parsing score
            score = converter.parse(concatenatedScore)
            scoreTitle = (resultsFile.split('/')[-1][:-4] + ': ' + pat + ' (' +
                          str(len(patterns[pat])) + ')')
            score.metadata.movementName = scoreTitle
            scoreName = concatenatedScore.split('/')[-1]
            print('\t' + scoreName + 'parsed')
            notes = score.flat.notes.stream()
                
            for occ in pattern:
                # Convert morphetic pitch into pitch names with octave
                occurrence = pattern[occ]
                occPitch = copy.deepcopy(occurrence)
                for n in occPitch:
                    morphPitch = n[1]
                    n[1] = morphPitchs[morphPitch]
            
                # Find notes from pattern according to the offsets
                for occNote in occPitch:
                    pos = occNote[0]
                    name1 = occNote[1]
                    scoreNote = notes.getElementsByOffset(pos)
                    for n in scoreNote:
                        name2 = n.nameWithOctave
                        if name1 == name2:
                            n.color = 'red'
                        else:
                            print('\t\tPossible problem at', pos)
            
            print('\tDisplaying', pat)
            score.show()