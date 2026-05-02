from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

# Replace with your actual key or set as environment variable
API_KEY = '773faa83a0917071d116810008763779'

@app.route('/')
def index():
    # Serves your index.html file from the /templates folder
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Missing coordinates"}), 400

    # Clean Code: Using a single session for multiple requests is more efficient
    base_url = "https://api.openweathermap.org/data/2.5"
    
    try:
        # Current Weather
        current = requests.get(f"{base_url}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric").json()
        # 5-Day Forecast
        forecast = requests.get(f"{base_url}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric").json()
        # Air Pollution (AQI)
        air = requests.get(f"{base_url}/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}").json()

        return jsonify({
            "current": current,
            "forecast": forecast,
            "air": air
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)