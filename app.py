#!/usr/bin/python3
# app.py
# purp: to create a full user-responsive, web server that can run various programs off several platforms including LEGO EV3
# last updated: by Ahmed Gado, D. Nguyen, J. Basso, Kevin Destin, Donna Chen

from flask import Flask, request, render_template, send_from_directory, send_file
from time import sleep
from gevent import monkey
monkey.patch_all()
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
from multiprocessing import Process
import os.path
import sys
import io
from flask_cors import CORS
import backend
import json

chordCount = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# this directory contains the projects that can be accessed by the user
DIR_ROOT = APP_ROOT + '/Projects'


# defining webpages and resources (CSS, images etc.) to be in /www folder makes the coding easier
app = Flask(__name__, template_folder="www", static_folder="www")
CORS(app)
app.config['UPLOAD_FOLDER'] = DIR_ROOT
socketio = SocketIO(app, engineio_logger=False, ping_timeout=30)

@app.route('/', methods=["GET"])
def index():
    return render_template('plai.html')

@app.route('/stream', methods=["POST"])
def processNote():
    chordString = backend.getNoteEvent((request.form["note"]))
    if chordString != None:
        backend.generateOutput(chordString)
       	return "CLICK THAT!!!"

    return ""


@app.route('/improv.mid', methods=["GET"])
def renderMidi():
        chordCount += 1
        print "sending midi file"
        if os.path.exists('app/tmp/improv.mid' + str(chordCount)):
            print "valid path for midi file"
        else:
            print "invalid path for midi file"
	return send_file('app/tmp/improv.mid' + str(chordCount))

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=8000)
