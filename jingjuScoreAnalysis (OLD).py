#!/usr/bin/python
# -*- coding: UTF-8 -*-

from music21 import *
import numpy as np
import matplotlib.pyplot as plt

def weightedHistogramPitchSpace(xmls, count='abs', figsize=None,
                                width=.4, showlabels=(True, True, True),
                                fontsize=None, rotation=None, xlimit=None,
                                ylimit=None, ticks_reduction_factor=0.5):
    '''([str]) --> matplotlib.pyplot.bar, dict
    It takes a list of musicXml file names as input, computes a weighted
    histogram of pitch space, plots it in a bar chart, and returns a dictionary
    with the pitch classes and their agregate duration.
    Count can be 'abs' for absolute duration values, 'sum' for the normalised
    duration to the summation, and 'max' for the normalised duration to the
    maximum.
    figsize: w,h tuple in inches
    showlabels: tuple of three bol, referring to title, xlabel, ylabel
    width: bars width (even number)
    fontsize:
    rotation:
    xlimit: minimum, maximum tuple
    ylimit: minimum, maximum tuple
    ticks_reduction_factor:
    '''

    if count not in ['abs', 'sum', 'max']:
        print 'Error: given count is not allowed.'
        return

    # Counting duration per pitch class
    noteDurations = {}

    for xml in xmls:
        print 'Parsing', xml
        s = converter.parse(xml)
        for n in s.flat.notes:
            name = n.nameWithOctave
            duration = n.quarterLength
            noteDurations[name] = noteDurations.get(name, 0) + duration

    # Sorting duration per pitch class frequency
    notes = noteDurations.keys()
    noteFrequencies = [(n, note.Note(n).frequency) for n in notes]
    sortedNoteFrequencies = sorted(noteFrequencies, key=lambda x: x[1])
    sortedNotes = [n[0] for n in sortedNoteFrequencies]
    sortedDurations = np.array([noteDurations[n] for n in sortedNotes])

    # Normalising, if requested
    if count == 'sum':
        values = sortedDurations / float(sum(sortedDurations))
        ylabel = 'Normalized Count'
    elif count == 'max':
        values = sortedDurations / float(max(sortedDurations))
        ylabel = 'Normalized Count'
    else:
        values = sortedDurations
        ylabel = 'Count'

    xposition = np.array([0]) # Xticks' positions separated by intervals
    for i in range(len(sortedNotes)-1):
        n1 = note.Note(sortedNotes[i])
        n2 = note.Note(sortedNotes[i+1])
        step = interval.notesToChromatic(n1, n2).directed
        xposition = np.append(xposition, xposition[-1] + step)

    # Plotting
    plotting(xposition, values, 'Weighted Histogram of Pitch Space', 'Pitch',
             ylabel, showlabels, sortedNotes, figsize, width, fontsize,
             rotation, xlimit, ylimit, ticks_reduction_factor)

    # plt.figure(1, figsize)
    # plt.bar(xposition, values, width)
    # plt.title(title, fontsize=fontsize)
    # plt.xlabel('Pitch', fontsize=fontsize)
    # plt.ylabel(ylabel, fontsize=fontsize)
    # if fontsize != None:
    #     plt.xticks(xposition + width/2, sortedNotes, fontsize=(fontsize*
    #     ticks_reduction_factor), rotation=rotation)
    #     plt.yticks(fontsize=(fontsize*ticks_reduction_factor))
    # else:
    #     plt.xticks(xposition + width/2, sortedNotes, rotation=rotation)
    # if xlimit != None:
    #     plt.xlim(xlimit[0], xlimit[1])
    # plt.grid(True, axis='y')
    # plt.tight_layout()
    # plt.show()

    return noteDurations


