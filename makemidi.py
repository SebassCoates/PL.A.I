import mido


from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

#MetaMessage('set_tempo', tempo=2000000)

#track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=64, velocity=64, time=1))
track.append(Message('note_on', note=64, velocity=0, time=1))

track.append(Message('note_on', note=68, velocity=64, time=1))
track.append(Message('note_on', note=68, velocity=0, time=1))


track.append(Message('note_on', note=64, velocity=64, time=1))
track.append(Message('note_on', note=64, velocity=0, time=1))


track.append(Message('note_on', note=64, velocity=64, time=1))
track.append(Message('note_on', note=64, velocity=0, time=1))


track.append(Message('note_on', note=64, velocity=64, time=1))
track.append(Message('note_on', note=64, velocity=0, time=1))


# 5
track.append(Message('note_on', note=64, velocity=64, time=2))
track.append(Message('note_on', note=64, velocity=0, time=2))

track.append(Message('note_on', note=64, velocity=64, time=2))
track.append(Message('note_on', note=64, velocity=0, time=2))

track.append(Message('note_on', note=64, velocity=64, time=2))
track.append(Message('note_on', note=64, velocity=0, time=2))

track.append(Message('note_on', note=64, velocity=64, time=2))
track.append(Message('note_on', note=64, velocity=0, time=2))

track.append(Message('note_on', note=64, velocity=64, time=4))
track.append(Message('note_on', note=64, velocity=0, time=4))

track.append(Message('note_on', note=64, velocity=64, time=4))
track.append(Message('note_on', note=64, velocity=0, time=4))



mid.save('new_song.mid')

