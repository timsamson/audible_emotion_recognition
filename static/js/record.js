function recordAudio(thing) {
    console.log("start record");
    thing.disabled = true;
    stopRecord.disabled = false;
    audioChunks = [];
    rec.start();
}

function stopAudioRecord(thing) {
    console.log("stop record");
    record.disabled = false;
    thing.disabled = true;
    rec.stop();
}

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);

        if (rec.state == "inactive"){
            let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
            recordedAudio.src = URL.createObjectURL(blob);
            recordedAudio.controls = true;
            recordedAudio.autoplay = false;
            sendData(blob);
        }
    }
}

function sendData(data) {}

navigator.mediaDevices.getUserMedia({audio: true})
    .then(stream => {handlerFunction(stream)});
