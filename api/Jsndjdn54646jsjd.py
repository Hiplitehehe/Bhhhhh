from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Supabase connection details
url = "https://tlqxjnzkwnlhaeqnzbcy.supabase.co"  # Your Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRscXhqbnprd25saGFlcW56YmN5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIxMDcxMzIsImV4cCI6MjA0NzY4MzEzMn0.7h5OAeHgZXKc11udZHy5Iano0Kxi9stzOzH-CRWLt2U"  # Replace with your Supabase anon key
supabase: Client = create_client(url, key)

# Store data in Supabase
@app.route("/store", methods=["POST"])
def store_data():
    content = request.json
    key = content.get("key")
    value = content.get("value")
    
    if key and value:
        # Insert data into Supabase
        response = supabase.table('data_store').insert({'key': key, 'value': value}).execute()
        return jsonify({"message": "Data stored successfully!"}), 200
    return jsonify({"error": "Invalid input"}), 400

# Retrieve data from Supabase
@app.route("/get", methods=["GET"])
def get_data():
    response = supabase.table('data_store').select("*").execute()
    return jsonify(response.data)

if __name__ == "__main__":
    app.run(debug=True)
