import os
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from transformers import pipeline
from pymongo import MongoClient
import secrets
import google.generativeai as genai
import json

app = Flask(__name__)


CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['petalvision']
users_collection = db['users']
detected_flowers_collection = db['detected_flowers']

# Image classification pipeline
classifier = pipeline("image-classification", model="dima806/flower_groups_image_detection")

# Gemini setup
GEMINI_API_KEY = "AIzaSyCFlKME8iunmkuzdFeGHFZkgir1z8XmQNo"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Server is Running!"})

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 409

    users_collection.insert_one({"name": name, "email": email, "password": password})
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = users_collection.find_one({"email": email, "password": password})
    if user:
        session['user_email'] = email
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/check-login", methods=["GET"])
def check_login():
    if 'user_email' in session:
        return jsonify({"logged_in": True, "email": session['user_email']})
    else:
        return jsonify({"logged_in": False})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('user_email', None)
    return jsonify({"message": "Logged out successfully"})

@app.route("/detect-flower", methods=["POST"])
def detect_flower():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_filename = secure_filename(image.filename)
    filename = f"{timestamp}_{original_filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    try:
        local_results = classifier(filepath)
        top_prediction = local_results[0]
        local_flower_name = top_prediction['label']
        confidence_score = round(top_prediction['score'] * 100, 2)

        # Upload image to Gemini for extra flower data
        uploaded_image = genai.upload_file(filepath, mime_type="image/png")

        prompt = (
            f"Identify the flower in this image and respond in this JSON format:\n"
            '{"name": "flower name", "description": "brief description", "season": "blooming season"}'
        )

        gemini_response = gemini_model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}, uploaded_image]}]
        )

        # Parsing Gemini response
        cleaned_text = gemini_response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]

        flower_info = json.loads(cleaned_text)

        response = {
            "name": flower_info.get("name", local_flower_name).capitalize(),
            "description": flower_info.get("description", "No description available."),
            "season": flower_info.get("season", "Unknown"),
            "confidence": f"{confidence_score}%",
            "saved_filename": filename
        }

        detected_flowers_collection.insert_one({
            "name": response["name"],
            "description": response["description"],
            "season": response["season"],
            "confidence": response["confidence"],
            "filename": filename,
            "timestamp": datetime.utcnow()
        })

    except json.JSONDecodeError:
        print("Failed to parse JSON from Gemini response.")
        response = {
            "name": local_flower_name.capitalize(),
            "description": "Gemini AI failed to generate data.",
            "season": "Unknown",
            "confidence": f"{confidence_score}%",
            "saved_filename": filename
        }
    except Exception as e:
        print(f"Gemini API error: {e}")
        response = {
            "name": local_flower_name.capitalize(),
            "description": "Gemini API error occurred.",
            "season": "Unknown",
            "confidence": f"{confidence_score}%",
            "saved_filename": filename
        }

    return jsonify(response), 200

@app.route("/know-more", methods=["POST"])
def know_more():
    data = request.get_json()
    flower_name = data.get("flower_name")

    if not flower_name:
        return jsonify({"error": "No flower name provided"}), 400

    prompt = f"Provide 50 words detailed information about the flower '{flower_name}'."

    try:
        gemini_response = gemini_model.generate_content(prompt)
        extra_info = gemini_response.text.strip()
    except Exception as e:
        print(f"Gemini API error on know-more: {e}")
        extra_info = "Additional information is currently unavailable."

    return jsonify({"extra_info": extra_info})

@app.route("/api/history", methods=["GET"])
def get_detection_history():
    try:
        detections = detected_flowers_collection.find().sort("timestamp", -1)

        history = []
        for item in detections:
            history.append({
                "id": str(item.get("_id")),
                "flowerName": item.get("name", "Unknown flower"),
                "description": item.get("description", "No description"),
                "confidence": float(item.get("confidence", "0%").strip('%')) / 100,
                "detectedAt": item.get("timestamp").isoformat() if item.get("timestamp") else "Unknown",
                "imageUrl": f"/uploads/{item.get('filename', '')}"
            })

        if not history:
            return jsonify([])

        return jsonify(history)

    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    uploads_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    return send_from_directory(uploads_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
