function buildCharts(){
    buildMetaData();

}

function buildMetaData(result) {
    d3.json("/data", function(resultData) {
        buildData(result)
        predictedEmotion  = [];
        emotionCategories = [];
        probabilities = [];
        predictedSex = [];

        resultData.forEach(function(data) {
            predictedEmotion.push(data[0]);
            emotionCategories.push(data[1]);
            probabilities.push(data[3]);
            predictedSex.push(data[2]);
            });

        console.log(predictedEmotion)
        console.log(emotionCategories)
        console.log(probabilities)
        console.log(predictedSex)

        
    });   
}



