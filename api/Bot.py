import asyncio
from flask import Flask, request, jsonify
import discord
from threading import Thread
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Discord client with appropriate intents
intents = discord.Intents.default()
intents.guilds = True  # Enable access to guild data
client = discord.Client(intents=intents)

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# To handle the event when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# API route to download Discord server profile based on ID
@app.route('/download_server_profile', methods=['GET'])
def download_server_profile():
    server_id = request.args.get('id')  # Get the Discord server ID from the URL query parameter

    if not server_id:
        return jsonify({"error": "No server ID provided"}), 400

    try:
        guild = client.get_guild(int(server_id))

        if guild is None:
            # If the bot is not in the server or the ID is invalid
            return jsonify({"error": "Server not found or bot is not in the server"}), 404

        # Correct icon URL generation
        icon_url = f"https://cdn.discordapp.com/icons/{guild.id}/{guild.icon}.png?size=1024" if guild.icon else None

        # Return server profile data without the deprecated `region` and updated icon handling
        profile_data = {
            "name": guild.name,
            "id": guild.id,
            "member_count": guild.member_count,
            "owner": str(guild.owner),
            "icon_url": icon_url  # Icon URL generated
        }

        return jsonify(profile_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to run the bot
async def run_bot():
    await client.start(BOT_TOKEN)

# Function to run the Flask app
def run_api():
    app.run(debug=True, use_reloader=False)

# Running both Flask and the bot concurrently using asyncio
async def main():
    bot_task = asyncio.create_task(run_bot())
    api_thread = Thread(target=run_api)
    api_thread.start()
    await bot_task

if __name__ == '__main__':
    asyncio.run(main())
