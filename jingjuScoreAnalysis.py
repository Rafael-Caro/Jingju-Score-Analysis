from music21 import *
import numpy as np
import matplotlib.pyplot as plt
import copy

def ejemplo():
    '''Creates a short phrase to be used as an example'''
    x = converter.parse("tinynotation: c4. d8 e d f16 g e d c2")
    adorno = note.Note('B3')
    adorno.duration.type = 'eighth'
    adorno = adorno.getGrace()
    x.insert(4.0, adorno)
    return x

def weightedHistogramPitchSpace(stream, width=.4, count = 'abs', figsize=None,
                                fontsize=None):
    '''(music21.stream.Score) -> matplotlib.pyplot.bar, dict
    Plots a pitch histogram for stream and returns a dictionary with
    the note classes as keys and their agregate duration as value.
    Width sets the width of the bars. Count can be set to 'abs' for
    displaying the total agregate duration of each note class, to 'sum'
    for displaying the duration normalized to the summation of all durations,
    or 'max' for displaying the duration normalized to the maximum
    duration.
    '''

    # Creating a dictionary with the all the notes in stream as keys
    # and the agregate duration for each note as values.
    noteDur = {}
    for n in stream.flat.notes:
        if n.nameWithOctave not in noteDur:
            noteDur[n.nameWithOctave] = n.quarterLength
        else:
            noteDur[n.nameWithOctave] += n.quarterLength

    # Creating an list of note clases sorted by pitch
    notes = [k for k in noteDur] # List of notes classes

    noteFreq = {} # Dictionary of notes and Hz frequencies for sorting
    for i in notes:
        noteFreq[i] = note.Note(i).frequency
    sortedNotes = sorted(noteFreq, key=noteFreq.get) # Sorted notes

    # Calculating duration values for each note class
    absValues = np.array([]) # Agragate duration for each note
    for i in sortedNotes:
        absValues = np.append(absValues, noteDur[i])
    if count == 'abs':
        values = absValues
        ylabel = 'Count'
    elif count == 'sum':
        values = absValues / sum(absValues)
        ylabel = 'Normalized Count'
    elif count == 'max':
        values = absValues / max(absValues)
        ylabel = 'Normalized Count'

    # Plotting a bar chart
    xposition = np.array([0]) # Xticks' positions separated by intervals
    for i in range(len(sortedNotes)-1):
        n1 = note.Note(sortedNotes[i])
        n2 = note.Note(sortedNotes[i+1])
        step = interval.notesToChromatic(n1, n2).directed
        xposition = np.append(xposition, xposition[-1] + step)

    plt.figure(1, figsize)
    plt.bar(xposition, values, width)
    plt.title('Weighted Histogram of Pitch Space', fontsize=fontsize)
    plt.xlabel('Pitch', fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if fontsize != None:
        plt.xticks(xposition + width/2, sortedNotes, fontsize=(fontsize*0.6))
    else:
        plt.xticks(xposition + width/2, sortedNotes)
    plt.grid(True, axis='y')
    plt.show()

    return noteDur

def intervalHistogram(stream, width=.4, directed=False, count='abs',
                      figsize=None, fontsize=None):
    '''(music21.stream.Score) -> matplotlib.pyplot.bar, dict
    Plots a histograms of the intervals found in stream and returns a
    dictionary with the interval classes as keys and their total count
    as values.
    '''
    notes = stream.flat.notesAndRests
    
    # Creating a dictionary with the interval classes as keys and their
    # count as values
    intCount = {}
    for i in range(len(notes)-1):
        if isinstance(notes[i], note.Note) and isinstance(notes[i+1],
                                                          note.Note):
            intl = interval.notesToInterval(notes[i], notes[i+1])
            if directed:
                intName = intl.directedName
            else:
                intName = intl.name
                
            if intName not in intCount:
                intCount[intName] = 1
            else:
                intCount[intName] += 1

    # Creating lists for computing the plot:
    # Interval classes to be displayed
    intClasses = [k for k in intCount]

    # Sorting interval classes according to their semitones steps
    intSteps = {}
    for i in intClasses:
        intSteps[i] = interval.Interval(i).chromatic.directed
    sortedInt = sorted(intSteps, key=intSteps.get)

    # (Normalized) count values to be displayed
    intValues = np.array([intCount[i] for i in sortedInt])
    if count == 'abs':
        ylabel = 'Count'
    elif count == 'sum':
        intValues = intValues / float(sum(intValues))
        ylabel = 'Normalized Count'
    elif count == 'max':
        intValues = intValues / float(max(intValues))
        ylabel = 'Normalized Count'

    # Position of xticks, separated for semitones steps
    xposition = np.array(sorted([intSteps[i] for i in sortedInt]))

    # Plotting the bar chart
    plt.figure(1, figsize)
    plt.bar(xposition, intValues, width)
    plt.title('Histogram of Intervals', fontsize=fontsize)
    plt.xlabel('Interval class', fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.xticks(xposition + width/2, sortedInt, fontsize=(fontsize*.6))
    plt.grid(True, axis='y')
    plt.show()

    return intCount

def findIntervalsPosition(stream, intl, directed=False):
    '''(music21.stream.Score, str) ->
    Finds the offset for each pair of notes separated by interval intl in sream.
    '''

    # Create a copy of the stream, so that notes color can be changed
    # without affecting the original stream
    score = copy.deepcopy(stream)

    # Get the notes and rests from score
    notes = score.flat.notesAndRests

    # Create a list with the offset positions of the intervals
    positions = []
    for i in range(len(notes)-1):
        n1 = notes[i]
        n2 = notes[i + 1]
        if isinstance(n1, note.Note) and isinstance(n2, note.Note):
            intlCand = interval.notesToInterval(n1, n2)
            if directed:
                intName = intlCand.directedName
            else:
                intName = intlCand.name

            # Change the color of the interval notes
            if intName == intl:
                n1.color = 'red'
                n2.color = 'red'
                pair = {n1.nameWithOctave:n1.offset, n2.nameWithOctave:
                        n2.offset}
                positions.append(pair)

    if len(positions) != 0:
        score.show()

    return positions

def beatCountPerNote(pitchClass, stream, showScore=True):
    working_stream = copy.deepcopy(stream)
    notes = working_stream.flat.notes
    found_notes = []
    for n in notes:
        if n.name == pitchClass:
            n.color = 'red'
            found_notes.append(n)
    if len(found_notes) == 0:
        return 'The given pitch class does not appear in the given stream.'
    else:
        beat_dic = {}
        for n in found_notes:
            beat_class = n.beat # This number has to be changed to the time signature's numerator
            if beat_class not in beat_dic:
                beat_dic[beat_class] = 1
            else:
                beat_dic[beat_class] += 1

#    return found_notes

    beat_classes = [i for i in beat_dic]
    beat_classes.sort()
    beat_values = [beat_dic[i] for i in beat_classes]
    beat_ticks = [str(i) for i in beat_classes]

#    plt.bar(beat_classes, yvalues, width)
#    plt.xticks(np.array(beat_classes) + width/2, xticks)
#    plt.show()

    if showScore:
        working_stream.show()

    return beat_classes, beat_values, beat_ticks

def beatHistogram(stream, tonic=None, width=.4, rotation=45, figsize=None,
                  fontsize=None):
    pitches = []
    for n in stream.flat.notes:
        if n.name not in pitches:
            pitches.append(n.name)

    # Organize pitches starting from the given tonic, if any
    pitches.sort()
    if tonic != None:
        ton_ind = pitches.index(tonic)
        pitch_classes = pitches[ton_ind:]
        pitch_classes.extend(pitches[:ton_ind])
    else:
        pitch_classes = pitches

    plots = len(pitch_classes)
    rows = (plots / 2) + (plots % 2)
    rowsAndCol = rows * 100 + 20

    # Setting the y margin
    maxima = []
    for i in pitch_classes:
        x, y, t = beatCountPerNote(i, stream, showScore=False)
        maxima.append(max(y))
    ylim = max(maxima)

    fig = plt.figure(figsize=figsize)
    ax0 = fig.add_subplot(111)
    for i in ['top', 'bottom', 'left', 'right']:
        ax0.spines[i].set_color('none')
    ax0.tick_params(labelcolor='w', top='off', bottom='off', left='off',
                    right='off')
    ax0.set_xlabel('Beat', fontsize=fontsize)
    ax0.set_ylabel('Count', fontsize=fontsize)
    for i in range(len(pitch_classes)):
        x, y, t = beatCountPerNote(pitch_classes[i], stream, showScore=False)
        ax = fig.add_subplot(rowsAndCol + i + 1)
        ax.bar(x, y, width=width)
        ax.set_ylim(0, ylim)
        ax.set_xlim(1, 3)
#        ax.yaxis.set_ticks(np.arange(0, ylim, 3))
        ax.set_xticks(np.array(x) + width/2)
        ax.set_xticklabels(t, rotation=rotation)
        ax.set_title(pitch_classes[i], fontsize=(fontsize*.75))
        ax.grid(True, axis='y')

    fig.tight_layout()
    plt.show()
    
def timeSignatureMeasures(timeSignature, source):
    '''(str, music21.stream) --> list of lists
    Returns a list of lists containing the start measure number and the end measure number
    for each section in source that is set to timesignature
    '''
    timeSignatures = source.flat.getTimeSignatures()
    measureNumbers = []
    for i in timeSignatures:
        if i.ratioString == timeSignature:
            ini = i.measureNumber
            end = timeSignatures[timeSignatures.index(i)+1].measureNumber-1
            measureNumbers.append([ini, end])

    return measureNumbers
    
def getSectionByTimeSignature(timeSignatureList, source):
    '''(list, music21.stream) --> music21.stream
    Given a list conatining lists with the start measure number and the end measure number
    for each section in a specific time Signature, it returns a stream containing all
    those sections from source
    '''
    section = stream.Stream()
    for i in timeSignatureList:
        for j in source.measures(i[0], i[1]).getElementsByClass('Measure'):
            section.append(j)

    return section

def beatAnalysis(stream, beatList, tonic=None, width=.4, figsize=None,
                 fontsize=None):
    
    beats = {}
    for n in stream.flat.notes:
        if n.duration.quarterLength > 0:
            if n.name not in beats:
                beats[n.name] = [n.beat]
            else:
                beats[n.name].append(n.beat)

    count = {}
    for i in beats:
        count[i] = []
        for j in beatList:
            count[i].append(beats[i].count(j))

    pitches = [i for i in beats]

    # Organize pitches starting from the given tonic, if any
    pitches.sort()
    if tonic != None:
        ton_ind = pitches.index(tonic)
        pitch_classes = pitches[ton_ind:]
        pitch_classes.extend(pitches[:ton_ind])
    else:
        pitch_classes = pitches

    #return beats, count, pitch_classes

    ind = np.arange(len(beatList))
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    bottom = np.zeros(len(ind))

    plots = []
    for i in range(len(pitch_classes)):
        height = count[pitch_classes[i]]
        plots.append(plt.bar(ind, height, width, bottom=bottom,
                color=colors[i]))
        bottom += height
    plt.xticks(ind+width/2., [str(i) for i in beatList])
    plt.legend(plots, pitch_classes)

    plt.show()
