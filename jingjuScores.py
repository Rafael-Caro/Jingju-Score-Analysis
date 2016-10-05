# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:57:07 2016

@author: Rafael.Ctt
"""

from music21 import *

def findVoicePart(score):
    '''music21.stream.Score --> music21.stream.Part
    
    Given a music21.stream.Score with one or more parts in which ONE of them is
        a sung part, it returns it as a music21.stream.Part
    '''
    
    for p in score.parts:
        n = p.flat.notes.stream()[0]
        if n.quarterLength != 0:
            if n.hasLyrics():
                voicePart = p
        elif n.next().hasLyrics():
            voicePart = p
            
    return voicePart

def cleanScore(filename, showCleanScore=True, slurs=True):
    '''str --> music21.stream.Score
    
    filename = string with the path to the file
    If showCleanScore=True, the resulting score will be showed according to
        music21 configuration
    If slurs=True, it draws a slur for each syllable melisma
    '''
    
    s = converter.parse(filename)
    
    # Transpose from C major (from Medeli) to E major
    s.transpose('M3', classFilterList=['Note'], inPlace=True)
    
    # Delete barline objects from measures
    for i in s.parts:
        for j in i:
            if j.isStream:
                j.removeByClass(bar.Barline)
    
    s.makeNotation(inPlace=True)
    
    # Add slurs for syllable melismae
    if slurs:
        voicePart = findVoicePart(s)        
        allnotes = voicePart.flat.notes.stream()
        for n in allnotes: # Removing grace notes for slurring
            if n.quarterLength == 0:
                allnotes.remove(n)
        for n in allnotes:
            if n.hasLyrics() and not n.next().hasLyrics():
                slurstart = n
                i = allnotes.index(n) + 1
                slurend = allnotes[i]
                while not slurend.next().hasLyrics() and i < len(allnotes):
                    slurend = allnotes[i]
                    i += 1
                slur = spanner.Slur([slurstart, slurend])
                voicePart.insert(0, slur)
            
                    
    if showCleanScore: s.show()
    
    return s

def extractPhrases(filename, lines, clean=False, slurs=False):
    '''str, list --> list
    
    filename: string with the path to the score
    lines: a list of tuples of integers indicating the first and last measure
    of each music phrase.
    '''
    
    if clean:
        s = cleanScore(filename, showCleanScore=False, slurs=slurs)
    else:
        s = converter.parse(filename)
        
    voicePart = findVoicePart(s)
    
    fragments = [] # It stores the streams per line
    
    for line in lines:
        fragment = voicePart.measures(line[0], line[1])
        fragments.append(fragment)
    
    # Clef, key signature and time signatures in the fragments after using the
    #   the music21.stream.Stream.measures() method are stored in offset 0.0 of
    #   the music21.stream.Part. When different parts are put together to form
    #   a score, this results in an error, so clef, key signature and time
    #   signature should be moved to offset 0.0 in the first meausre of each
    #   part.
    cl = fragments[0].getClefs()[0]
    ks = fragments[0].getKeySignatures()[0]
    ts = fragments[0].getTimeSignatures()[0]
    
    toRemove = [cl, ks, ts]
    toInsert = [0, cl, 0, ks, 0, ts]
    
    for fragment in fragments:
        fragment.remove(toRemove)
        fragment[1].insert(toInsert)
        
    return fragments

def alignLines(scores, clean=False, slurs=False, showAlignedScore=True):
    '''{str:[()]}, list --> music21.stream.Score
    
    scores: dictionary whose keys are strings with the path to the score and
    whose values are lists of tuples of integers indicating the first and last
    measure of each music phrase.
    '''
    
    parts = [] # It stores the streams per line
    
    for score in scores:
        fragments = extractPhrases(score, scores[score], clean=clean,
                                   slurs=slurs)
        parts.extend(fragments)
    
    # Completing parts with empty measures so that all of them have the same
    #   length as the longest.
    longestLength = 0
    for part in parts:
        if len(part) > longestLength:
            longestLength = len(part)
    for part in parts:
        if len(part) < longestLength:
            part.repeatAppend(stream.Measure(), longestLength-len(part))
    
    alignedScore = stream.Score()
    for part in parts:
        alignedScore.insert(0, part)
        
    if showAlignedScore: alignedScore.show()
        
    return alignedScore