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
}

var currTala = $("#taal").val();
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

function getBlinkOnSpeed() {
	return (60 * 1000) / (currTempo);
}

function getBlinkOffSpeed() {
	return (60 * 1000) / (currTempo);
}

function onBlinker() {

	var $disp = $("#tempoView");
	$disp.html("Beat");

	var $blinker = $("#blinker");
	$blinker.css("background-color","white");

	setTimeout(offBlinker, getBlinkOnSpeed());
}

function offBlinker() {
	var $disp = $("#tempoView");
	$disp.html("");

	var $blinker = $("#blinker");
	$blinker.css("background-color","white");

	setTimeout(onBlinker, getBlinkOffSpeed());
}