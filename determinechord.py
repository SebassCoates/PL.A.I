targets = [3, 4, 7, 10, 11]

def determinechord(notes_list):
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

#print()
#notes_list = [0,4,10]
#print(determinechord(notes_list))

#print()
#notes_list = [0,10,4]
#print(determinechord(notes_list))

#print()
#notes_list = [4,0,11]
#print(determinechord(notes_list))

#print()
#notes_list = [4,11,0]
#print(determinechord(notes_list))

#print()
#notes_list = [10,3,0]
#print(determinechord(notes_list))

#print()
#notes_list = [11,0,3]
#print(determinechord(notes_list))

#print()
#notes_list = [0,1,2]
#print(determinechord(notes_list))

#print()
#notes_list = [1,2,0]
#print(determinechord(notes_list))

#print()
#notes_list = [0,1,2]
#print(determinechord(notes_list))