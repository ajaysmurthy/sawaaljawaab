(function(window) {
	var app = angular.module("hamrSJ", []);

	// Controller for recorder
	app.controller("SJController", function() {
		this.appName = "SawaalJawaab";
	});

	app.controller("RecordController", ['$timeout', function($timeout) {
		this.recording = false;

		////////////////////////////////////////////////////////////////////////////

		// setting up the filesystem api
		//window.requestFileSystem = 

		// seeting up the for the recorder
		var navigator = window.navigator;
		navigator.getUserMedia = (
			navigator.getUserMedia ||
	  		navigator.webkitGetUserMedia ||
	    	navigator.mozGetUserMedia ||
	    	navigator.msGetUserMedia
			);
		var Context = window.AudioContext || window.webkitAudioContext;
		var context = new Context();

		// we need these variables for later use with the stop function
		var mediaStream;
		var rec;

		var record = function() {
                    
                    console.log("Started Recording!");
                    console.log(new Date().getTime());
                    // ask for permission and start recording
		  	navigator.getUserMedia({audio: true}, function(localMediaStream){
		    mediaStream = localMediaStream;

		    // create a stream source to pass to Recorder.js
		    var mediaStreamSource = context.createMediaStreamSource(localMediaStream);

		    // create new instance of Recorder.js using the mediaStreamSource
		    rec = new Recorder(mediaStreamSource, {
		      // pass the path to recorderWorker.js file here
		      workerPath: '/bower_components/recorderjs/recorderWorker.js'
		    });

		    // start recording
		    rec.record();
		  }, function(err){
		    console.log('Browser not supported');
		  });
		};

		var stopRec = function() {
		  // stop the media stream
		  mediaStream.stop();

		  // stop Recorder.js
		  rec.stop();
                

		  // export it to WAV
		  rec.exportWAV(function(e){
		    rec.clear();
                    
                    var fd = new FormData();
                    
                    fd.append('data', e);
                    $.ajax({
                        type: "POST",
                        url: "http://127.0.0.1:5000/upload_audio",
                        data: fd,
                        processData: false,
                        contentType: false
                    }).done(function(data) {
                        tala_info = data;
                        console.log(tala_info);
                    });
                    //console.log(e.slice(0));
		    //Recorder.forceDownload(e, "filename.wav");
		  });
		};


		///////////////////////////////////////////////////////////////////////////////////////////////////////////
		// functions for the template
		this.isRecording = function() {
			return this.recording;
		};

		this.startRecording = function() {
			console.log("Recording Button Clicked ....");
                        console.log("curretn time", nextSamaTime - new Date().getTime(), new Date().getTime());
			this.recording = true;
			$timeout(record, nextSamaTime - new Date().getTime);
		};

		this.stopRecording = function() {
			console.log("Recording Stopped ....");
			this.recording = false;
			stopRec();
		};
	}]);

	app.controller("TempoController", function() {
		this.tempo = 100;
	});
})(window);


function checkTime() {
    console.log("check time", nextSamaTime - new Date().getTime(), new Date().getTime());
}