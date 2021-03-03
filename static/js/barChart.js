function buildMetaData() {
    // sleep(2000);
    console.log("Called buildMetaData")
    d3.json("/data", function(resultData) {

        if (resultData.emotionCategories.length) {
            predictedEmotion  = resultData.predictedEmotion;
            emotionCategories = resultData.emotionCategories;
            probabilities = resultData.probabilities;
            predictedSex = resultData.predictedSex;

            // console.log(predictedEmotion)
            // console.log(emotionCategories)
            // console.log(probabilities)
            // console.log(predictedSex)
            // console.log(prob_dict)

            buildBarChart(predictedEmotion, emotionCategories, probabilities, predictedSex);

        } else {
            setTimeout(buildMetaData, 300);
        }
        // prob_dict =  probabilities.reduce(function(result, field, index) {
        //     result[emotionCategories[index]] = field;
        //     return result;
        //     }, {})


  
        // d3.select("#result").text(predictedEmotion);
        // d3.select("#cat").text(emotionCategories);
        // d3.select("#prob").text(probabilities);
        // d3.select("#sex").text(predictedSex);

    })
};

// function sleep(time) {
//     return new Promise(resolve => setTimeout(resolve, time));
//     }

function buildBarChart(predictedEmotion, emotionCategories, probabilities, predictedSex) {
    trace = [{
        x: emotionCategories,
        y: probabilities,
        type: 'bar',
        // text: `: probability chance you are ${emotionCategories}`,
        marker: {
            color: ["red", "blue", "green", "orange", "yellow", "brown", "purple"]
        }
    }]

    layout = {
        title: `We predict you are ${predictedSex} and sound ${predictedEmotion}`,
        yaxis: {
            title: "Probability of Each Emotion"
        }
    }

    Plotly.newPlot('result', trace, layout)
}