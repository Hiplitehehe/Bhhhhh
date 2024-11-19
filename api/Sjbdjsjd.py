import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from threading import Thread
from flask import Flask, jsonify

# Create a Flask app
flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def us():
    return jsonify({"status": "API is running"})


@flask_app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

# Load your token from an environment variable or file
TOKEN = os.getenv('TOKEN')  # Set your bot token as an environment variable

print(os.getenv('TOKEN'))

# Create a bot instance
bot = commands.Bot(command_prefix='>', intents=discord.Intents.default())

API_BASE_URL = "https://bhhhhh-2.onrender.com/"  # Replace with your actual API domain

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print("Bot is {bot.user.name} ready")

@bot.tree.command(name="sync_commands")
async def sync_commands(interaction: discord.Interaction):
    """Manually sync commands."""
    await bot.tree.sync()
    await interaction.response.send_message("Commands synced!", ephemeral=True)


@bot.tree.command(name="fluxus")
async def fluxus(interaction: discord.Interaction, link: str):
    """Fetch Fluxus data."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/api/fluxus?link={link}") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="bloxfruits_stock")
async def bloxfruits_stock(interaction: discord.Interaction):
    """Get Blox Fruits stock."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/api/bloxfruits/stock") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="addlink")
async def addlink(interaction: discord.Interaction, url: str):
    """Add a link."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/TestHub/addlink?url={url}") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="flux_gen")
async def flux_gen(interaction: discord.Interaction):
    """Get a random Flux HWID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/flux_gen") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="arc_gen")
async def arc_gen(interaction: discord.Interaction):
    """Get a random Arc HWID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/arc_gen") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="delta_gen")
async def delta_gen(interaction: discord.Interaction):
    """Get a random Delta HWID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/delta_gen") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="gen_key")
async def gen_key(interaction: discord.Interaction):
    """Generate a key from the external API."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api/add") as response:
                # Try to get the response data regardless of status code
                response_data = await response.json()
                
                if response.status == 200:
                    await interaction.response.send_message(response_data, ephemeral=True)
                else:
                    # Show the API response even on error status codes
                    await interaction.response.send_message(f"Error: Received status code {response.status}. Response: {response_data}", ephemeral=True)
        except Exception as e:
            # If there's an exception, show the error and the API response if available
            await interaction.response.send_message(f"Exception occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="hydro_gen")
async def hydro_gen(interaction: discord.Interaction):
    """Get a random Hydro HWID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/hydro_gen") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="boost_ink")
async def boost_ink(interaction: discord.Interaction, url: str):
    """Extract Base64 from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/boost.ink?url={url}") as response:
            data = await response.json()
            await interaction.response.send_message(data)

@bot.tree.command(name="status")
async def check_status(interaction: discord.Interaction):
    """Check the health of the API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/status") as response:
            data = await response.json()
            await interaction.response.send_message(data)

# Start the Flask app in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Start the bot
bot.run(TOKEN)