def intervalHistogram(xmls, directed=False, restThreshold=0, count='abs',
                      figsize=None, showlabels=(True, True, True), width=.4,
                      fontsize=None,rotation=None, xlimit=None, ylimit=None,
                      ticks_reduction_factor=0.5):
    '''([str]) --> matplotlib.pyplot.bar, dict
    It takes a list of musicXml file names as input, computes a interval
    histogram, plots it in a bar chart, and returns a dictionary
    with the interval classes and their occurrence.
    directed: if True, takes into account the direction of the interval
    restThreshold: the maximun rest duration in quarter length between two
        notes not to be considered for computing the interval between those
        notes.
    count can be 'abs' for absolute occurrrence values, 'sum' for the normalised
    occurrence to the summation, and 'max' for the normalised occurrence to the
    maximum.
    figsize: w,h tuple in inches
    showlabels: tuple of three bol, referring to title, xlabel, ylabel
    width: bars width (even number)
    fontsize:
    rotation:
    xlimit: minimum, maximum tuple
    ylimit: minimum, maximum tuple
    ticks_reduction_factor:
    '''

    if count not in ['abs', 'sum', 'max']:
        print 'Error: given count is not allowed.'
        return

    intvlOccurrence = {}

    for xml in xmls:
        print 'Parsing', xml
        s = converter.parse(xml)
        notes = s.flat.notesAndRests

        for i in range(len(notes)-1):
            if notes[i].isNote and notes[i+1].isNote:
                if notes[i].tie != None and notes[i].tie.type == 'start':
                    continue
                intvl = computeInterval(notes[i], notes[i+1], directed)
                intvlOccurrence[intvl] = intvlOccurrence.get(intvl, 0) + 1
            elif notes[i].isNote and notes[i+1].isRest:
                try:
                    if ((notes[i+1].quarterLength <= restThreshold) and
                        (notes[i+2].isNote)):
                        intvl = computeInterval(notes[i], notes[i+2], directed)
                        intvlOccurrence[intvl] = intvlOccurrence.get(intvl,0)+1
                except:
                    print 'Algo raro ha pasado...'

    # Sorting occurerence per interval length
    intvls = intvlOccurrence.keys()
    intvlSemitons = [(i, interval.Interval(i).chromatic.directed) for i in
        intvls]
    sortedIntvlSemitons = sorted(intvlSemitons, key=lambda x: x[1])
    sortedIntvls = [i[0] for i in sortedIntvlSemitons]
    sortedOcurrences = np.array([intvlOccurrence[i] for i in sortedIntvls])

    # Normalising, if requested
    if count == 'sum':
        values = sortedOcurrences / float(sum(sortedOcurrences))
        ylabel = 'Normalized Count'
    elif count == 'max':
        values = sortedOcurrences / float(max(sortedOcurrences))
        ylabel = 'Normalized Count'
    else:
        values = sortedOcurrences
        ylabel = 'Count'

    xposition = np.array([i[1] for i in sortedIntvlSemitons])

    plotting(xposition, values, 'Interval histogram', 'Interval class', ylabel,
             showlabels, sortedIntvls, figsize, width,
             fontsize, rotation, xlimit, ylimit, ticks_reduction_factor)

    return intvlOccurrence

def findInterval(xmls, interval, restThreshold=0, directed=False):
    '''([str], str, bol) --> {str:[{str:int}]}
    Takes a list of musicXml files addresses and an interval as input and find
    it in each of the scores by plotting the involved notes in red. It returns
    a list with the offset positions of each of the notes involved.
    '''

    allPositions = {}
    for xml in xmls:
        print 'Parsing', xml
        s = converter.parse(xml)
        notes = s.flat.notesAndRests

        positions = []
        intvl = None

        for i in range(len(notes)-1):
            if notes[i].isNote and notes[i+1].isNote:
                if notes[i].tie != None and notes[i].tie.type == 'start':
                    continue
                intvl = computeInterval(notes[i], notes[i+1], directed)
                n1 = notes[i]
                n2 = notes[i+1]
            elif notes[i].isNote and notes[i+1].isRest:
                try:
                    if ((notes[i+1].quarterLength <= restThreshold) and
                        (notes[i+2].isNote)):
                        intvl = computeInterval(notes[i], notes[i+2], directed)
                        n1 = notes[i]
                        n2 = notes[i+2]
                except:
                    print 'Algo raro ha pasado...'

            if (intvl != None) and (intvl == interval):
                    n1.color = '#FF0000' # Red in the RGB color code
                    n2.color = '#FF0000' # Red in the RGB color code
                    pair = {n1.nameWithOctave:n1.offset, n2.nameWithOctave:
                            n2.offset}
                    positions.append(pair)

        if len(positions) != 0:
            print '\t' + str(len(positions)), 'found'
            s.show()
            allPositions[xml]=positions
        else:
            print '\tNone found'

    return allPositions

