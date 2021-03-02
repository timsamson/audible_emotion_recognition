function buildMetaData() {
    sleep(2000);
    d3.json("/data", function(resultData) {
        predictedEmotion  = resultData.predictedEmotion;
        emotionCategories = resultData.emotionCategories;
        probabilities = resultData.probabilities;
        predictedSex = resultData.predictedSex;

        prob_dict =  probabilities.reduce(function(result, field, index) {
            result[emotionCategories[index]] = field;
            return result;
            }, {})

        console.log(predictedEmotion)
        console.log(emotionCategories)
        console.log(probabilities)
        console.log(predictedSex)
        console.log(prob_dict)
  
        d3.select("#result").text(predictedEmotion);
        d3.select("#cat").text(emotionCategories);
        d3.select("#prob").text(probabilities);
        d3.select("#sex").text(predictedSex);

    })
};

function sleep(time) {
    return new Promise(resolve => setTimeout(resolve, time));
    }

