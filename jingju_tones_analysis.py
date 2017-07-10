# -*- coding: utf-8 -*-

from music21 import *
import fractions



###############################################################################
## FUNCTIONS FOR GATHERING MATERIAL                                          ##
###############################################################################

def toneMaterialPerLine(linesData, hd=['laosheng', 'dan'], sq=['erhuang',
                         'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                         'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                         'kuaiban'], ju = ['s', 's1', 's2', 'x']):

    '''str, [str], [str], [str], [str] --> [{str:list}, [str[[str, float,
                                            float, str, str, str, str]]]
   
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a list with
    information from each line that matches the search criteria. The structure
    of this list is as follows
        dictionary with the included bs, hd, ju, sq
        score-lists: a list for each score that contains a line that matches
                     the search criteria. It includes:
            score path (str)
            part-lists: a list for each vocal part of the score. For the part
                        that contains lines that match the search criteria, its
                        part-list includes:
                line-list: for each line that matches the search criteria,
                           including:
                    lyrics (str)
                    start offset of the line (float)
                    end offset of the line (float)
                    tones (str)
                    hangdan (str)
                    shengqiang (str)
                    banshi (str)
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
        start = floatOrFraction(strInfo[6])
        end = floatOrFraction(strInfo[7])
        tones = strInfo[8]
        
        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            material[-1][-1].append([line, start, end, tones, hd0, sq0, bs0])
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



def toneMaterialPerJudou(linesData, hd=['laosheng', 'dan'], sq=['erhuang',
                         'xipi'], bs = ['manban', 'sanyan', 'zhongsanyan',
                         'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                         'kuaiban'], ju = ['s', 's1', 's2', 'x']):

    '''str, [str], [str], [str], [str] --> [{str:list}, [str[[str, float,
                                            float, str]]]
   
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a list with
    information from each judou that matches the search criteria. The structure
    of this list is as follows
        dictionary with the included bs, hd, ju, sq
        score-lists: a list for each score that contains a line that matches
                     the search criteria. It includes:
            score path (str)
            part-lists: a list for each vocal part of the score. For the part
                        that contains lines that match the search criteria, its
                        part-list includes:
                judou-list: each line that matches the search criteria produces
                            three judou-lists, including:
                    lyrics (str)
                    start offset of the judou (float)
                    end offset of the judou (float)
                    tones (str)
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
        jd1start = floatOrFraction(strInfo[10])
        jd1end = floatOrFraction(strInfo[11])
        jd2 = strInfo[12]
        jd2tones = tones[countCharacters(jd1):
                         countCharacters(jd1)+countCharacters(jd2)]
        jd2start = floatOrFraction(strInfo[13])
        jd2end = floatOrFraction(strInfo[14])
        jd3 = strInfo[15]
        jd3tones = tones[countCharacters(jd1)+countCharacters(jd2):]
        jd3start = floatOrFraction(strInfo[16])
        jd3end = floatOrFraction(strInfo[17])
        
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



###############################################################################
## MAIN FUNCTIONS                                                            ##
###############################################################################

def syllabicContour(material, filename=None, query=[]):
    '''list --> dict
    
    It takes the list returned by the toneMaterialPerLine function, computes a
    syllabic contour analysis and print the results in a table. Columns are
    separated by tabs and rows by lines.

    If a file path given in filename, it writes the results in that file.
    
    The query parameter allows to show the score of the line that contains
    syllables that satisfy the query criteria. The query parameter is a list
    with two elements, a tone (str) and a contour (str); for example ['1', 'A']
    
    It returns two items:
    - A nested list with a list per score, line and syllable. The syllable list
      contains character in the score (str), the character in material (str),
      the tone (str), the contour (str) and a list with the midi value of all
      the notes (int).
    - A dictionary with tones 1 to 4 as keys, and a dictionary counting each
      contour as value.
    '''
    
    contours = {'1':{}, '2':{}, '3':{}, '4':{}}
    syllables = []
    tone5 = 0
    
    for score in material[1:]:
        # Loading the score to get the parts list
        syllables.append([])
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
            
            for line in score[partIndex]:
                syllables[-1].append([])
                lyrics = line[0]
                start = line[1]
                end = line[2]
                tones = line[3]
                hd = line[4]
                sq = line[5]
                bs = line[6]
                
                # Set the tuoqiang threshold
                if hd == 'laosheng':
                    if sq == 'erhuang':
                        if bs == 'manban':
                            threshold = 4.5
                        elif bs == 'sanyan':
                            threshold = 3.5
                        elif bs == 'kuaisanyan':
                            threshold = 3.5
                        elif bs == 'yuanban':
                            threshold = 2.5
                    elif sq == 'xipi':
                        if bs == 'manban':
                            threshold = 3.5
                        elif bs == 'sanyan':
                            threshold = 3.5
                        elif bs == 'kuaisanyan':
                            threshold = 3.0
                        elif bs == 'yuanban':
                            threshold = 2.25
                        elif bs == 'liushui':
                            threshold = 1.75
                        elif bs == 'kuaiban':
                            threshold = 1.5
                elif hd == 'dan':
                    if sq == 'erhuang':
                        if bs == 'manban':
                            threshold = 3.5
                        elif bs == 'zhongsanyan':
                            threshold = 3.0
                        elif bs == 'kuaisanyan':
                            threshold = 2.0
                        elif bs == 'yuanban':
                            threshold = 1.75
                    elif sq == 'xipi':
                        if bs == 'manban':
                            threshold = 3.5
                        elif bs == 'yuanban':
                            threshold = 3.5
                        elif bs == 'erliu':
                            threshold = 2.0
                        elif bs == 'liushui':
                            threshold = 1.75
                        elif bs == 'kuaiban':
                            threshold = 1.5
                
                lyrIndex = 0
                toneJump = 0
                
                syl = []
                sylLength = 0
                tuoqiang = False
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
                            if sylLength <= threshold:
                                syl.append(n.pitch.midi)
                                sylLength += n.quarterLength
                            else:
#                                m = n.getContextByClass('Measure')
#                                b = n.getOffsetBySite(m)
                                tuoqiang = True
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        elif inBrackets == True:
                            if sylLength <= threshold:
                                syl.append(n.pitch.midi)
                                sylLength += n.quarterLength
                            else:
#                                m = n.getContextByClass('Measure')
#                                b = n.getOffsetBySite(m)
                                tuoqiang = True
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        elif '）' in char:
                            inBrackets = False
                            if sylLength <= threshold:
                                syl.append(n.pitch.midi)
                                sylLength += n.quarterLength
                            else:
#                                m = n.getContextByClass('Measure')
#                                b = n.getOffsetBySite(m)
                                tuoqiang = True
                            toneJump += len(char)
                            if len(toRed)>0: toRed.append(i)
                        else:
                            # First, solve the accumulated pitches in syl from
                            # the previous syllable
                            if len(syl) > 0:
                                if tuoqiang:
                                    contour = defineContour(syl[:3])
                                else:
                                    contour = defineContour(syl)
                                if (len(query)>0 and contour==query[1]
                                    and len(toRed)>0):
                                    for n2r in toRed:
                                        segment[n2r].color = 'red'
                                    showSegment = True
                                syllables[-1][-1][-1].append(contour)
                                syllables[-1][-1][-1].append(syl)
                                if currentTone == '5': tone5 += 1
                                else:
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
                            syllables[-1][-1].append([char,currentChar,
                                                      currentTone])
                            toneJump += len(char) - 1
                            syl = graceNotes + [n.pitch.midi] # Add preceding
                                                              # grace notes
                            graceNotes = [] # Grace notes buffer empty
                            sylLength = 0
                            tuoqiang = False
                        lyrIndex += len(char)

                    elif n.quarterLength == 0: continue # Omit grace notes

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
                                    if sylLength <= threshold:
                                        syl.append(mid)
                                        sylLength += n.quarterLength
                                    else:
#                                        m = n.getContextByClass('Measure')
#                                        b = n.getOffsetBySite(m)
                                        tuoqiang = True
                                    if len(toRed)>0: toRed.append(i)
                            else:
                                if sylLength <= threshold:
                                    syl.append(mid)
                                    sylLength += n.quarterLength
                                else:
#                                    m = n.getContextByClass('Measure')
#                                    b = n.getOffsetBySite(m)
                                    tuoqiang = True
                                if len(toRed)>0: toRed.append(i)
                        else:
                            if sylLength <= threshold:
                                syl.append(mid)
                                sylLength += n.quarterLength
                            else:
#                                m = n.getContextByClass('Measure')
#                                b = n.getOffsetBySite(m)
                                tuoqiang = True
                            if len(toRed)>0: toRed.append(i)
                
                if tuoqiang:
                    syllables[-1][-1][-1].append(defineContour(syl[:3]))
                else:
                    syllables[-1][-1][-1].append(defineContour(syl))
                syllables[-1][-1][-1].append(syl)

                if showSegment: segment.show()
                    
#    for i in range(1, 5):
#        print(i, sorted(contours[str(i)].items(), key=lambda x:x[1],
#                        reverse=True))

    txt2print = '\tdL\tL\tA\tD\tAD\tDA'
    rels = ['L', 'A', 'D', 'AD', 'DA']
    
    for t in sorted(contours.keys()):
        tone = contours[t]
        total = sum(tone.values())
        txt2print += '\nTone ' + t + ' (' + str(total) + ')'
        totaldL = 0
        for rel in tone.keys():
            if rel != 'dL':
                totaldL += tone[rel]
        dL = tone['dL']
        dLpc = round(dL / (total/100), 2)
        txt2print += '\t' + str(dL) + ' (' + str(dLpc) + '%)'
        for rel in rels:
            if rel not in tone.keys():
                txt2print += '\t'
                continue
            relv = tone[rel]
            relpc = str(round(relv / (total/100), 2))
            relpcdL = str(round(relv / (totaldL/100), 2))
            txt2print += '\t'+str(relv)+' ('+relpc+'%/'+relpcdL+'%)'
    txt2print += '\nTone 5 ('+str(tone5)+')\t\t\t\t\t\t'

    print('\n--------------------------------------------------')
    print('Pairwise relationship analysis results\n')
    print(txt2print)
            
    if filename != None:
        with open(filename, 'w') as f:
            f.write(txt2print)

    return syllables, contours



def pairwiseRelationship(material, relationship=[1, 0], filename=None,
                         query=[]):
    '''list --> list, dict
    
    It takes the list returned by the toneMaterialPerJudou function, and
    analyses the pairwise relationship of the syllables contained in each
    judou, according to the relationship given.

    The argument relationship is a
    list with two values, indicating the note to be compared from the melodic
    contour of each syllable of the pair:
        0 for the first note,
        1 for the last note.
    
    It prints a table with the results, both in absolute numbers and
    percentage. Columns are separated by tabs and rows by lines.

    If a file path given in filename, it writes the results in that file.
    
    It returns two items:
    - A nested list containing one list per score, part,
      dou and syllable for all the syllables in the argument material. Each
      syllable list containts the character (str), the tone (str) the first
      note (int) and last note (int).
    - A dictionary with all the tone combinations (including tone 5) as keys
      and the count of A, L, D for each combination.
        
    The query parameter allows to show the score of each dou that satisfies the
    query criteria. The query is a list with two elements: a tone pair (str)
    and a direction (str); for example: ['1-2', 'A'].
    '''
    
    pairs = {'1-1':{}, '1-2':{}, '1-3':{}, '1-4':{}, '1-5':{},
             '2-1':{}, '2-2':{}, '2-3':{}, '2-4':{}, '2-5':{},
             '3-1':{}, '3-2':{}, '3-3':{}, '3-4':{}, '3-5':{},
             '4-1':{}, '4-2':{}, '4-3':{}, '4-4':{}, '4-5':{},
             '5-1':{}, '5-2':{}, '5-3':{}, '5-4':{}}
    dous = []
    
    for score in material[1:]:
        s = []
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
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
                                print('Problem with', char, currentChar)
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
                    note1 = syl1[relationship[0]+2]
                    note2 = syl2[relationship[1]+2]
                    if note1 > note2:
                        shape = 'D'
                    elif note1 == note2:
                        shape = 'L'
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
                            parts = findVoiceParts(loadedScore)
                            parte = parts[p]
                            notes = parte.flat.notesAndRests.stream()
                            segmentInfo = material[s+1][p+1][d]
                            start = segmentInfo[1]
                            end = segmentInfo[2]
                            segment = notes.getElementsByOffset(start, end)
                            segment.show()
                            
    
    txt2print = '\tA\tL\tD'
        
    # Compute percentages
    for p in sorted(pairs.keys()):
        pair = pairs[p]
        if len(pair) > 0:
            total = sum(pair.values())
            if 'A' in pair.keys():
                ax = pair['A']
                ay = round(ax / (total / 100), 2)
                a = str(ax) + ' (' + str(ay) + '%)'
            else:
                a = ''
            if 'L' in pair.keys():
                fx = pair['L']
                fy = round(fx / (total / 100), 2)
                f = str(fx) + ' (' + str(fy) + '%)'
            else:
                f = ''
            if 'D' in pair.keys():
                dx = pair['D']
                dy = round(dx / (total / 100), 2)
                d = str(dx) + ' (' + str(dy) + '%)'
            else:
                d = ''
            txt = p + '\t' + a + '\t' + f + '\t' + d
            txt2print += '\n' + txt
    print('\n--------------------------------------------------')
    print('Pairwise relationship analysis results\n')
    print(txt2print)
            
    if filename != None:
        with open(filename, 'w') as f:
            f.write(txt2print)

    return dous, pairs



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


    
def floatOrFraction(strValue):
    '''str --> fractions.Fraction or float
    Given a numeric value as a string, it returns it as a fractions.Fraction
    object if contains '/' on it, or as a float otherwise
    '''
    if '/' in strValue:
        numerator = int(strValue.split('/')[0])
        denominator = int(strValue.split('/')[1])
        value = fractions.Fraction(numerator, denominator)
    elif len(strValue) == 0:
        value = None
    else:
        value = float(strValue)
        
    return value



def defineContour(pitches):
    '''
    [int] --> str
    
    I takes a list of midi pitches and returns a string defining the melodic
    contour
    A : ascending
    D : descending
    L : flat
    '''
    
    if len(pitches) == 1:
        contour = 'dL'
        
    elif len(pitches) == 2:
        if pitches[0] > pitches[1]:
            contour = 'D'
        elif pitches[0] == pitches[1]:
            contour = 'L'
        elif pitches[0] < pitches[1]:
            contour = 'A'

    elif len(pitches) > 2:
        first = pitches[0]
        last = pitches[-1]
        if first > last:
            contour = 'D'
        elif first == last:
            contour = 'L'
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
        elif contour == 'L':
            if h-first > first-l:
                contour = 'AD'
            elif first == h == l:
                contour = 'L'
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



def getTones(linesData, hd=['laosheng', 'dan'], sq=['erhuang', 'xipi'],
                    bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
                    'yuanban', 'erliu', 'liushui', 'kuaiban'], ju = ['s', 's1',
                    's2', 'x']):
    '''str, [str], [str], [str], [str] --> str
    Given the path of the linesData file, and a list of the hangdang,
    shengqiang, banshi and line type to look for, it returns a string with the
    score name and intercalated lyrics and tones for the lines found.
    '''
    with open(linesData, 'r', encoding='utf-8') as f:
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