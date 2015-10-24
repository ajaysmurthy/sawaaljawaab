//global variables
var audio_context;
var isPlaying = false;
var source1;
var nChannels = 1;
var tabla_strokes;
var audioBuffer;
var sampleRate;
var theka = 'teental';
var total_out_dur;
var tala_info;
var playSound;


function setBarLength(length){
    barLength = length
}

function setTheka(theka_inp){
    theka = theka_inp;
}


// fetching dictionary of sounds
var getSound = new XMLHttpRequest();
getSound.open("GET", "http://127.0.0.1:5000/get_tabla_sounds", true);
getSound.send();
getSound.onreadystatechange = function() {
    if (getSound.readyState == 4 && getSound.status == 200) {
        tabla_strokes = JSON.parse(getSound.responseText);
    }
}

//fetch tala information
var getTala = new XMLHttpRequest();
getTala.open("GET", "http://127.0.0.1:5000/get_tala_info", true);
getTala.send();
getTala.onreadystatechange = function() {
    if (getTala.readyState == 4 && getTala.status == 200) {
        tala_info = JSON.parse(getTala.responseText);
    }
}


function buildTheka(){
    total_out_dur = tala_info.strokeTime[tala_info.strokeTime.length-1] + 2;
    var frameCount = sampleRate*total_out_dur;
    audioBuffer = audio_context.createBuffer(nChannels, frameCount, sampleRate);
    for (var channel = 0 ; channel < nChannels; channel ++){
        var nowBuffering = audioBuffer.getChannelData(channel);
    
        var len_stroke;
        for (var bol_ind in tala_info.strokeTime){
            start = Math.floor(tala_info.strokeTime[bol_ind]*sampleRate);
            len_stroke = tabla_strokes[tala_info.strokeList[bol_ind]].length
            for (var ii = 0; ii < len_stroke; ii++){
                nowBuffering[start + ii] = nowBuffering[start + ii] + tala_info.strokeAmp[bol_ind]*tabla_strokes[tala_info.strokeList[bol_ind]][ii]/32767.0;
            }
        }
    }
}

function playTheka(inp){
    if (isPlaying == true){
            stopPlaying();
    }
    playSound = audio_context.createBufferSource();
    playSound.buffer = audioBuffer;
    playSound.connect(audio_context.destination);
    playSound.loop = true;
    playSound.start(0);  
    isPlaying = true;
};

function stopPlaying(){
    if (isPlaying == true){
        playSound.stop();
        isPlaying = false;        
    }
    
};

// Function that initializes the audio context
function init() {
    try {
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;
      
      audio_context = new AudioContext();      
    } catch (e) {
      alert('No web audio support in this browser!');
    }
    sampleRate = audio_context.sampleRate;
    onBlinker();
    
};



