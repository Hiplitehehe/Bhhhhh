import discord
from discord.ext import commands
from discord import app_commands
import random
import string
import time
import requests
from flask import Flask, jsonify, request
from threading import Thread
import os

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

token = os.getenv('token')

# Flask API setup
app = Flask(__name__)
keys = {}
api_url = "https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api"

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@bot.event
async def sync_commands():
    await bot.tree.sync()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    await sync_commands()

@bot.tree.command(description="Lock a specific channel")
async def lockchannel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    # Use the current channel if none is specified
    if channel is None:
        channel = interaction.channel

    # Attempt to lock the channel
    try:
        await channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await interaction.response.send_message(f"The channel `{channel.name}` has been locked.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to lock this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Failed to lock the channel. Error: {e}", ephemeral=True)

@bot.tree.command(description="Unlock a specific channel")
async def unlockchannel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    # Use the current channel if none is specified
    if channel is None:
        channel = interaction.channel

    # Attempt to unlock the channel
    try:
        await channel.set_permissions(interaction.guild.default_role, read_messages=True)
        await interaction.response.send_message(f"The channel `{channel.name}` has been unlocked.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to unlock this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Failed to unlock the channel. Error: {e}", ephemeral=True)

@bot.tree.command(description="Generate a new key")
async def genkey(interaction: discord.Interaction):
    try:
        response = requests.get(f"{api_url}/add")
        response.raise_for_status()
        data = response.json()

        embed = discord.Embed(title="Key Generated", color=discord.Color.green())
        embed.add_field(name="pyt that key then put this key `B3f9xT2W8kZ1uL7jP6yV`", value=f"`{data['key']}`", inline=False)
        embed.add_field(name="Expires", value=f"<t:{data['expiresAt']}:R>", inline=False)

        await interaction.user.send(embed=embed)
        await interaction.response.send_message("I have sent you the key in a DM!", ephemeral=False)
    except requests.RequestException as e:
        await interaction.response.send_message("Error generating key. Please try again later.", ephemeral=True)
        print(f"Error in genkey command: {e}")
        print(f"API Response: {response.text}")  # Print the API response for debugging
    except discord.Forbidden:
        await interaction.response.send_message("I can't DM you. Please check your privacy settings.", ephemeral=True)

@bot.tree.command(description="Check if a key is valid")
async def checkkey(interaction: discord.Interaction, key: str):
    try:
        response = requests.get(f"{api_url}/verify?key={key}&username={interaction.user.name}")
        response.raise_for_status()
        data = response.json()
        if data['valid']:
            await interaction.response.send_message(f"Valid key, expires: <t:{data['expiresAt']}:R>")
        else:
            await interaction.response.send_message("Invalid or expired key.")
    except requests.RequestException as e:
        await interaction.response.send_message("Error checking key. Please try again later.", ephemeral=True)
        print(f"Error in checkkey command: {e}")
        print(f"API Response: {response.text}")  # Print the API response for debugging

@app.route('/keys', methods=['GET'])
def list_keys():
    if not keys:
        return jsonify({"message": "No keys have been generated."}), 404

    key_list = [{"key": k, "expiresAt": v['expiry'], "username": v.get('username', 'Not bound')} for k, v in keys.items()]
    return jsonify(key_list), 200

@app.route('/keepalive', methods=['GET'])
def keep_alive():
    return jsonify({"status": "online"}), 200

@app.route('/add', methods=['GET'])
def add_key():
    key = generate_key()
    expiry = int(time.time()) + (3 * 24 * 60 * 60)  # 3 days in seconds
    keys[key] = {'expiry': expiry}
    return jsonify({"key": key, "expiresAt": expiry})

@app.route('/verify', methods=['GET'])
def verify_key():
    key = request.args.get('key')
    username = request.args.get('username')
    current_time = int(time.time())

    if key in keys:
        if current_time < keys[key]['expiry']:
            if 'username' not in keys[key]:
                keys[key]['username'] = username
            elif keys[key]['username'] != username:
                return jsonify({"valid": False, "reason": "bound_to_other"})

            return jsonify({"valid": True, "expiresAt": keys[key]['expiry'], "username": username})
        else:
            del keys[key]  # Remove expired key
            return jsonify({"valid": False, "reason": "expired"})
    else:
        return jsonify({"valid": False, "reason": "invalid"})

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    bot.run(token)
