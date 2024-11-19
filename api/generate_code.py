import random
import string
from flask import Flask, jsonify

app = Flask(__name__)

def generate_code():
    # Generates a random code in the format XXXX-XXXX-XXXX
    return '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])

@app.route('/a', methods=['GET'])
def get_code():
    # Returns the generated random code
    return jsonify({"code": generate_code()})

# Export the app for Vercel
if __name__ == "__main__":
    app.run(debug=True)
