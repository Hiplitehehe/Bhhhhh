import os
import pymongo
from pymongo import MongoClient
from flask import jsonify, request

# Fetch MongoDB connection URI from Vercel environment variables
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.get_database('your-db-name')  # Replace with your database name
collection = db.get_collection('your-collection')  # Replace with your collection name

def handler(request):
    if request.method == 'POST':
        try:
            data = request.get_json().get('data')  # Get the data from the request body
            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            # Insert the data into the collection
            result = collection.insert_one({'data': data})
            return jsonify({"success": True, "insertedId": str(result.inserted_id)}), 200

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    else:
        return jsonify({"success": False, "message": "Method not allowed"}), 405
