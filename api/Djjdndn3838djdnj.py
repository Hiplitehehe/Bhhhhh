from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

# Function to generate a Roblox-like code
def generate_roblox_code():
    # Generate 4 groups of 4 random alphanumeric characters separated by hyphens
    segments = []
    for _ in range(4):
        segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        segments.append(segment)
    return '-'.join(segments)

@app.route('/generate_roblox_code', methods=['GET'])
def get_roblox_code():
    code = generate_roblox_code()
    return jsonify({"code": code})

if __name__ == '__main__':
    app.run(debug=True)
