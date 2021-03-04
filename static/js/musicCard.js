

//Get reference for bootstrap card
var music = document.querySelectorAll('.music');
document.querySelectorAll('.pButton').forEach(item => {
    item.addEventListener('click', event => {
        play(event);
    })
})

//get target url for audio
function play(event) {
    var target = event.target;
    var url = d3.select(target).select('source').attr('src');
    var filename = ''
    console.log(url);
    playAudio(url)
    
    // link.href = url;
    filename = url;
    d3.json("/tv_movie", function(data) {
        buildBarChart(data[0].predictedEmotion, data[0].emotionCategories, data[0].probabilities, data[0].predictedSex)
    })
    // var xhr = new XMLHttpRequest();
    // xhr.onload = function(e) {
    //     if(this.readyState === 4) {
    //         console.log("Server accessed successfully");
    //         buildMetaData()
    //         // console.log("called BuildMetaData")
    //     }
    // };

    // var fd = new FormData();
    // fd.append("audio_data", blob, filename);
    // xhr.open("POST", "/gallery", true);
    // xhr.send(fd);    
}

//Play audio and run model
function playAudio(url) {
    new Audio(url).play();
    

  }
