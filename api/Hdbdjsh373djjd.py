from flask import Flask, jsonify
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Global variable to store website status and last check time
website_status = {
    "status": "unknown",
    "message": "Waiting for first check",
    "status_code": None,
    "last_check": None
}

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            website_status['status'] = "up"
            website_status['message'] = "Website is up"
            website_status['status_code'] = response.status_code
        else:
            website_status['status'] = "down"
            website_status['message'] = "Website is down"
            website_status['status_code'] = response.status_code
    except requests.exceptions.RequestException as e:
        website_status['status'] = "down"
        website_status['message'] = f"Error: {str(e)}"
        website_status['status_code'] = None
    
    # Update the last check time with the current timestamp
    website_status['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def monitor_website():
    url = "https://gelatinous-lopsided-coneflower.glitch.me/"  # Use the provided URL
    while True:
        check_website(url)
        time.sleep(10)  # Wait for 10 seconds before checking again

@app.route('/monitor', methods=['GET'])
def monitor():
    return jsonify(website_status)

if __name__ == '__main__':
    # Start the monitoring in a background thread
    threading.Thread(target=monitor_website, daemon=True).start()
    app.run(debug=True)