def computeInterval(n1, n2, directed=False):
    '''(music21.note.Note, music21.note.Note, bool) --> str
    Given to music21 notes, computes the interval between and returns its name.
    If directed is True, it takes into account the direction of the interval.
    '''

    intvl = interval.notesToInterval(n1, n2)
    if directed:
        intvlName = intvl.directedName
    else:
        intvlName = intvl.name

    return intvlName

def plotting(xposition, values, title, xlabel, ylabel, showlabels, xticks,
             figsize, width, fontsize, rotation, xlimit, ylimit,
             ticks_reduction_factor):
    if not showlabels[0]: title = ''
    if not showlabels[1]: xlabel = ''
    if not showlabels[2]: ylabel = ''
    plt.figure(1, figsize)
    plt.bar(xposition, values, width)
    plt.title(title, fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if fontsize != None:
        plt.xticks(xposition + width/2, xticks, fontsize=(fontsize*
        ticks_reduction_factor), rotation=rotation)
        plt.yticks(fontsize=(fontsize*ticks_reduction_factor))
    else:
        plt.xticks(xposition + width/2, xticks, rotation=rotation)
    if xlimit != None:
        plt.xlim(xlimit[0], xlimit[1])
    if ylimit != None:
        plt.ylim(ylimit[0], ylimit[1])
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

# Chinese punctuation marcs: ，。？！
diacritics = [u'\uff0c', u'\u3002', u'\uff1f', u'\uff01']

def getlyrics(filename, returnLyrics=False):
    '''(str) -->
    It takes a musicXml file name as input and prints its lyrics. I returnLyrics
    is True, it also returns the lyrics.
    '''

    s = converter.parse(filename)

    print 'Parsing', filename

    for i in s:
        if i.isClassOrSubclass(('Stream', 'Part')):
            if i.flat.notes[0].quarterLength == 0:
                n = i.flat.notes[1]
            else:
                n = i.flat.notes[0]

            if n.hasLyrics:
                p = i.flat.notes

    rawlyrics = ''
    lyrics = ''
    lines = 0

    for note in p:
        if note.hasLyrics(): rawlyrics += note.lyric

    for i in range(len(rawlyrics)):
        if rawlyrics[i] not in diacritics:
            lyrics += rawlyrics[i]
        elif rawlyrics[i] == diacritics[1]: # Chinese full stop 。
            lyrics += (rawlyrics[i] + '\n')
            lines += 1
        else:
            if i < len(rawlyrics)-5:
                condition1 = ((rawlyrics[i+4] not in diacritics) and
                              (rawlyrics[i+5] not in diacritics) and
                              (rawlyrics[i+6] not in diacritics))
                condition2 = ((rawlyrics[i-4] not in diacritics) and
                              (rawlyrics[i-5] not in diacritics) and
                              (rawlyrics[i-6] not in diacritics))
                if condition1 and condition2:
                    lyrics += (rawlyrics[i] + '\n')
                    lines += 1
                else:
                    lyrics += rawlyrics[i]
            else:
                lyrics += (rawlyrics[i] + '\n')
                lines += 1

    if lyrics[-1] != '\n':
        lyrics += '\n'

    print str(lines), 'lines.'
    print lyrics

    if returnLyrics:
        return lyrics

def noteStrings(xmls, stringLength, restThreshold=0, removeGraces=True):
    '''([str], int, bol) --> [(str, int)]
    It takes a list of musicXml file names and the length of the note string to
    be searched (either 3 or 4), and it returns an ordered list of tuples with
    the notestring and its count. If removeGraces is True, grace notes are
    removed before counting.
    '''

    notestrings = {}

    for xml in xmls:
        print 'Parsing', xml
        s = converter.parse(xml)
        p = s.flat.notesAndRests

        # Removing grace notes if applicable
        if removeGraces:
            graces = []
            for n in p:
                if n.isGrace:
                    graces.append(n)
            p.remove(graces)

        # Removing rests between notes equal or under the given restThreshold
        if restThreshold > 0:
            rests = []
            for i in range(1, len(p)-1):
                if (p[i].isRest and (p[i].quarterLength<=restThreshold) and
                p[i-1].isNote and p[i+1].isNote):
                    rests.append(p[i])
            p.remove(rests)

        # Finding note strings of given lenght
        if stringLength == 3:
            for i in range(2, len(p)):
                if p[i-2].isNote and p[i-1].isNote and p[i].isNote:
                    notestring = p[i-2].name + p[i-1].name + p[i].name
                    notestrings[notestring] = notestrings.get(notestring, 0) + 1

        elif stringLength == 4:
            for i in range(3, len(p)):
                if (p[i-3].isNote and p[i-2].isNote and p[i-1].isNote and
                    p[i].isNote):
                    notestring = p[i-3].name+p[i-2].name+p[i-1].name+p[i].name
                    notestrings[notestring] = notestrings.get(notestring, 0) + 1

    return sorted(notestrings.items(), key=lambda x: x[1], reverse=True)

def findNoteString(xml, notestring, restThreshold=0, removeGraces=True,
                   show=True):
    '''(str, str) -->
    Parses the given musicXml file with music21, and searches for the given
    notestring. If show is True, it shows the score with the notes that form the
    notestring in red.
    NOTE: notestrings should be of 3 or 4 notes long
    '''

    print 'Parsing', xml
    s = converter.parse(xml)
    p = s.flat.notesAndRests

    # Removing grace notes if applicable
    if removeGraces:
        graces = []
        for n in p:
            if n.isGrace:
                graces.append(n)
        p.remove(graces)

    # Removing rests between notes equal or under the given restThreshold
    if restThreshold > 0:
        rests = []
        for i in range(1, len(p)-1):
            if (p[i].isRest and (p[i].quarterLength<=restThreshold) and
            p[i-1].isNote and p[i+1].isNote):
                rests.append(p[i])
        p.remove(rests)

    noteNames = []
    for char in notestring:
        if char not in ['-', '#']:
            noteNames.append(char)
        else:
            noteNames[-1] += char
    print '\tSearching for', noteNames

    stringsFound = 0
    if len(noteNames) == 3:
        for i in range(2, len(p)):
            if ((p[i-2].name == noteNames[0]) and (p[i-1].name == noteNames[1])
                and (p[i].name == noteNames[2])):
                p[i-2].color = '#FF0000' # Red in the RGB color code
                p[i-1].color = '#FF0000' # Red in the RGB color code
                p[i].color = '#FF0000' # Red in the RGB color code
                stringsFound += 1

    elif len(noteNames) == 4:
        for i in range(3, len(p)):
            if ((p[i-3].name==noteNames[0]) and (p[i-2].name==noteNames[1])
                and (p[i-1].name==noteNames[2]) and (p[i].name==noteNames[3])):
                p[i-3].color = '#FF0000' # Red in the RGB color code
                p[i-2].color = '#FF0000' # Red in the RGB color code
                p[i-1].color = '#FF0000' # Red in the RGB color code
                p[i].color = '#FF0000' # Red in the RGB color code
                stringsFound += 1

    print '\tFound', str(stringsFound), 'occurrences'

    if stringsFound > 0:
        s.show()
