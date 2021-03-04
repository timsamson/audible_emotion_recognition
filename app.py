from flask import Flask, jsonify, render_template, redirect, request, session

import os
import psycopg2
import numpy as np
import socket
import librosa
import librosa.display
from matplotlib import pyplot as plt
from joblib import load
import datetime
import json

results_dict = {
    "predictedEmotion": [],
    "emotionCategories": [], 
    "probabilities": [], 
    "predictedSex": []
    }

user_file = {
    'filepath': []
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
    user_file["filepath"] = input_file
    model = load('models/rf2_model.sav')
    model2 = load('models/gen_emo_rf_model.sav')
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
    results_dict["predictedEmotion"] = pred_emotion[0]
    results_dict["emotionCategories"] = emotion_labels.tolist()
    results_dict["probabilities"] = probs[0].tolist()
    results_dict["predictedSex"] = label
    print(results_dict)
    return results_dict

def plot_audio(input_file):
    
    data, sampling_rate = librosa.load(input_file)
    plt.figure(figsize=(12, 4))
    plot_fig = librosa.display.waveplot(data, sr=sampling_rate)
    return(data, sampling_rate, plot_fig)


audio_file_paths = [
    "static/audio/mono_a13_hanks.wav", 
    "static/audio/mono_clue_mustard.wav",
    "static/audio/mono_ewdavid.wav",
    "static/audio/mono_meangirls_gretchen.wav",
    "static/audio/mono_nathan.wav",
    "static/audio/mono_starwars_vader.wav",
    "static/audio/mono_theoffice_michael.wav",
    "static/audio/mono_wizardofoz_witch.wav"
]
tv_movie_sounds = [model_test(path) for path in audio_file_paths]



app = Flask(__name__)

# app.config['SESSION_COOKIE_SAMESITE'] = True
# app.config['SESSION_COOKIE_SECURE'] = True

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

@app.route("/viz")
def visuals_page():
    print("responding to visualzations route request")
    return render_template("viz.html")

@app.route("/", methods=['GET', 'POST'])
def record_page():
    print("responding to record page route request")
    #     return render_template('index.html', request="POST")
    # else:
    if request.method == "POST":
        f = request.files['audio_data']
        # file_name = datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S.wav")
        # with open(file_name, 'wb') as audio_file:
        #     f.save(audio_file)

        results = model_test(f)
        # session['dict']=results
        print('file uploaded successfully')
        print(results)
        return (results)
    else:
        return render_template('index.html')

@app.route("/data")
def data():
    return(jsonify(results_dict))

@app.route("/tv_movie")
def more_data():
    print("Success!!!")
    return(jsonify(tv_movie_sounds))

@app.route("/plot")
def plot():
    src_path = user_file['filepath']
    # result = plot_audio(src_path)
    return(src_path)
       
@app.route("/gallery", methods=['GET', 'POST'])
def gallery_page():
    print("responding to gallery page route request")
    if request.method == "POST":
        f = request.files['audio_data']
        results = model_test(f)
        print('file uploaded to model')
        print(results)
        return (results)
    else:
        return render_template('gallery.html')

if __name__ == "__main__":
    app.run(debug=True)



