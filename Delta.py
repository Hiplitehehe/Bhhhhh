from flask import Flask, request, jsonify
import requests
import asyncio
from urllib.parse import parse_qs, unquote  # Correct imports

# Initialize Flask app
app = Flask(__name__)

platoboost_url = "https://gateway.platoboost.com/a/8?id="

def time_convert(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours} Hours {mins} Minutes"

async def get_turnstile_response():
    await asyncio.sleep(1)  # Simulated delay for response
    return "simulated-captcha-response"

async def delta(id):
    try:
        response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        if response.status_code != 200:
            raise Exception(f"Access to Platoboost failed: {response.status_code}")

        already_pass = response.json()
        if 'key' in already_pass:
            time_left = time_convert(already_pass['minutesLeft'])
            return jsonify({"message": f"**INFO** Remaining time: {time_left} - KEY: {already_pass['key']}"})

        captcha = already_pass.get('captcha')
        post_data = {
            "captcha": await get_turnstile_response() if captcha else "",
            "type": "Turnstile" if captcha else ""
        }
        response = requests.post(
            f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}",
            json=post_data
        )

        if response.status_code != 200:
            security_check_link = f"{platoboost_url}{id}"
            return jsonify({"error": "Security Check Needed", "link": security_check_link}), 400

        loot_link = response.json()['redirect']
        await asyncio.sleep(1)  # Simulated delay

        r = requests.utils.urlparse(loot_link).query.split("r=")[-1]
        decoded = unquote(r).encode('ascii')
        print(f"Decoded query string: {decoded}")  # Log the decoded query string for debugging
        
        parsed_qs = parse_qs(decoded)
        if 'tk' not in parsed_qs:
            raise Exception("Token ('tk') not found in the query string")
        
        tk = parsed_qs['tk'][0]  # Corrected here using parse_qs from urllib.parse
        await asyncio.sleep(5)  # Simulated delay

        response = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/{tk}")
        if response.status_code != 200:
            raise Exception(f"Key creation failed: {response.status_code}")

        response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        pass_data = response.json()
        if 'key' in pass_data:
            time_left = time_convert(pass_data['minutesLeft'])
            return jsonify({"message": f"**INFO** Remaining time: {time_left} - KEY: {pass_data['key']}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for the bypass API
@app.route('/bypass', methods=['POST'])
def bypass():
    data = request.get_json()
    hwid = data.get('hwid')

    if not hwid:
        return jsonify({"error": "HWID is required"}), 400

    # Run the bypass process asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(delta(hwid))
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
