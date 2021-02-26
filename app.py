from flask import Flask, jsonify, render_template, redirect
# from geopy.geocoders import GoogleV3
import os
import psycopg2
import numpy as np
import socket

db_name = "cocktail_db"

#check if we're running in heroku and my environmental variable exist
if 'DATABASE_URL' in os.environ:
    postgres_url = os.environ['DATABASE_URL']
else:
    #if we're not running in heroku then try and get my local config password
    from db import config
    postgres_url = f"postgresql://postgres:{config.postgres_pwd}@127.0.0.1:5432/{db_name}"

conn = psycopg2.connect(postgres_url)
mycursor = conn.cursor()

def state_data():
    mycursor.execute("select * from state")
    results = mycursor.fetchall()
    result_dicts = [ {"state": result[0], "abbr": result[1], "latitude": result[2], "longitude": result[3], "cocktail": result[4], "image_src": result[5]} for result in results]
    return jsonify(result_dicts)

# Create an instance of Flask for bubble
def bubble_data():
    mycursor.execute("SELECT s.cocktail, m.ingredient, m.measure, m.unit FROM state s \
                    INNER JOIN measure m ON (s.cocktail = m.cocktail) \
                    GROUP BY s.cocktail, m.ingredient, m.measure, m.unit \
                    ORDER BY s.cocktail DESC;")
    results = mycursor.fetchall()
    result_dicts = [ {"cocktail": result[0], "ingredient": result[1], "measure": result[2], "unit": result[3]} for result in results]
    return (result_dicts)
    
def measure_data():
    mycursor.execute("SELECT * FROM measure;")
    results = mycursor.fetchall()
    result_dicts = [ {"cocktail": result[2], "ingredient": result[0], "measure": result[1], "unit": result[3]} for result in results]
    return jsonify(result_dicts)

def cocktail_name_data():
    mycursor.execute("SELECT * FROM cocktail;")
    results = mycursor.fetchall()
    result_dicts = [ {"cocktail": result[0], "category": result[1]} for result in results]
    return jsonify(result_dicts)

def recipe_data():
    mycursor.execute("SELECT * FROM recipe;")
    results = mycursor.fetchall()
    result_dicts = [ {"cocktail": result[0], "glass_type": result[1], "glass_size": result[2], "instructions": result[3]} for result in results]
    return jsonify(result_dicts)

   
app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = True
app.config['SESSION_COOKIE_SECURE'] = True

# Route to render leaflet map on home
@app.route("/raw-web-api")
def scrape():
    map_data = state_data()
    print("responding to raw-web-api route: ")
    return (map_data)

@app.route("/", methods=['post', 'get'])
def home():
    print("responding to home route request")
    # Return template and data
    return render_template("index.html")

@app.route("/homepage")
def home2():
    print("responding to homepage route request")
    # Return template and data
    return render_template("homepage.html")

@app.route("/not_21")
def not_21():
    print("responding to 21 route request")
    # Return template and data
    return render_template("not_21.html")

@app.route("/measure-data")
def measure():
    ingred_data = measure_data()
    print("responding to ingredients route request")
    return (ingred_data)

@app.route("/cocktail-name-data")
def names():
    name_data = cocktail_name_data()
    print("responding to cocktail names request")
    return (name_data)

@app.route("/leaflet-map")
def leaflet_map():
    return render_template("leaflet-map.html")

@app.route("/bubble-data")
def scrape2():
    bub_data = bubble_data()
    print("responding to raw-web-api route: ")
    return jsonify(bub_data)

@app.route("/bubble")
def bubble2():
    return render_template("bubble.html")

@app.route("/recipe-data")
def recipes():
    recipe = recipe_data()
    print("responding to recipe-data request")
    return (recipe)

if __name__ == "__main__":
    app.run(debug=True)



