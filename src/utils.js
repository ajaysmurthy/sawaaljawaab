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
