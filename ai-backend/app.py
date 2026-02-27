from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os
from flask_cors import CORS
from weather import get_weather, get_weather_history
from prediction import predict_disaster_risk

app = Flask(__name__)
CORS(app)

# Load AI knowledge for historical data only
try:
    df = pickle.load(open("models/disaster_knowledge_clean.pkl", "rb"))
    print(f"[OK] Loaded {len(df)} disaster records")
except Exception as e:
    print(f"[WARNING] Could not load clean data: {e}")
    try:
        df = pickle.load(open("models/disaster_knowledge.pkl", "rb"))
        print(f"[OK] Loaded original data: {len(df)} records")
    except:
        df = pd.DataFrame()

try:
    le_location = pickle.load(open("models/state_encoder.pkl", "rb"))
    print(f"[OK] Loaded state encoder with {len(le_location.classes_)} states")
    print(f"[INFO] Available states: {list(le_location.classes_)[:10]}...")
except Exception as e:
    print(f"[WARNING] Could not load state encoder: {e}")
    try:
        le_location = pickle.load(open("models/location_encoder.pkl", "rb"))
        print(f"[OK] Loaded location encoder")
    except:
        le_location = None


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "Disaster Preparedness API",
        "endpoints": [
            "/disaster-prediction?location=Mumbai",
            "/weather?location=Mumbai",
            "/weather-history?location=Mumbai&days=3",
            "/disaster",
            "/modules"
        ]
    })


@app.route("/get_location_data", methods=["POST"])
def get_location_data():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        location = data.get("location", "").strip()
        if not location:
            return jsonify({"message": "Location required"}), 400

        if le_location is None or df.empty:
            return jsonify({"message": "Historical data not available"}), 503
        
        print(f"Searching for location: '{location}'")
        
        # Try exact match first (case-insensitive)
        try:
            encoded = le_location.transform([location])[0]
            matched_location = location
        except:
            # Fuzzy match - find states containing the search term
            matching_locations = [loc for loc in le_location.classes_ if location.lower() in loc.lower()]
            
            if not matching_locations:
                available = ", ".join(list(le_location.classes_)[:5])
                return jsonify({"message": f"No data for '{location}'. Try: {available}, etc."}), 404
            
            matched_location = matching_locations[0]
            encoded = le_location.transform([matched_location])[0]
        
        print(f"Matched '{location}' to '{matched_location}'")
        
        # Get data using State column if available, otherwise location_encoded
        if 'State' in df.columns:
            result = df[df['State'] == matched_location]
        else:
            result = df[df["location_encoded"] == encoded]
        
        if result.empty:
            return jsonify({"message": f"No historical disasters for '{location}'"}), 404
        
        # Drop encoded column if exists
        if 'location_encoded' in result.columns:
            result = result.drop(columns=["location_encoded"])
        
        # Convert to records and clean NaN values
        raw = result.to_dict(orient="records")
        cleaned = []
        for rec in raw:
            cleaned_rec = {}
            for k, v in rec.items():
                if pd.isna(v):
                    cleaned_rec[k] = None
                else:
                    cleaned_rec[k] = int(v) if isinstance(v, (int, float)) and k in ["Start Year", "Total Deaths"] else v
            cleaned.append(cleaned_rec)
        
        print(f"Returning {len(cleaned)} disaster records for '{matched_location}'")
        return jsonify(cleaned)

    except Exception as e:
        print(f"Error in get_location_data: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Internal server error"}), 500


@app.route("/locations", methods=["GET"])
def get_locations():
    """List all available locations in the dataset"""
    if le_location is None:
        return jsonify({"message": "No locations available"}), 503
    return jsonify({"locations": sorted(list(le_location.classes_))})


# Frontend expects /disaster and /modules — provide simple endpoints
@app.route("/disaster", methods=["GET"])
def disaster():
    # Return live or sample disaster info
    sample = {
        "type": "Flood",
        "weather": "Heavy Rain",
        "risk": "HIGH",
        "tip": "Move to higher ground and avoid water crossings."
    }
    return jsonify(sample)


@app.route("/modules", methods=["GET"])
def modules():
    # Return a simple modules list usable by the frontend
    modules_list = [
        {"id": "m1", "type": "video", "title": "Flood Safety", "description": "Flood tips"},
        {"id": "m2", "type": "quiz", "title": "Fire Quiz", "description": "Test yourself"}
    ]
    return jsonify(modules_list)


@app.route("/weather", methods=["GET"])
def weather():
    # Accept ?location=... or JSON {"location": "..."}
    loc = request.args.get("location") or (request.json or {}).get("location")
    if not loc:
        return jsonify({"message": "location required"}), 400
    try:
        data = get_weather(loc)
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": str(e)}), 502


@app.route("/weather-history", methods=["GET"])
def weather_history():
    """Fetch past N days of weather for a location."""
    loc = request.args.get("location") or (request.json or {}).get("location")
    days = request.args.get("days", 3, type=int)
    if not loc:
        return jsonify({"message": "location required"}), 400
    try:
        data = get_weather_history(loc, days=min(days, 7))  # Max 7 days
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": str(e)}), 502


@app.route("/disaster-prediction", methods=["GET", "POST"])
def disaster_prediction():
    """Predict disaster risk based on location and weather."""
    try:
        # Get location from query or JSON
        if request.method == "POST":
            data = request.json or {}
            loc = data.get("location")
            temp = data.get("temp")
            humidity = data.get("humidity")
            wind = data.get("wind")
        else:
            loc = request.args.get("location")
            temp = request.args.get("temp")
            humidity = request.args.get("humidity")
            wind = request.args.get("wind")
        
        if not loc:
            return jsonify({"message": "location required"}), 400
        
        # Fetch real-time weather if not provided
        if temp is None or humidity is None or wind is None:
            weather_data = get_weather(loc)
            temp = weather_data.get("main", {}).get("temp", 25)
            humidity = weather_data.get("main", {}).get("humidity", 50)
            wind = weather_data.get("wind", {}).get("speed", 5)
        else:
            temp = float(temp)
            humidity = int(humidity)
            wind = float(wind)
        
        # Use heuristic prediction
        location_encoded = 0
        if le_location is not None:
            try:
                location_encoded = le_location.transform([loc])[0]
            except:
                location_encoded = 0
        
        prediction = predict_disaster_risk(location_encoded, temp, humidity, wind)
        
        # Add weather data to response
        prediction["weather_data"] = {
            "temp": temp,
            "humidity": humidity,
            "wind": wind,
            "location": loc
        }
        
        return jsonify(prediction)
    except Exception as e:
        print(f"Error in disaster_prediction: {e}")
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
