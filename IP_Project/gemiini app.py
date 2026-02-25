import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from transformers import pipeline
from PIL import Image
from pymongo import MongoClient
import secrets
import google.generativeai as genai
import json

# Flask app setup
app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

# Uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['petalvision']
users_collection = db['users']

# Load flower detection model
classifier = pipeline("image-classification", model="dima806/flower_groups_image_detection")

# Gemini setup
GEMINI_API_KEY = "AIzaSyCFlKME8iunmkuzdFeGHFZkgir1z8XmQNo"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

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
        pil_image = Image.open(filepath).convert("RGB")
        results = classifier(pil_image)
        if not results:
            return jsonify({"error": "Flower classification failed"}), 500
        top_result = results[0]
    except Exception as e:
        return jsonify({"error": f"Image classification failed: {str(e)}"}), 500

    flower_name = top_result["label"].lower()

    # Improved Gemini prompt
    prompt = (
        f"Give the following details about the flower '{flower_name}':\n"
        f"- A brief description\n"
        f"- Season of blooming\n\n"
        f"Respond only in JSON format like this:\n"
        f'{{"description": "your description", "season": "your season"}}'
    )
    print(f"Prompt sent to Gemini: {prompt}")

    try:
        gemini_response = gemini_model.generate_content(prompt)
        print(f"Gemini Response: {gemini_response.text}")

        # Remove markdown code block if it exists
        cleaned_text = gemini_response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]

        flower_info = json.loads(cleaned_text.strip())

    except json.JSONDecodeError:
        print("Failed to parse JSON from Gemini response.")
        flower_info = {
            "season": "Unknown",
            "description": "Could not get details from AI."
        }
    except Exception as e:
        print(f"Gemini API error: {e}")
        flower_info = {
            "season": "Unknown",
            "description": "Gemini AI failed to generate data."
        }

    response = {
        "name": flower_name.capitalize(),
        "season": flower_info.get("season", "Unknown"),
        "description": flower_info.get("description", "No description available."),
        "confidence": f"{top_result['score']:.2%}",
        "saved_filename": filename
    }

    return jsonify(response), 200

@app.route("/know-more", methods=["POST"])
def know_more():
    data = request.get_json()
    flower_name = data.get("flower_name")

    if not flower_name:
        return jsonify({"error": "No flower name provided"}), 400

    prompt = (
        f"Provide 50 words detailed information about the flower '{flower_name}'. "
        
    )

    try:
        gemini_response = gemini_model.generate_content(prompt)
        extra_info = gemini_response.text.strip()
    except Exception as e:
        print(f"Gemini API error in know-more: {e}")
        extra_info = "Failed to retrieve more information."

    return jsonify({"extra_info": extra_info})


if __name__ == "__main__":
    app.run(debug=True)