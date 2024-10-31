from flask import Flask, request, jsonify
import time
import secrets

app = Flask(__name__)

# Sample keys dictionary to store keys and their associated data
keys = {}

@app.route('/api/add', methods=['GET'])
def add_key():
    # Generate a random key
    key = secrets.token_urlsafe(16)  # Generate a random key of 16 bytes (22 characters)

    # Set expiry time to 3 days (3 days = 3 * 24 * 60 * 60 seconds)
    expiry_time = 3 * 24 * 60 * 60  # 3 days in seconds
    current_time = int(time.time())
    
    keys[key] = {
        "expiry": current_time + expiry_time,
        "username": None  # Initialize username as None or any default value
    }

    return jsonify({"success": True, "key": key, "message": f"Key {key} added successfully.", "expiresAt": keys[key]['expiry']}), 201

@app.route('/api/keys', methods=['GET'])
def list_keys():
    # Prepare the list of keys with their details
    keys_list = []
    current_time = int(time.time())
    
    for key, data in keys.items():
        keys_list.append({
            "key": key,
            "expiresAt": data["expiry"],
            "username": data["username"],
            "valid": current_time < data["expiry"]
        })
    
    return jsonify(keys_list), 200


@app.route('/api/verify', methods=['GET'])
def verify_key():
    key = request.args.get('key')
    username = request.args.get('username')
    current_time = int(time.time())

    if key in keys:
        if current_time < keys[key]['expiry']:
            if keys[key]['username'] is None:
                keys[key]['username'] = username
                print(f"API: Key {key} bound to {username}")
            elif keys[key]['username'] != username:
                return jsonify({"valid": False, "reason": "bound_to_other"})

            print(f"API Check: {key} valid for {username}")
            return jsonify({"valid": True, "expiresAt": keys[key]['expiry'], "username": username})
        else:
            print(f"API Check: {key} expired")
            del keys[key]  # Remove expired key
            return jsonify({"valid": False, "reason": "expired"})
    else:
        print(f"API Check: {key} invalid")
        return jsonify({"valid": False, "reason": "invalid"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
