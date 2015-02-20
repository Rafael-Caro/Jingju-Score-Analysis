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

def weightedHistogramPitchSpace(stream, width = 0.4, count = 'abs'):
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

    plt.bar(xposition, values, width)
    plt.title('Weighted Histogram of Pitch Space')
    plt.ylabel(ylabel)
    plt.xticks(xposition + width/2, sortedNotes)
    plt.show()

    return noteDur

def intervalHistogram(stream, width = 0.4, directed=False, count='abs'):
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
    plt.bar(xposition, intValues, width)
    plt.title('Intervals Histogram')
    plt.ylabel(ylabel)
    plt.xticks(xposition + width/2, sortedInt)
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
            beat_class = n.beat # This number has tu be changed to the time signature's numerator
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

def beatHistogram(stream, tonic=None, width=0.1, rotation=45):
    pitch_classes = []
    for n in stream.flat.notes:
        if n.name not in pitch_classes:
            pitch_classes.append(n.name)

    plots = len(pitch_classes)
    rows = (plots / 2) + (plots % 2)
    rowsAndCol = rows * 100 + 20

    # Setting the y margin
    maxima = []
    for i in pitch_classes:
        x, y, t = beatCountPerNote(i, stream, showScore=False)
        maxima.append(max(y))
    ylim = max(maxima)

    fig = plt.figure()
    for i in range(len(pitch_classes)):
        x, y, t = beatCountPerNote(pitch_classes[i], stream, showScore=False)
        ax = fig.add_subplot(rowsAndCol + i)
        ax.bar(x, y, width)
        ax.set_ylim(0, ylim)
        ax.set_xlim(1, 3)
        ax.set_xticks(np.array(x) + width/2)
        ax.set_xticklabels(t, rotation=rotation)
        ax.set_title(pitch_classes[i])

    fig.tight_layout()
    plt.show()
    
