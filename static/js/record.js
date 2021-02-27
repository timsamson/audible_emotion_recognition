/*  
    Creates audio files to test with machine learning model.
    Adapted from Jeremy Gottfried's tutorial: 
        https://medium.com/jeremy-gottfrieds-tech-blog/javascript-tutorial-record-audio-and-encode-it-to-mp3-2eedcd466e78

    and Recorder.js:
        https://github.com/addpipe/simple-recorderjs-demo/blob/master/js/app.js
*/

URL = window.URL || window.webkitURL;
var gumStream;

var rec;

var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;

function startAudioRecord() { 
    console.log("startRecord button clicked"); 

    startRecord.disabled = true;
    stopRecord.disabled = false;

    navigator.mediaDevices.getUserMedia({audio: true}).then(function(stream) {
        console.log("Initializing Recorder.js ..."); 
        
        gumStream = stream;

        input = audioContext.createMediaStreamSource(stream);

        // Create the Recorder object
        rec = new Recorder(input, {
            numChannels: 1
        }) 
        // Start recording 
        rec.record()
        console.log("Recording started");

    }).catch(function(err) {
        // Enable the record button if getUserMedia() fails 
        startRecord.disabled = false;
        stopRecord.disabled = true;
        });
}

function stopAudioRecord() {
    console.log("stopRecord button clicked");
    //disable the stop button, enable the record too allow for new recordings 
    stopRecord.disabled = true;
    startRecord.disabled = false;
    //tell the recorder to stop the recording 
    rec.stop(); //stop microphone access 
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink 
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
    var url = URL.createObjectURL(blob);
    var li = document.createElement('li');
    var audioPlayback = document.createElement('audio');
    var link = document.createElement('a');

    audioPlayback.controls = true;
    audioPlayback.src = url;

    link.href = url;
    link.download = new Date().toISOString() + '.wav';
    link.innerHTML = link.download;

    li.appendChild(audioPlayback);
    li.appendChild(link);

    recordingsList.appendChild(li);
}