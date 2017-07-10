# -*- coding: utf-8 -*-

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
