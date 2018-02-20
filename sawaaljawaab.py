from __future__ import unicode_literals
from flask import Flask, request, jsonify, current_app
from functools import wraps
import sys
import os
import json
from flask.ext.cors import CORS
from scipy.io.wavfile import read as wavread
import inspect
import sys
from src import tablaAnalysis as anal

PULSEP = 0.5
TAAL_ID = "teen"   # 1 for teental, 2 for ektaal, 3 for rupak taal, 4 for jhap taal

app = Flask(__name__)
CORS(app)

TablaStrokesPath = json.load(open('../dataset/filelist.json', 'r'))

clickStrokes = {'hiClick': '../dataset/hiclick.wav', 'lowClick': '../dataset/loclick.wav'}

@app.route('/')
def index():
    return "thing"

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args, **kwargs)) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)

    return decorated_function    

@app.route('/get_tabla_sounds', methods=['GET', 'POST'])
@support_jsonp
def get_tabla_sounds():
    """
    http://127.0.0.1:5000/get_tabla_sounds
    simple! and you get the json data :)
    """
    #read a wav sound
    output = {}
    for stroke in TablaStrokesPath.keys():
        fs, data = wavread(TablaStrokesPath[stroke])
        output[stroke] = data.tolist()
    return jsonify(**output)

@app.route('/get_click_sounds', methods=['GET', 'POST'])
@support_jsonp
def get_click_sounds():
    """
    http://127.0.0.1:5000/get_tabla_sounds
    simple! and you get the json data :)
    """
    #read a wav sound
    output = {}
    for stroke in clickStrokes.keys():
        fs, data = wavread(clickStrokes[stroke])
        output[stroke] = data.tolist()
    return jsonify(**output)


@app.route('/get_tala_info', methods=['GET', 'POST'])
@support_jsonp
def get_tala_info():
    """
    http://127.0.0.1:5000/get_tala_info
    simple! and you get the json data :)
    """
    
    TalaInfoFULL = json.load(open('../dataset/exampleOutput.json', 'r'))
    return jsonify(**TalaInfoFULL)

@app.route('/set_tempo', methods=['GET', 'POST'])
@support_jsonp
def set_tempo():
    """
    """
    global PULSEP
    if request.method == 'POST':
        PULSEP =  request.get_json()['tempo']
    #tempo = float(request.args.get('tempo'))
    return jsonify(**{'status': True, 'tempo': PULSEP})

@app.route('/set_taal', methods=['GET', 'POST'])
@support_jsonp
def set_taal():
    """
    """
    global TAAL_ID
    if request.method == 'POST':
        TAAL_ID =  request.get_json()['taal']
    return jsonify(**{'status': True, 'taal': TAAL_ID})

@app.route('/upload_audio', methods=['GET', 'POST'])
@support_jsonp
def upload_audio():
    """
    Example: http://127.0.0.1:5000/upload_audio?audio=[1,2,3]
    you have to see how to send json object, we can parse that. We might need that for passing audio arrays
    """
    if request.method == 'POST':
        blob = request.files['data']
        blob.save('temp.wav')
        audio = anal.ess.MonoLoader(filename = 'temp.wav')()
        featFull, strokeSeq, strokeTime, strokeAmp, opulsePer = anal.getJawaabLive(audio, PULSEP, iTaal = TAAL_ID)
        output = {'strokeTime': strokeTime.tolist(), 'strokeAmp': strokeAmp.tolist(), 'strokeList': strokeSeq}
    return jsonify(**output)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host= '0.0.0.0', debug = True)        