# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:57:07 2016

@author: Rafael.Ctt
"""

from music21 import *

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
#        n = p.flat.notes.stream()[0]
#        if n.quarterLength != 0:
#            if n.hasLyrics():
#                if p.hasElementOfClass('Instrument'):
#                    p.remove(p.getInstrument())
#                voiceParts.append(p)
#        elif n.next().hasLyrics():
#            if p.hasElementOfClass('Instrument'):
#                p.remove(p.getInstrument())
#            voiceParts.append(p)
            
    return voiceParts

#def cleanScore(filename, showCleanScore=True, slurs=True):
#    '''str --> music21.stream.Score
#    
#    filename = string with the path to the file
#    If showCleanScore=True, the resulting score will be showed according to
#        music21 configuration
#    If slurs=True, it draws a slur for each syllable melisma
#    '''
#    
#    s = converter.parse(filename)
#    
#    # Transpose from C major (from Medeli) to E major
#    s.transpose('M3', classFilterList=['Note'], inPlace=True)
#    
#    # Delete barline objects from measures
#    for i in s.parts:
#        for j in i:
#            if j.isStream:
#                j.removeByClass(bar.Barline)
#    
#    s.makeNotation(inPlace=True)
#    
#    # Add slurs for syllable melismae
#    if slurs:
#        voicePart = findVoicePart(s)        
#        allnotes = voicePart.flat.notes.stream()
#        for n in allnotes: # Removing grace notes for slurring
#            if n.quarterLength == 0:
#                allnotes.remove(n)
#        for n in allnotes:
#            if n.hasLyrics() and not n.next().hasLyrics():
#                slurstart = n
#                i = allnotes.index(n) + 1
#                slurend = allnotes[i]
#                while not slurend.next().hasLyrics() and i < len(allnotes):
#                    slurend = allnotes[i]
#                    i += 1
#                slur = spanner.Slur([slurstart, slurend])
#                voicePart.insert(0, slur)
#            
#                    
#    if showCleanScore: s.show()
#    
#    return s

def extractPhrases(filename, lines): #, clean=False, slurs=False):
    '''str, list --> list
    
    filename: string with the path to the score
    lines: a list of tuples of integers indicating the first and last measure
    of each music phrase.
    '''
    
#    if clean:
#        s = cleanScore(filename, showCleanScore=False, slurs=slurs)
#    else:
#        s = converter.parse(filename)

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
#    cl = fragments[0].getClefs()[0]
#    ks = fragments[0].getKeySignatures()[0]
#    ts = fragments[0].getTimeSignatures()[0]
#    
#    toRemove = [cl, ks, ts]
#    toInsert = [0, cl, 0, ks, 0, ts]
#    
#    for fragment in fragments:
#        fragment.remove(toRemove)
#        fragment[1].insert(toInsert)
        
    return fragments

#def alignLines(scores, showAlignedScore=True): #, clean=False, slurs=False):
#    '''{str:[()]}, list --> music21.stream.Score
#    
#    scores: dictionary whose keys are strings with the path to the score and
#    whose values are lists of tuples of integers indicating the first and last
#    measure of each music phrase.
#    '''
#    
#    parts = [] # It stores the streams per line
#    
#    longestLength = 0 # Finding the longest measure length
#    
#    for score in scores:
#        s = converter.parse(score)
#        print(score.split('/')[-1] + ' parsed.')
#        voicePart = findVoicePart(s)
#        fragments = [] # It stores the streams per line
#        for line in scores[score]:
#            fragment = voicePart.measures(line[0], line[1])
#            fragment.remove(fragment.getTimeSignatures()[0])
#            if len(fragment.getElementsByClass('Measure')) > longestLength:
#                longestLength = len(fragment.getElementsByClass('Measure'))
#            fragments.append(fragment)
#        parts.extend(fragments)
#    
#    # Completing parts with empty measures so that all of them have the same
#    #   length as the longest.
#    
#    for part in parts:
#        partLength = len(part.getElementsByClass('Measure'))        
#        if partLength < longestLength:
#            part.repeatAppend(stream.Measure(), longestLength-partLength)
#    print('\nExtra empty measures appended.\n\nAligning parts...')
#    
#    alignedScore = stream.Score()
#    for part in parts:
#        alignedScore.insert(0, part)
#        
#    alignedScore.makeNotation(inPlace=True)
#    
#    print('\nDone!')    
#    
#    if showAlignedScore:
#        print ('\nOpening aligned score with MuseScore')
#        alignedScore.show()
#        
#    return alignedScore

def changeDurations(score, value, showScore=True, save=False):
    '''str, int --> music21.stream.Score
    
    Given a string with the address of a xml score and an integer, it returns a
    score without time signature and with all the durations multiplied by the
    given integer.
    '''
    
    s = converter.parse(score)
    
    for p in s.parts:
        try:
            p.measure(0).removeByClass('TimeSignature')
        except:
            p.measure(1).removeByClass('TimeSignature')
    
    for n in s.flat.notesAndRests:
        n.quarterLength = n.quarterLength * 2
        
    if showScore:
        s.show()
        
    if save:
        scoreName = score[:-4] + '-x' + str(value) + '.xml'
        s.write(fp=scoreName)

# Chinese punctuation marcs: ，。？！
#diacritics = [u'\uff0c', u'\u3002', u'\uff1f', u'\uff01']
diacritics = ['，', '。', '？', '！', '；', '：']
###############################################################################
## Change the name of the variable diacritics to closingDiacritics, or some- ##
## thing like that, meaning that these are the ones that are taken as a li-  ##
## ne segmentation mark, as opposed to allDiacritics, that includes all the  ##
## existing diacritics for counting purposes. IMPORTANT, change also the na- ##
## in the functions that use this variable.                                  ##
###############################################################################

def lyricsFromPart(part, printLyrics=False):
    '''music21.stream.Part --> str
    It takes a music21.stream.Part as input and returns its lyrics. If
    printLyrics is True, it also prints them in the console.
    '''

    notes = part.flat.notes

    rawlyrics = ''
    lyrics = ''
    lines = 0

    for n in notes:
        if n.hasLyrics(): rawlyrics += n.lyric

    for i in range(len(rawlyrics)):
        if rawlyrics[i] not in diacritics:
            lyrics += rawlyrics[i]
        elif rawlyrics[i] != diacritics[0]: # Chinese comma ，
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
                lyrics += rawlyrics[i]
#        else:
#            lyrics += (rawlyrics[i] + '\n')
#            lines += 1

    if lyrics[-1] != '\n':
        lyrics += '\n'

    print('One part with', str(lines), 'lines')
    
    if printLyrics: print(lyrics)

    return lyrics

def lyricsFromScore(filename, printLyrics=False):
    '''music21.stream.Score --> str
    It takes a music21.stream.Score as input and returns the lyrics of all the
    parts that contain lyrics. If printLyrics is True, it also prints them in
    the console.
    '''
    
    print('Parsing ' + filename.split('/')[-1])
    s = converter.parse(filename)
    
    voiceParts = findVoiceParts(s)
    
    if len(voiceParts) == 1:
        lyrics = lyricsFromPart(voiceParts[0], printLyrics)
    else:
        lyrics = ''
        for p in voiceParts:
            heading = 'Part ' + str(voiceParts.index(p) + 1) + '\n'          
            partLyrics = lyricsFromPart(p, printLyrics=False)
            lyrics += (heading + partLyrics)
            if printLyrics: print(heading + partLyrics)
    
    return lyrics

def lyrics2csv(scores, csv, printLyrics=True):
    '''[str], str --> csv file
    Given a list of paths for xml scores, it creates a csv file with all the
    lyrics per score in the given 'csv' path. If printLyrics is true, it prints
    the lyrics of each file in the cosole.
    '''
    for s in scores:
        lyrics = lyricsFromScore(s, printLyrics)
        with open(csv, 'a', encoding='utf-8') as f:
            f.write(s.split('/')[-1] + ',' + lyrics.split('\n')[0])
            for l in lyrics.split('\n')[1:-1]:
                f.write('\n,' + l)
            f.write('\n')

def partSegmentation(part, printLyrics):
    '''music21.stream.Part --> str
    It takes a music21 part as an input and it returns a string in the csv file
    format to be used in the lyricsSegmentation function
    '''
    lyrics = lyricsFromPart(part, printLyrics)   
    notes = part.flat.notes.stream()
    offsets = [notes[0].offset]
    index = 0
    limit = False

    for n in notes:
        if not n.hasLyrics(): continue
        nl = n.lyric
        ll = lyrics[index:index+len(nl)]
        if nl != ll:
            print('Error at index ', str(index), ' (', nl, ')')
            break
        if (lyrics[index+len(nl):index+len(nl)+1] == '\n') and (lyrics[index-1]
            != '\n'):
            limit = True                
            index += (len(nl) + 1)
        else:
            if limit:
#                offsets.append(n.previous().offset)
                preNote = n.previous()
                while preNote.quarterLength == 0:
                    preNote = preNote.previous()
                offsets.append(preNote.offset)
                offsets.append(n.offset)
                limit = False                    
                index += len(nl)
            else:
                index += len(nl)
    offsets.append(notes[-1].offset)

    partLyrics = ','
    index = 0
    for line in lyrics.split('\n')[:-1]:
        partLyrics += (line + ',' + str(offsets[index]) + ',' + 
                      str(offsets[index+1]) + '\n,')
        index += 2
        
    return partLyrics

def lyricsSegmentation(scores, csv, printLyrics=False):
    '''[str], str --> csv file
    Given a list of paths for xml scores, it creates a csv file in the given
    'csv' path with all the lyrics per score divided by lines plus the offset
    of the first and last note of each line. If printLyrics is true, it prints
    the lyrics of each file in the console.
    '''

    for score in scores:
        print('Parsing ' + score.split('/')[-1])
        s = converter.parse(score)
        
#        lyrics = lyricsFromScore(score, printLyrics)
        
        voiceParts = findVoiceParts(s)
        
#        for p in voiceParts:
#            offsets = [p.flat.notes[0].offset]        
#    
#            notes = p.flat.notes.stream()
#            index = 0
#            limit = False
#    
#            for n in notes:
#                if not n.hasLyrics(): continue
#                nl = n.lyric
#                ll = lyrics[index:index+len(nl)]
#                if nl != ll:
#                    print('Error at index ', str(index), ' (', nl, ')')
#                    break
#                if lyrics[index+len(nl):index+len(nl)+1] == '\n':
#                    limit = True                
#                    index += (len(nl) + 1)
#                    
#                else:
#                    if limit:
#                        offsets.append(n.previous().offset)
#                        offsets.append(n.offset)
#                        limit = False                    
#                        index += len(nl)
#                    else:
#                        index += len(nl)
#            offsets.append(notes[-1].offset)
        
        if len(voiceParts) == 1:
            partLyrics = partSegmentation(voiceParts[0], printLyrics)
        else:
            partLyrics = ','
            for p in voiceParts:
                onePartLyrics = partSegmentation(p, printLyrics)
                partLyrics += ('Part ' + str(voiceParts.index(p)+1) + '\n' +
                               onePartLyrics)
    
        finalFile = score.split('/')[-1] + partLyrics
        
#        index = 0
#        for line in lyrics.split('\n')[:-1]:
#            finalFile += (line + ',' + str(offsets[index]) + ',' + 
#                          str(offsets[index+1]) + '\n,')
#            index += 2        
        
        with open(csv, 'a', encoding='utf-8') as f:
            f.write(finalFile[:-1])

allDiacritics = ['。', '，', '、', '；', '：', '（', '）', '？', '！']

def judouSegmentation(lyricsdata, csvfile):
    '''str --> csv file
    It takes a lyricsdata file, which should be stored in the same folder as
    scores. It returns a csv file with the starting and ending offset of each
    judou.
    '''
    
    with open(lyricsdata, 'r', encoding='utf') as f:
        info = f.readlines()
    
    path = lyricsdata[:lyricsdata.rfind('/')+1]
    
    dous = ''
    
    for line in info:
        strInfo = line.strip().split(',')
        if strInfo[0] != '':
            score = converter.parse(path+strInfo[0])
            print('Parsing ' + strInfo[0])
            voiceParts = findVoiceParts(score)
            notesMap = createNotesMap(voiceParts, 0)
            lyricsIndex = 0
            if 'Part' in line:
                dous += '\n'
                continue
        
        if 'Part' in line:
            voicePart = int(strInfo[5][-1]) - 1
            notesMap = createNotesMap(voiceParts, voicePart)
            lyricsIndex = 0
            dous += '\n'
            continue

        lineDous = ''

        for i in range (9, 12):
            if len(strInfo[i]) == 0:
                lineDous += ',,'
                continue
            lyricsLength = 0
            for l in strInfo[i]:
                if l not in allDiacritics:
                    lyricsLength += 1
            n = notesMap[lyricsIndex]
            if strInfo[i][0:len(n[0])] == n[0]:
                start = str(n[1])
                lineDous += start + ','
            else:
                print('Error 1 at line', info.index(line), 'dou', i)
                print(strInfo[i][0:len(n[0])], n[0])
                return(notesMap)
            
            lyricsIndex += lyricsLength-1
            
            n = notesMap[lyricsIndex]
            if strInfo[i][-len(n[0]):] == n[0]:
                end = str(n[2])
                lineDous += end + ','
            else:
                print('Error 2 at line', info.index(line), 'dou', i)
                print(strInfo[i][-len(n[0]):], n[0])
                return(notesMap)

            lyricsIndex += 1
        
        lineDous = lineDous.strip(',')

#        toCheck = lineDous.split(',')
#        if not ((float(toCheck[0])==float(strInfo[6]))
#                and (float(toCheck[-1])==float(strInfo[7]))):
#            print('Boundaries of line and dous do not coincide at ' + 
#                  info.index(line))
        
        lineDous += '\n'
        dous += lineDous
        
    with open(path+csvfile, 'w') as f:
        f.write(dous)
            
    return dous

def createNotesMap(voiceParts, voicePart):
    '''[music21.stream.Part], int --> [[str, float, float]]
    Given a list of parts found using the findVoiceParts function and an int
    indicating which of this parts must be used, it returns a list of lists per
    each note with lyrics in that part, containing its lyric, starting offset
    and ending offset.
    '''
    notes = voiceParts[voicePart].flat.notes.stream()
    notesMap = []
    for n in notes:
        if n.hasLyrics():
            noteLyric = n.lyric
            noteOffset = n.offset
            notesMap.append([noteLyric, noteOffset])
            if len(notesMap) != 1:
                preNote = n.previous()
                while preNote.quarterLength == 0:
                    preNote = preNote.previous()
                notesMap[-2].append(preNote.offset)
    notesMap[-1].append(notes[-1].offset)
    
    return notesMap


















        
        

def getMelodicLine(filename, start, end, partIndex=1, show=False):
    '''str, float, float --> music21.stream.Stream
    Given the file path to a jingju score, and the offset value of the first
    and last note of a given line, it returns a music21 stream with that line.
    If the score has more than one singing parts, the part index should be
    introduced (strating from 1). If show is True, the line is shown.
    '''
    
    print('Parsing ' + filename.split('/')[-1])
    s = converter.parse(filename)
    
    voiceParts = findVoiceParts(s)
    
    p = voiceParts[partIndex-1]
    
    line = p.getElementsByOffset(start, end, mustBeginInSpan=False,
                                 includeElementsThatEndAtStart=False)
    
    if show:
        line.show()
    
    return line
    
def alignLines(linesdata, title, infoFile, file2write, removeSlurs=True,
               showScore=False, createInfoFile=True):
    '''dict --> [music21.stream.Score]
    '''
    
    filenames = sorted(linesdata.keys())
    
    scores = []
    linesCount = 19
    
    for f in filenames:
        s = converter.parse(f)
        print('Parsing ' + f.split('/')[-1] + '\n')
        voiceParts = findVoiceParts(s)
        for i in linesdata[f]:
            p = voiceParts[i]
            toRemove = list(p.recurse().getElementsByClass(['PageLayout',
                            'SystemLayout', 'Barline']))
            p.remove(toRemove, recurse=True)
            for j in linesdata[f][i]:
                line = p.getElementsByOffset(j[0], j[1], mustBeginInSpan=False,
                                           includeElementsThatEndAtStart=False)
                ts = line.flat.getTimeSignatures()
                if len(ts) > 0:
                    line[0].remove(ts[0])
                ks = line.flat.getKeySignatures()
                if len(ks) == 0:
                    line[0].insert(0, key.KeySignature(4))
                if linesCount == 19:
                    alignedScore = stream.Score()
                    scores.append(alignedScore)
                    alignedScore.insert(0, line)
                    linesCount = 0
                else:
                    alignedScore.insert(0, line)
                    linesCount += 1

    if len(scores) == 1:
        print('1 score to be created\n')
    else:
        print(str(len(scores)) + ' scores to be created\n')
    
    for s in scores:
        s.insert(0, metadata.Metadata())
        s.metadata.title = (title+' ('+str(scores.index(s)+1)+'/'+
                            str(len(scores))+')')
        s.makeNotation(inPlace=True)
        if removeSlurs:
            slurs2remove = list(s.recurse().getElementsByClass('Slur'))
            s.remove(slurs2remove, recurse=True)

    if showScore:
        for s in scores: s.show()
    
    print('Aligned lines for ' + infoFile)
    
    if createInfoFile:
        with open(file2write, 'w', encoding='utf-8') as f:
            f.write(infoFile)
    
    return scores

def comparePerCategories(datafile, hd, sq, bs, sx, removeSlurs=True,
                         showScore=False, createInfoFile=True):
    '''str, str, str, str, str --> [music21.stream.Score]
    '''
#    path = './scores/'
    path = datafile[:datafile.rfind('/')+1]
    
    with open(datafile, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    linesdata = {}

    filename = ''
    part = 0
    
    title = hd + ', ' + sq + ', ' + bs + ', ' + sx
    infoFile = title + '\n'
    lineNumber = 1
    
    lines2beAligned = 0
    scores2parse = 0
        
    for linedata in data:
        datacolumns = linedata.split(',')
        if datacolumns[0] != '':
            name = datacolumns[0]
            filename = path+name
            titleAlready = False
            if part != 0: part = 0
        if 'Part ' in linedata:
            pi = int(linedata[linedata.find('Part ')+len('Part ')])-1
            part = pi
        else:
            if ((hd == datacolumns[1]) and
                (sq == datacolumns[2]) and
                (bs == datacolumns[3]) and
                (sx == datacolumns[4])):
                
                lines2beAligned += 1

                if not titleAlready:
                    infoFile += '\n'+name+'\n'
                    titleAlready = True
                    scores2parse += 1
                infoFile += str(lineNumber)+'\t'+datacolumns[-3]+'\n'
                if lineNumber < 20:
                    lineNumber += 1
                else:
                    lineNumber = 1

                startStr = datacolumns[-2]
                endStr = datacolumns[-1]
                if '/' in startStr:
                    start = float(startStr.split('/')[0]) / float(
                                                        startStr.split('/')[1])
                else:
                    start = float(startStr)

                if '/' in endStr:
                    end = float(endStr.split('/')[0]) / float(
                                                          endStr.split('/')[1])
                else:
                    end = float(endStr)

                if filename not in linesdata:
                    linesdata[filename] = {part:[(start, end)]}
                else:
                    if part not in linesdata[filename]:
                        linesdata[filename][part] = [(start, end)]
                    else:                        
                        linesdata[filename][part].extend([(start, end)])

    print('Found ' + str(lines2beAligned) + ' lines to be aligned from ' +
          str(scores2parse) + ' scores\n')
          
    file2write = path + hd + '-' + sq + '-' + bs + '-' + sx + '.txt'
    
    scores = alignLines(linesdata, title, infoFile, file2write, removeSlurs,
                        showScore, createInfoFile)
    
    return scores

def comparePerChangduan(datafile, changduans, sx=None, removeSlurs=True,
                        showScore=False, createInfoFile=True):
    '''str, [str] --> [music21.stream.Score]
    '''
    path = datafile[:datafile.rfind('/')+1]
    
    with open(datafile, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    linesdata = {}

    filename = ''
    part = 0
    
    title = 'Comparison of ' + str(len(changduans)) + ' changduan'
    infoFile = title + '\n'
    lineNumber = 1

    lines2beAligned = 0
    scores2parse = 0
        
    for linedata in data:
        datacolumns = linedata.split(',')
        if datacolumns[0] != '':
            name = linedata.split(',')[0]
            filename = path+name
            titleAlready = False
            if name in changduans:
                validLine = True
            else:
                validLine = False
            if part != 0: part = 0
        if 'Part ' in linedata:
            pi = int(linedata[linedata.find('Part ')+len('Part ')])-1
            part = pi
        else:
            if not validLine: continue
            if (sx == None) or (datacolumns[4] == sx):
                lines2beAligned += 1
    
                if not titleAlready:
                    infoFile += '\n'+name+'\n'
                    titleAlready = True
                    scores2parse += 1
                infoFile += str(lineNumber)+'\t'+datacolumns[-3]+'\n'
                if lineNumber < 20:
                    lineNumber += 1
                else:
                    lineNumber = 1
    
                startStr = datacolumns[-2]
                endStr = datacolumns[-1]
                if '/' in startStr:
                    start = float(startStr.split('/')[0]) / float(
                                                    startStr.split('/')[1])
                else:
                    start = float(startStr)
    
                if '/' in endStr:
                    end = float(endStr.split('/')[0]) / float(
                                                      endStr.split('/')[1])
                else:
                    end = float(endStr)
    
                if filename not in linesdata:
                    linesdata[filename] = {part:[(start, end)]}
                else:
                    if part not in linesdata[filename]:
                        linesdata[filename][part] = [(start, end)]
                    else:                        
                        linesdata[filename][part].extend([(start, end)])

    print('Found ' + str(lines2beAligned) + ' lines to be aligned from ' +
          str(scores2parse) + ' scores\n')
          
    file2write = path + str(len(changduans)) + 'ChangduanCompared.txt'
    
    scores = alignLines(linesdata, title, infoFile, file2write, removeSlurs,
                        showScore, createInfoFile)
    
    return scores

def comparePerOrderedLines(datafile, lines, removeSlurs=True, showScore=False,
                    createInfoFile=True):
    '''str, [int] --> [music21.stream.Score]
    '''
    path = datafile[:datafile.rfind('/')+1]
    
    with open(datafile, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    linesdata = {}

    filename = ''
    part = 0

    lines4title = ''    
    for l in lines:
        lines4title += ', ' + str(l)
        
    title = 'Comparison of lines' + lines4title[1:]
    infoFile = title + '\n'
    lineNumber = 1

    lines2beAligned = len(lines)
    scores2parse = 0
        
    for linedata in data:
        datacolumns = linedata.split(',')
        if datacolumns[0] != '':
            name = linedata.split(',')[0]
            filename = path+name
            titleAlready = False
            if part != 0: part = 0
        if 'Part ' in linedata:
            pi = int(linedata[linedata.find('Part ')+len('Part ')])-1
            part = pi
        else:
            if data.index(linedata) not in lines: continue

            if not titleAlready:
                infoFile += '\n'+name+'\n'
                titleAlready = True
                scores2parse += 1
            infoFile += str(lineNumber)+'\t'+datacolumns[-3]+'\n'
            if lineNumber < 20:
                lineNumber += 1
            else:
                lineNumber = 1

            startStr = datacolumns[-2]
            endStr = datacolumns[-1]

            # Check if the start value is a fraction            
            if '/' in startStr:
                start = float(startStr.split('/')[0]) / float(
                                                startStr.split('/')[1])
            else:
                start = float(startStr)

            # Check if the end value is a fraction
            if '/' in endStr:
                end = float(endStr.split('/')[0]) / float(
                                                  endStr.split('/')[1])
            else:
                end = float(endStr)

            if filename not in linesdata:
                linesdata[filename] = {part:[(start, end)]}
            else:
                if part not in linesdata[filename]:
                    linesdata[filename][part] = [(start, end)]
                else:                        
                    linesdata[filename][part].extend([(start, end)])

    print(str(lines2beAligned) + ' lines to be aligned from ' +
          str(scores2parse) + ' scores\n')
          
    file2write = path + str(len(lines)) + 'LinesCompared.txt'
    
    scores = alignLines(linesdata, title, infoFile, file2write, removeSlurs,
                        showScore, createInfoFile)
    
    return scores
    
def comparePerLines(datafile, lines, removeSlurs=True, showScore=False,
                    createInfoFile=True):
    '''str, [int] --> [music21.stream.Score]
    '''
    path = datafile[:datafile.rfind('/')+1]
    
    with open(datafile, 'r', encoding='utf-8') as f:
        data = f.readlines()

    lines4title = ''    
    for l in lines:
        lines4title += ', ' + str(l)
        
    title = 'Comparison of lines' + lines4title[1:]
    infoFile = title + '\n'
    lineNumber = 1

    lines2beAligned = len(lines)
    scores2parse = []
        

    linesdata = [] # List of lines to be aligned

    for line in lines:
        datacolumns = data[line].split(',')

        # Search the file name:
        i = line
        while data[i].split(',')[0] == '':
            i += -1
        filename = path + data[i].split(',')[0]
        if filename not in scores2parse:
            scores2parse.append(filename)

        # Search the part name:
        part = 0        
        j = line
        while (j > i) and ('Part' not in data[j].split(',')[5]):
            j += -1
        if 'Part' in data[j].split(',')[5]:
            part += int(data[j].split(',')[5][-1])-1

        # Search de line boundaries        
        startStr = datacolumns[-2]
        endStr = datacolumns[-1]

        # Check if the start value is a fraction            
        if '/' in startStr:
            start = float(startStr.split('/')[0]) / float(
                                            startStr.split('/')[1])
        else:
            start = float(startStr)

        # Check if the end value is a fraction
        if '/' in endStr:
            end = float(endStr.split('/')[0]) / float(
                                              endStr.split('/')[1])
        else:
            end = float(endStr)

        # Append line to linesdata
        linesdata.append((filename, part, start, end))
            
        # Info of the lines to the info file
        infoFile += (str(lineNumber)+'\tline '+str(line)+'\t'+
                     filename.split('/')[-1]+'\t'+datacolumns[-3]+'\n')
        if lineNumber < 20:
            lineNumber += 1
        else:
            lineNumber = 1

    print(str(lines2beAligned) + ' lines to be aligned from ' +
          str(len(scores2parse)) + ' scores\n')
          
    scores = []
    linesCount = 19
    
    for linedata in linesdata:
        file2parse = ''
        if linedata[0] != file2parse:
            file2parse = linedata[0]
            s = converter.parse(file2parse)
            print('Parsing ' + file2parse.split('/')[-1] + '\n')
            voiceParts = findVoiceParts(s)
        p = voiceParts[linedata[1]]
        toRemove = list(p.recurse().getElementsByClass(['PageLayout',
                        'SystemLayout', 'Barline']))
        p.remove(toRemove, recurse=True)
        line = p.getElementsByOffset(linedata[-2], linedata[-1],
                                     mustBeginInSpan=False,
                                     includeElementsThatEndAtStart=False)
        ts = line.flat.getTimeSignatures()
        if len(ts) > 0:
            line[0].remove(ts[0])
        ks = line.flat.getKeySignatures()
        if len(ks) == 0:
            line[0].insert(0, key.KeySignature(4))
        if linesCount == 19:
            alignedScore = stream.Score()
            scores.append(alignedScore)
            alignedScore.insert(0, line)
            linesCount = 0
        else:
            alignedScore.insert(0, line)
            linesCount += 1

    if len(scores) == 1:
        print('1 score to be created\n')
    else:
        print(str(len(scores)) + ' scores to be created\n')
    
    for s in scores:
        s.insert(0, metadata.Metadata())
        s.metadata.title = (title+' ('+str(scores.index(s)+1)+'/'+
                            str(len(scores))+')')
        s.makeNotation(inPlace=True)
        if removeSlurs:
            slurs2remove = list(s.recurse().getElementsByClass('Slur'))
            s.remove(slurs2remove, recurse=True)

    if showScore:
        for s in scores: s.show()
    
    print('Aligned lines for ' + infoFile)
    
    if createInfoFile:
        file2write = path + str(len(lines)) + 'LinesCompared.txt'
        with open(file2write, 'w', encoding='utf-8') as f:
            f.write(infoFile)
    
    return scores