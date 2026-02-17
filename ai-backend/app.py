from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS
from weather import get_weather, get_weather_history
from prediction import predict_disaster_risk, train_prediction_model
from xgboost_model import predict_with_xgboost, train_xgboost_model

app = Flask(__name__)
CORS(app)

# Load AI knowledge (optional — files must exist)
try:
    df = pickle.load(open("models/disaster_knowledge.pkl", "rb"))
except Exception:
    df = pd.DataFrame()

try:
    le_location = pickle.load(open("models/location_encoder.pkl", "rb"))
except Exception:
    le_location = None

# Train disaster prediction model on startup
try:
    train_prediction_model(df)
    print("✅ Disaster predictor model trained")
except Exception as e:
    print(f"⚠ Warning: could not train predictor: {e}")

# Train XGBoost AI model on startup
try:
    train_xgboost_model()
    print("✅ XGBoost AI model trained")
except Exception as e:
    print(f"⚠ Warning: could not train XGBoost: {e}")


@app.route("/get_location_data", methods=["POST"])
def get_location_data():
    data = request.json
    location = data.get("location")

    try:
        if le_location is None:
            raise ValueError("Location encoder not available")
        encoded = le_location.transform([location])[0]
        result = df[df["location_encoded"] == encoded].drop(columns=["location_encoded"])
        # Convert to records then replace NaN with None for JSON compatibility
        raw = result.to_dict(orient="records")
        cleaned = []
        for rec in raw:
            cleaned_rec = {}
            for k, v in rec.items():
                if pd.isna(v):
                    cleaned_rec[k] = None
                else:
                    cleaned_rec[k] = v
            cleaned.append(cleaned_rec)
        return jsonify(cleaned)

    except Exception:
        return jsonify({"message": "Location not found"})


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
    
    try:
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
        
        # Encode location if available
        location_encoded = 0
        if le_location is not None:
            try:
                location_encoded = le_location.transform([loc])[0]
            except:
                location_encoded = 0
        
        # Get AI prediction using XGBoost
        prediction = predict_with_xgboost(temp, humidity, wind)
        
        if prediction is None:
            # Fallback to heuristic model
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
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
