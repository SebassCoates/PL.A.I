import sys
import mido
#sys.path.append("/tmp/python-midi-master")
#import midi

#pattern = midi.read_midifile("IALikeBeingInLove.mid")
# print pattern

from mido import MidiFile


def parse_notes(filename, complete_notes):
    notes = MidiFile(filename)
    
    tempo = 500000

    root = 0

    mode = 'major'

    note_timer = -1
    note_value = 128
    
    time = 0
    for msg in notes:
        if (not msg.is_meta):
            time += msg.time #* notes.ticks_per_beat
        elif (msg.type == 'key_signature'):
            key = msg.key
            if (key[0:1] == 'Db' or key[0:1] == 'C#'):
                root = 1
            elif (key[0] == 'D'):
                root = 2
            elif (key[0:1] == 'D#' or key[0:1] == 'Eb'):
                root = 3
            elif (key[0] == 'E'):
                root = 4
            elif (key[0] == 'F'):
                root = 5
            elif(key[0:1] == 'Gb' or key[0:1] == 'F#'):
                root = 6
            elif (key[0] == 'G'):
                root = 7
            elif (key[0:1] == 'Ab' or key[0:1] == 'G#'):
                root = 8
            elif (key[0] == 'A'):
                root = 9
            elif (key[0:1] == 'A#' or key[0:1] == 'Bb'):
                root = 10
            elif (key[0] == 'B'):
                root = 11
            try:
                if (key[1] == 'm' or key[2] == 'm'):
                    mode = 'minor'
            except:
                IndexError
            try:
                mode = msg.mode
            except:
                AttributeError
        
        elif (msg.type == 'set_tempo'):
            tempo = msg.tempo


        try:
            if (msg.velocity != 0):
                if (note_timer > 0):
                    cn = Complete_node(note_value, note_timer, time - note_timer, mode)
                    if (cn.duration != 0):
                        complete_notes.append(cn)
                note_timer = time
                note_value = msg.note - root
            else:
                if (msg.note - root == note_value):
                    cn = Complete_note(note_value, note_timer, timer - note_timer, mode)
                    if (cn.duration != 0):
                        complete_notes.append(cn)
                    note_value = 128
                    note_timer = time
                        

        except:
            AttributeError

    return tempo / 1000000.0



filenames = sys.argv


from collections import namedtuple
Complete_node = namedtuple("Complete_node", "note start_time duration mode")

fmajor = open('major.mff', 'w')
fminor = open('minor.mff', 'w')

for filename in filenames:
    if (filename == 'parse_midi.py'):
        continue
    
    complete_notes = []
    try:
        tempo = parse_notes(filename, complete_notes)

        # sort by start_time
        from operator import itemgetter
        complete_notes.sort(key=itemgetter(1))
        
        next_measure = 8 * tempo
        
        for sn in complete_notes:
            value = (int) (2 / (sn.duration / tempo))
            i = 0
            if (value == 0):
                continue
            while (value >= (1 << i)):
                i += 1
            i -= 1
            value = 1 << i
            if (value < 50):
                code_word = str(sn.note) + "x" + str(value)
                if (sn.mode == 'major'):
                    fmajor.write(code_word + ' ')
                elif (sn.mode == 'minor'):
                    fminor.write(code_word + ' ')
            if (sn.start_time > next_measure):
                if (sn.mode == 'major'):
                    fmajor.write("\n")
                else:
                    fminor.write("\n")
                next_measure += 8 * tempo
    except:
        KeyError


fmajor.close()
fminor.close()
