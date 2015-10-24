from __future__ import unicode_literals
from flask import Flask, request, jsonify, current_app
import requests
from functools import wraps
import sys
import os.path
import json
from flask.ext.cors import CORS
from scipy.io.wavfile import read as wavread

app = Flask(__name__)
CORS(app)

TablaStrokesPath={
'dhen': '../audio/tabla/171897__ajaysm__dhen-stroke.wav',
'dhec': '../audio/tabla/171898__ajaysm__dhec-stroke.wav',
'dhe': '../audio/tabla/171899__ajaysm__dhe-stroke.wav',
'dha': '../audio/tabla/171900__ajaysm__dha-stroke.wav',
'ka': '../audio/tabla/171901__ajaysm__ka-stroke.wav',
'ga': '../audio/tabla/171902__ajaysm__ga-stroke.wav',
'dhun': '../audio/tabla/171903__ajaysm__dhun-stroke.wav',
'dhin': '../audio/tabla/171904__ajaysm__dhin-stroke.wav',
'ta': '../audio/tabla/171905__ajaysm__na-stroke.wav',
'na': '../audio/tabla/171905__ajaysm__na-stroke.wav',
'kat': '../audio/tabla/171906__ajaysm__kat-stroke.wav',
're': '../audio/tabla/171907__ajaysm__re-stroke.wav',
'ne': '../audio/tabla/171908__ajaysm__ne-stroke.wav',
'tun': '../audio/tabla/171909__ajaysm__tun-stroke.wav',
'tak': '../audio/tabla/171910__ajaysm__tak-stroke.wav',
'tin': '../audio/tabla/171911__ajaysm__tin-stroke.wav',
'tit': '../audio/tabla/171912__ajaysm__tit-stroke.wav',
'te': '../audio/tabla/171913__ajaysm__te-stroke.wav'}

TalaInfoFULL = {
'teental': {'normal':{'bols':['dha', 'dhin', 'dhin', 'dha', 'dha', 'dhin', 'dhin', 'dha', 'dha', 'tin', 'tin', 'ta', 'ta', 'dhin', 'dhin', 'dha'],
            'durratio':[0.0, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625, 0.6875, 0.75, 0.8125, 0.875, 0.9375]},
            'roll': {'bols':['dha', 'dhin', 'dhin', 'dha', 'dha', 'dhin', 'dhin', 'dha', 'dha', 'tin', 'tin', 'ta', 'ta', 'dhin', 'dhin', 'dha'],
            'durratio':[0.0, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625, 0.6875, 0.75, 0.8125, 0.875, 0.9375]}},
'keherwa': {'normal':{'bols':['dha', 'ga', 'na', 'te', 'na', 'ka', 'dhin', 'na'],
            'durratio':[0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875],
            'prefDur':2},
            'roll': {'bols':['dha', 'dhin', 'ta', 'dha', 'dhin', 'ta', 'dha', 'dhin', 'ta'],
            'durratio':[0.0, 0.0625, 0.1875, 0.3125, 0.375, 0.5, 0.625, 0.6875, 0.8125]}},
'bhajan': {'normal':{'bols':['dhin', 'ta', 'dhin', 'dhin', 'ta', 'tin', 'ta', 'tin', 'tin', 'ta'],
            'durratio':[0.0, 0.125, 0.1875, 0.3125, 0.375, 0.5,  0.625, 0.6875,  0.8125, 0.875],
            'prefDur':4},
            'roll': {'bols':['dha', 'dhin', 'ta', 'dha', 'dhin', 'ta', 'dha', 'dhin', 'ta'],
            'durratio':[0.0, 0.0625, 0.1875, 0.3125, 0.375, 0.5, 0.625, 0.6875, 0.8125]}}
}


@app.route('/')
def index():
    return "raga phrase demo"

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

@app.route('/get_tala_info', methods=['GET', 'POST'])
@support_jsonp
def get_tala_info():
	"""
	http://127.0.0.1:5000/get_tala_info
	simple! and you get the json data :)
	"""
	return jsonify(**TalaInfoFULL)


@app.route('/upload_audio', methods=['GET', 'POST'])
@support_jsonp
def upload_audio():
	"""
	Example: http://127.0.0.1:5000/upload_audio?audio=[1,2,3]
	you have to see how to send json object, we can parse that. We might need that for passing audio arrays
	"""
	if request.method == 'POST':
		data = request.args.get('audio')
	 	print data
	return "Audio registered"




if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host= '0.0.0.0', debug = True)        