// Global variables
var currTala = $("#taal").val();
var isBlinking = false;
var beatsPT = {'teen':16, 'jhap':10, 'ek': 12, 'rupak':7};
var beatDuration =60.0/parseFloat($("#tempoControl").val());
var samaDuration = beatDuration*beatsPT[currTala];
var pulsePeriod;
var samaScheduler;
var beatScheduler;
var nextSamaTime;

var currTempo = Number($("#tempoControl").val());

function onTempoChange() {
	console.log($("#tempoControl").val());
	currTempo = Number($("#tempoControl").val());
        $.ajax({
                    type: "POST",
                    url: "http://127.0.0.1:5000/set_tempo",
                    data: JSON.stringify({'tempo': 60.0/parseFloat($("#tempoControl").val())}),
                    contentType: 'application/json',
                    dataType: 'json'
                }).done(function(data) {
                    console.log(data);
                });
                stopMetronome();
                startMetronome();
}


function onTaalChange(){
	console.log($("#taal").val());
	currTempo = Number($("#taal").val());
        $.ajax({
                    type: "POST",
                    url: "http://127.0.0.1:5000/set_taal",
                    data: JSON.stringify({'taal': $("#taal").val()}),
                    contentType: 'application/json',
                    dataType: 'json'
                }).done(function(data) {
                    console.log(data);
                });
}

function getPulsePeriod(){
    return 60.0/parseFloat($("#tempoControl").val());
    
}
function getBlinkOnSpeed() {
    
	return (60 * 1000) / (currTempo);
}

function getBlinkOffSpeed() {
	return (60 * 1000) / (currTempo);
}

function samaArrived(){
    nextSamaTime = new Date().getTime() + samaDuration * 1000;  
    $("#samaText").text("Sama");
    setTimeout(function (){$("#samaText").text("");}, 300);
}

function beatArrived(){
    
    $("#samaText").text("Beat");
    setTimeout(function (){$("#samaText").text("");}, 300);
    
}

function startMetronome() {
        
        pulsePeriod = getPulsePeriod();
        samaDuration = pulsePeriod*beatsPT[currTala];
        beatDuration = pulsePeriod;
        
        buildMetronometrack();
        playMetronomeAudio();
        
        nextSamaTime = new Date().getTime() + samaDuration * 1000;
        
        samaScheduler = setInterval(samaArrived, samaDuration*1000);
        beatScheduler = setInterval(beatArrived, beatDuration*1000);
        
}
function stopMetronome(){
    
    stopMetronomeAudio();
    clearInterval(samaScheduler);
    clearInterval(beatScheduler);
}

function offBlinker() {
	var $disp = $("#tempoView");
	$disp.html("");

	var $blinker = $("#blinker");
	$blinker.css("background-color","white");

	setTimeout(onBlinker, getBlinkOffSpeed());
}