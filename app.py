from flask import Flask, jsonify, render_template, redirect

import os
import psycopg2
import numpy as np
import socket
import librosa

#functions
def input_parser(input_file):

   try:
      X, sample_rate = librosa.load(input_file, res_type='kaiser_fast') 
      mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0) 
   except Exception as e:
      print("Error encountered while parsing file: ", input_file)
      return None
 
   feature = mfccs.tolist()

   return feature
 
app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = True
app.config['SESSION_COOKIE_SECURE'] = True

# App routes

@app.route("/")
def index_page():
    print("responding to index route request")

    return render_template("index.html")

# @app.route("/homepage")
# def home2():
#     print("responding to homepage route request")
#     # Return template and data
#     return render_template("homepage.html")

@app.route("/team")
def team_page():
    print("responding to team route request")

    return render_template("team.html")

@app.route("/emotions")
def emotions_page():
    print("responding to emotions route request")

    return render_template("emotions.html")

@app.route("/record")
def record_page():
    print("responding to record page route request")

    return render_template("record.html")

if __name__ == "__main__":
    app.run(debug=True)



