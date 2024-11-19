import requests
import time  # Make sure to import the time module

# Define the URL to monitor
url = "https://gelatinous-lopsided-coneflower.glitch.me/"  # Replace with the website you want to monitor

# Function to check the website status
def check_website_status():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Website is up: {url}")
        else:
            print(f"Website is down. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Monitor the website continuously
while True:
    check_website_status()
    time.sleep(10)  # Small pause to avoid overwhelming the server
