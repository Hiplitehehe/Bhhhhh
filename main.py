from flask import Flask, request, jsonify

app = Flask(__name__)
latest_command = None  # Store the most recent command

@app.route("/command", methods=["POST"])
def receive_command():
    global latest_command
    data = request.json
    latest_command = data.get("command")
    print(f"Received command: {latest_command}")
    return jsonify({"status": "success", "received_command": latest_command})

@app.route("/get_command", methods=["GET"])
def send_command():
    return jsonify({"command": latest_command})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
