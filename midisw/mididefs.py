
_NOTE_ALL =  ["c","c#","d","d#","e","f","f#","g","g#","a","a#","b"]
_NOTE_BLACK =  [1,3,6,8,10]
_NOTE_WHITE =  [0,2,4,5,7,9,11]

def note2num(note):
    if isinstance(note,int):
        if note < 0:
            ret = 0
        else:
            ret = note
    if isinstance(note,str):
        note = note.lower()
    else:
        raise TypeError("note must be an integer or string")

    return ret%128

def num2note(num):
    if isinstance(num):
        oct = int(num/12)
        note_in_oct = num % 12
        ret = _NOTE_ALL[note_in_oct] + str(oct)
    else:
        raise TypeError("num must be integer")

    return ret
