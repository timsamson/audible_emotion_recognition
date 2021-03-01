from flask import Flask, jsonify, render_template, redirect, request, session

import os
import psycopg2
import numpy as np
import socket
import librosa
import librosa.display
from joblib import load
import datetime

results_dict = {
    "Predicted Emotion": [],
    "Emotion Categories": [], 
    "Probabilities": [], 
    "Predicted Sex": []
    }

#functions
def input_parser(input_file):

   try:
      X, sample_rate = librosa.load(input_file, res_type='kaiser_fast') 
      mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=128).T,axis=0) 
   except Exception as e:
      print("Error encountered while parsing file: ", input_file)
      return None
   feature = mfccs.tolist()
   
   return feature

def model_test(input_file):

    model = load('models/rf_model.sav')
    model2 = load('models/gender_model.sav')
    feature = input_parser(input_file)
    arr = np.array(feature)
    arr2d = np.reshape(arr, (1,128))
    pred_emotion = model.predict(arr2d)  
    probs = model.predict_proba(arr2d)
    emotion_labels = model.classes_
    gender = model2.predict(arr2d)
    if gender[0] == 0:
        label = "Male"
    elif gender[0] == 1:
        label = "Female"

    # results_dict = {
    #     "Predicted Emotion": pred_emotion[0],
    #     "Emotion Categories": emotion_labels.tolist(), 
    #     "Probabilities": probs[0].tolist(), 
    #     "Predicted Sex": label
    #     }
    results_dict["Predicted Emotion"].append(pred_emotion[0])
    results_dict["Emotion Categories"].append(emotion_labels.tolist())
    results_dict["Probabilities"].append(probs[0].tolist())
    results_dict["Predicted Sex"].append(label)
    print(results_dict)
    plot_audio(input_file)
    session['dict'] = results_dict
    return plot_audio

def plot_audio(input_file):
    
    data, sampling_rate = librosa.load(input_file)
    plt.figure(figsize=(12, 4))
    plot_fig = librosa.display.waveplot(data, sr=sampling_rate)

    return(data, sampling_rate, plot_fig)

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = True
app.config['SESSION_COOKIE_SECURE'] = True

app.secret_key = 'upgraded potato'

# App routes

@app.route("/team")
def team_page():
    print("responding to team route request")
    return render_template("team.html")

@app.route("/emotions")
def emotions_page():
    print("responding to emotions route request")
    return render_template("emotions.html")

@app.route("/", methods=['GET', 'POST'])
def record_page():
    print("responding to record page route request")
    #     return render_template('index.html', request="POST")
    # else:
    return render_template('index.html')

# @app.route("/output")
# def output():

@app.route("/api/v1.0", methods=['GET', 'POST'])
def load_data():
    if request.method == "POST":
        f = request.files['audio_data']
        file_name = datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S.wav")
        with open(file_name, 'wb') as audio_file:
            f.save(audio_file)

        results = model_test(file_name)
        print('file uploaded successfully')
        return (results)
    else:
        return (jsonify(results_dict))
       

@app.route("/gallery")
def gallery_page():
    print("responding to gallery page route request")
    return render_template("gallery.html")


if __name__ == "__main__":
    app.run(debug=True)



