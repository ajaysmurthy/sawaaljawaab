var currTempo = Number($("#tempoControl").val());

function onTempoChange() {
	console.log($("#tempoControl").val());
	currTempo = Number($("#tempoControl").val());
}

function getBlinkSpeed() {
	return (60 * 1000) / (2 * currTempo);
}
function onBlinker() {

	var $disp = $("#tempoView");
	$disp.html("||||");

	var $blinker = $("#blinker");
	$blinker.css("background-color","red");

	setTimeout(offBlinker, getBlinkSpeed());
}

function offBlinker() {
	var $disp = $("#tempoView");
	$disp.html("");

	var $blinker = $("#blinker");
	$blinker.css("background-color","white");

	setTimeout(onBlinker, getBlinkSpeed());
}
