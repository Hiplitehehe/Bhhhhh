from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/encode_base64', methods=['POST'])
def encode_base64():
    data = request.get_json()  # Get JSON data from the request
    if 'text' in data:
        text = data['text']
        encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return jsonify({'encoded': encoded_text})
    else:
        return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
