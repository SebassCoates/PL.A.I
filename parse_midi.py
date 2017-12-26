import sys
import mido
#sys.path.append("/tmp/python-midi-master")
#import midi

#pattern = midi.read_midifile("IALikeBeingInLove.mid")
# print pattern

from mido import MidiFile

#this is a comment

def parse_notes(filename, complete_notes):
    notes = MidiFile(filename)
    
    tempo = 500000

    root = 0

    mode = 'major'

    channels = []
    
    started_notes = [];

    from collections import namedtuple
    Started_node = namedtuple("Started_node", "channel note start_time")

    rest_timer = -1
    
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
                if (msg.note - root > 55):
                    sn = Started_node(msg.channel, msg.note - root, time)
                    started_notes.append(sn)
                elif (rest_timer > 0):
                    cn = Complete_node(128, rest_timer, time - rest_timer, mode)
                    if (cn.duration != 0):
                        complete_notes[:].append(cn)
                    rest_timer = -1
            else:
                for sn in started_notes:
                    if (sn.channel == msg.channel and sn.note == msg.note - root):
                        cn = Complete_node(sn.note, sn.start_time, time - sn.start_time, mode)
                        if (cn.duration != 0):
                            try:
                                index = channels.index(msg.channel)
                                complete_notes[index].append(cn)
                            except:
                                channels.append(msg.channel)
                                complete_notes.append([])
                                complete_notes[-1].append(cn)
                        started_notes.remove(sn)
                        if (len(started_notes) == 0):
                            rest_timer = time
                        break

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

        
        next_measure = 8 * tempo
       

        for channel in complete_notes:
            from operator import itemgetter
            channel.sort(key=itemgetter(1))
            for cn in channel:

                # sort by start_time

                value = (int) (2 / (cn.duration / tempo))
                i = 0
                if (value == 0):
                    continue
                while (value >= (1 << i)):
                    i += 1
                i -= 1
                value = 1 << i
                if (value < 50):
                    code_word = str(cn.note) + "x" + str(value)
                    if (cn.mode == 'major'):
                        fmajor.write(code_word + ' ')
                    elif (cn.mode == 'minor'):
                        fminor.write(code_word + ' ')
                if (cn.start_time > next_measure):
                    if (cn.mode == 'major'):
                        fmajor.write("\n")
                    else:
                        fminor.write("\n")
                    next_measure += 8 * tempo

    except:
        KeyError


fmajor.close()
fminor.close()
