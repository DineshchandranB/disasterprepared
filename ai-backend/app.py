from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS

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


if __name__ == "__main__":
    app.run(debug=True)
