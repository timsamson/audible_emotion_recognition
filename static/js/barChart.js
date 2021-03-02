function buildMetaData(result) {
    d3.json("/data", function(resultData) {
        buildData(result)
        predictedEmotion  = [];
        emotionCategories = [];
        probabilities = [];
        predictedSex = [];
        var traces = [];

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
        colors = [
            "#800000",
            "#AC5924",
            "#CC993D",
            "#ECD957",
            "#DF8234",
            "#800000",
            "#D6411A"
        ]
        for (i=0; i<emotionCategories.lngth; i++) {

            var trace = {
                x: [emotionCategories],
                y: [parseFloat(probabilities[i])],
                type: 'bar',
                width: 1,
                marker: {
                    color: colors[i],
                }
            };
            
            traces.push(trace);
        }
        layout = {
            barmode: 'stack',
            title: cocktail,
            xaxis: {
                visible: false,
            },
            yaxis: {
                visible: false,
            },
            showlegend: true,
        }

        Plotly.newPlot('bar', traces, layout);

    }




