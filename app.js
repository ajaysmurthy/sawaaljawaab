(function(window) {
	var app = angular.module("hamrSJ", []);

	// Controller for recorder
	app.controller("SJController", function() {
		this.appName = "SawaalJawaab";
	});

	app.controller("RecordController", function() {
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
		    Recorder.forceDownload(e, "filename.wav");
		  });
		};


		///////////////////////////////////////////////////////////////////////////////////////////////////////////
		// functions for the template
		this.isRecording = function() {
			return this.recording;
		};

		this.startRecording = function() {
			console.log("Recording Started ....");
			this.recording = true;
			record();
		};

		this.stopRecording = function() {
			console.log("Recording Stopped ....");
			this.recording = false;
			stopRec();
		};
	});

	app.controller("TempoController", function() {
		this.tempo = 100;
	});
})(window);