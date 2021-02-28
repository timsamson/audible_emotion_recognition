from flask import Flask, jsonify, render_template, redirect, request

import os
import psycopg2
import numpy as np
import socket
import librosa
from pylab import *
import librosa.display
from joblib import load


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

def model_test(input_value):

    model = load('../models/rf_model.sav')
    feature = input_parser(input_file)
    arr = np.array(feature)
    arr2d = np.reshape(arr, (1,128))
    result = model.predict(arr2d)  

    return result

def plot_audio(input_file):
    
    data, sampling_rate = librosa.load(input_file)
    plt.figure(figsize=(12, 4))
    plot_fig = librosa.display.waveplot(data, sr=sampling_rate)

    return(data, sampling_rate, plot_fig)

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = True
app.config['SESSION_COOKIE_SECURE'] = True

# App routes

@app.route("/")
def index_page():
    print("responding to index route request")
    return render_template("index.html")

@app.route("/team")
def team_page():
    print("responding to team route request")
    return render_template("team.html")

@app.route("/emotions")
def emotions_page():
    print("responding to emotions route request")
    return render_template("emotions.html")

@app.route("/record", methods=['GET', 'POST'])
def record_page():
    print("responding to record page route request")
    if request.method == "POST":
        f = request.files['audio_data']
        with open('uploads/audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('record.html', request="POST")
    else:
        return render_template('record.html')

@app.route("/gallery")
def gallery_page():
    print("responding to gallery page route request")
    return render_template("gallery.html")


if __name__ == "__main__":
    app.run(debug=True)



