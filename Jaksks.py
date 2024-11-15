from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/gamepasscheck', methods=['GET'])
def gamepasscheck():
    # Get the Game Pass ID from the query parameters
    game_pass_id = request.args.get('game_pass_id')

    if not game_pass_id or not game_pass_id.isdigit():
        return jsonify({"error": "Invalid or missing game_pass_id parameter."}), 400

    # Convert the Game Pass ID to an integer
    game_pass_id = int(game_pass_id)

    # URL to fetch game pass info from Roblox API
    url = f"https://apis.roblox.com/game-passes/v1/game-passes/{game_pass_id}/product-info"
    
    try:
        # Fetch the game pass data from the API
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract relevant details from the response
            name = data.get('Name', 'N/A')
            description = data.get('Description', 'N/A')
            price = data.get('PriceInRobux', 0)  # Default to 0 if the price is not available
            icon_id = data.get('IconImageAssetId', None)
            creator_name = data.get('Creator', {}).get('Name', 'N/A')
            creator_id = data.get('Creator', {}).get('Id', 'N/A')

            # Check if price is None, and default it to 0 if necessary
            if price is None:
                price = 0

            # Calculate the Robux reward (50% of the price)
            robux_reward = int(price * 0.5)  # Calculate reward

            # Construct the response message
            game_pass_info = {
                "Name": name,
                "Description": description,
                "Price": price,
                "Robux Reward": robux_reward,
                "Creator": {"Name": creator_name, "Id": creator_id},
                "Icon": f"https://www.roblox.com/asset/?id={icon_id}" if icon_id else "No icon available"
            }

            return jsonify(game_pass_info)

        else:
            return jsonify({"error": f"Failed to fetch game pass data. Status code: {response.status_code}"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred while fetching game pass data: {e}"}), 500

if __name__ == '__main__':
    # Set the host to '0.0.0.0' to allow access from any IP address
    app.run(host='0.0.0.0', port=5000, debug=True)
