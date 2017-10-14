import sys
import mido
#sys.path.append("/tmp/python-midi-master")
#import midi

#pattern = midi.read_midifile("IALikeBeingInLove.mid")
# print pattern

from mido import MidiFile

def parse_notes(filename, complete_notes):
    notes = MidiFile(filename)

    root = 0
    
    started_notes = [];

    from collections import namedtuple
    Started_node = namedtuple("Started_node", "channel note start_time")

    time = 0
    # counter = 0
    for msg in notes:
        if (not msg.is_meta):
            time += msg.time
        elif (msg.type == 'key_signature'):
            key = msg.key
            if (key == 'Db' or key == 'C#'):
                root = 1
            elif (key == 'D'):
                root = 2
            elif (key == 'D#' or key == 'Eb'):
                root = 3
            elif (key == 'E'):
                root = 4
            elif (key == 'F'):
                root = 5
            elif(key == 'Gb' or key == 'F#'):
                root = 6
            elif (key == 'G'):
                root = 7
            elif (key == 'Ab' or key == 'G#'):
                root = 8
            elif (key == 'A'):
                root = 9
            elif (key == 'A#' or key == 'Bb'):
                root = 10
            elif (key == 'B'):
                root = 11
        
        elif (msg.type == 'set_tempo'):
            tempo = msg.tempo

        rest_timer = -1

        try:
            if (msg.velocity != 0):
                if (rest_timer > 0):
                    cn = Complete_node(128, rest_timer, time - rest_timer)
                    rest_timer = -1
                sn = Started_node(msg.channel, msg.note - root, time)
                started_notes.append(sn)
            else:
                for sn in started_notes:
                    if (sn.channel == msg.channel and sn.note == msg.note - root):
                        cn = Complete_node(sn.note, sn.start_time, time - sn.start_time)
                        if (cn.duration != 0):
                            complete_notes.append(cn)
                        started_notes.remove(sn)
                        # print cn
                        if (len(started_notes) == 0):
                            rest_timer = time
                        break

        except:
            AttributeError
    
    return tempo / 1000000.0



filenames = sys.argv

from collections import namedtuple
Complete_node = namedtuple("Complete_node", "note start_time duration")


for filename in filenames:
    if (filename == 'parse_midi.py'):
        continue
    
    complete_notes = [];
    tempo = parse_notes(filename, complete_notes)

    
    
    # sort by start_time
    from operator import itemgetter
    complete_notes.sort(key=itemgetter(1))
    
    
    for sn in complete_notes:
        print("duration")
        print sn.duration
        print("duration / tempo")
        print sn.duration / tempo
        print("value of note")
        print (int) (4 / (sn.duration / tempo))
        code_word = str(sn.note) + ":" + str(4 / (sn.duration / tempo))
        #print code_word
        #machinely_learn(code_word)

    print tempo


#print("all done")
