var midi, data;
SERVERIP = "";

function onLoad(){ 
    if (navigator.requestMIDIAccess) {
        navigator.requestMIDIAccess({
            sysex: false
        }).then(onMIDISuccess, onMIDIFailure);
    } else {
        alert("No MIDI support in your browser.");
    }
}
// midi functions
function onMIDISuccess(midiAccess) {

    //setup Midi library
    MIDI.loadPlugin({
        soundfontUrl: "www/soundfont/",
        instrument: "acoustic_grand_piano",
        onprogress: function(state, progress) {
            console.log(state, progress);
        },
        onsuccess: function() {
            console.log('done loading midi library')
        }
    });



    // when we get a succesful response, run this code
    midi = midiAccess; // this is our raw MIDI data, inputs, outputs, and sysex status

    var inputs = midi.inputs.values();
    // loop over all available inputs and listen for any MIDI input
    for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
        // each time there is a midi message call the onMIDIMessage function
        input.value.onmidimessage = onMIDIMessage;
    }
}

function onMIDIFailure(error) {
    // when we get a failed response, run this code
    console.log("No access to MIDI devices or your browser doesn't support WebMIDI API. Please use WebMIDIAPIShim " + error);
}

function playImprov() {
    MIDI.Player.loadFile('/improv.mid', MIDI.Player.start

    MIDIjs.play('/improv.mid');
}

function onMIDIMessage(message) {
    data = message.data; // this gives us our [command/channel, note, velocity] data.
    //console.log('MIDI data', data); // MIDI data [144, 63, 73]
    console.log(data);
    document.getElementById("stopper").click()

    jQuery.post(SERVERIP + "/stream",
    {
          "start_time": data[0],
          "note"      : data[1],
          "velocity"  : data[2], 
    }, function(data){
    	if (data != ""){
            document.getElementById("player").click()
    	}
    });
}

