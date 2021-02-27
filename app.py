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

@app.route("/homepage")
def home2():
    print("responding to homepage route request")
    # Return template and data
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)



