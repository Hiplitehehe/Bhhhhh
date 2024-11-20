import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_FILE = "data.json"

# Function to load data from the file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save data to the file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Initialize data
data_store = load_data()

@app.route("/store", methods=["POST"])
def store_data():
    global data_store
    content = request.json
    key = content.get("key")
    value = content.get("value")
    if key and value:
        data_store[key] = value
        save_data(data_store)  # Save data to the file
        return jsonify({"message": "Data stored successfully!"})
    return jsonify({"error": "Invalid input"}), 400

@app.route("/get", methods=["GET"])
def get_data():
    global data_store
    return jsonify(data_store)

# Run the server locally (not required on Render)
if __name__ == "__main__":
    app.run(debug=True)
