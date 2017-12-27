import markovify
import time
from mido import Message, MetaMessage, MidiFile, MidiTrack
import  random as rand
import os

queue = []
mid = MidiFile()


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

last_time = 0

f = open("major.json", 'r')
major_filetext = f.read()
major_model = markovify.NewlineText.from_json(major_filetext)

g = open("minor.json", 'r')
minor_filetext = g.read()
minor_model = markovify.NewlineText.from_json(minor_filetext)

def getNoteEvent(note):
        global last_time

        note = int(note)

        curr_time = int(round(time.time() * 1000))
        to_return = None;
        if curr_time - last_time < 500:
                queue.append(note)
                if len(queue) == 3:
                        to_return = determinechord(queue)
                        del queue[:]

        else: 
                del queue[:]

        last_time = curr_time
        return to_return

def generateOutput(chord_string):
        print "generating output"
        output = []
        chord_shift = 0
        if chord_string != "":
                ismajor = chord_string.split(':')[1]
                chord_shift = chord_string.split(':')[0]
        if ismajor:
                output = (major_model.make_sentence(test_output = False)).split()
        else:
                output = (minor_model.make_sentence(test_output = False)).split()
        

        mid = MidiFile()
        track = MidiTrack()
        track.append(MetaMessage('instrument_name', name='piano'))#accoustic grand piano

        counter = 0
        numskips = rand.randint(len(output) / 4, 3 * len(output) / 4)
        print("NUM SKIPS IS " + str(numskips))
        print("CHORD SHIFT IS " + str(chord_shift))
        for note in output:
                try:
                        (note_value, duration) = note.split('x')
                except:
                        continue
                #if counter < numskips:
                #        counter = counter + 1
                #        continue

                track.append(Message('program_change', program=12, time=0))
                if int(note_value) + int(chord_shift) > 127:
                        track.append(Message('note_on', note=0, velocity=0, time=0))
                        track.append(Message('note_off', note=0, velocity=0, time= 0/int(duration)))
                else:
                        track.append(Message('note_on', note=int(note_value) + int(chord_shift), velocity=100, time=0))
                        track.append(Message('note_off', note=int(note_value) + int(chord_shift), velocity=100, time= 650/int(duration))) 

                #counter = counter + 1
                #if counter >= 25 + numskips:
                #        print("breaking")
                #        break;

        mid.tracks.append(track)

        print("Saving improv.mid")
        print(mid.length)
        
        if not os.path.exists("app/tmp"):
            os.makedirs("app/tmp")

        mid.save("app/tmp/improv.mid")
        print "generated midi"

def determinechord(notes_list):
        print "determining chord"
        targets = [3, 4, 7, 10, 11]
        hits_hash = {}
        reduced = []
        for note in notes_list:
                reduced.append(note % 12)
        
        for note in reduced:
                hits_hash[note] = list();

        length = len(reduced)
        for note in reduced:
                third_found = False;
                seventh_found = False;
                for i in range(length):
                        diff = (reduced[i % length] - note) % 12
                        
                        if (diff in targets and not third_found) or (diff in targets and not seventh_found):
                                hits_hash[note].append(diff)
                                if diff == 10 or diff == 11:
                                        seventh_found = True;
                                elif diff == 3 or diff == 4:
                                        third_found = True;
                
        max_key = reduced[0];
        max_value = 0;
        for key in hits_hash:
                if len(hits_hash[key]) > max_value:
                        max_key = key;
                        max_value = len(hits_hash[key])

        print "done determining chord"

        return str(max_key) + ':' + str(int(3 in hits_hash[max_key])) + ':' + str(int(10 in hits_hash[max_key]))
