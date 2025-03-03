from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

fuel = 100.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    global fuel

    fuel -= 0.001 

    if fuel < 0:
        fuel = 0.0

    lat = random.uniform(20.9840, 20.9890)  
    lon = random.uniform(105.8060, 105.8130)  

    speed = random.randint(0, 120)

    gps_location = {"lat": lat, "lon": lon}

    return jsonify(speed=speed, fuel=fuel, gps=gps_location)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)
