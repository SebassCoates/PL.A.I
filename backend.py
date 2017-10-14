import markovify
import time

queue = []

last_time = 0

f = open("major.json", 'r')
major_filetext = f.read()
major_model = markovify.NewlineText.from_json(major_filetext)

g = open("minor.json", 'r')
minor_filetext = g.read()
minor_model = markovify.NewlineText.from_json(minor_filetext)

def initialize():
        print(minor_model)
        print(major_model)

def getNodeEvent(note):
        curr_time = int(round(time.time() * 1000))
        to_return = None;
        if curr_time - last_time < 50:
                queue.append(note.note)
        else: 
                to_return = determinechord(queue)
                del queue[:]

        last_time = curr_time
        return to_return

def generateOutput(ismajor):
        if ismajor:
                return(major_model.make_sentence(test_output = False))

        return(minor_model.make_sentence(test_output = False))

def determinechord(notes_list):
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

        return str(max_key) + ':' + str(int(3 in hits_hash[max_key])) + ':' + str(int(10 in hits_hash[max_key]))