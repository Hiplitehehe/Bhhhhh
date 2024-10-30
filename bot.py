import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from threading import Thread
from flask import Flask, jsonify
from datetime import datetime

# Create a Flask app
flask_app = Flask(__name__)

@flask_app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

# Load your token from an environment variable or file
TOKEN = os.getenv('token')  # Set your bot token as an environment variable

# Create a bot instance
bot = commands.Bot(command_prefix='>', intents=discord.Intents.default())

API_BASE_URL = "https://bhhhhh-2.onrender.com/"  # Replace with your actual API domain
INVITE_URL = "https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=YOUR_PERMISSIONS&scope=bot%20applications.commands"  # Replace with your bot's invite URL

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.tree.sync()
    print("Commands synced")

def add_invite_button():
    """Add an 'Add Me!' button."""
    button = discord.ui.Button(label="Add Me!", url=INVITE_URL)
    view = discord.ui.View()
    view.add_item(button)
    return view

@bot.tree.command(name="commands")
@app_commands.describe(command="Choose a command to execute")
async def commands(interaction: discord.Interaction, command: str):
    """Execute a command based on user input."""
    async with aiohttp.ClientSession() as session:
        if command == "fluxus":
            link = interaction.user.mention  # You could ask for a link instead
            async with session.get(f"{API_BASE_URL}/api/fluxus?link={link}") as response:
                data = await response.json()
                embed = discord.Embed(title="Fluxus Data", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        elif command == "bloxfruits_stock":
            async with session.get(f"{API_BASE_URL}/api/bloxfruits/stock") as response:
                data = await response.json()
                embed = discord.Embed(title="Blox Fruits Stock", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        elif command == "addlink":
            url = "http://example.com"  # Replace this with actual user input handling
            async with session.get(f"{API_BASE_URL}/TestHub/addlink?url={url}") as response:
                data = await response.json()
                embed = discord.Embed(title="Add Link", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        elif command == "flux_gen":
            async with session.get(f"{API_BASE_URL}/flux_gen") as response:
                data = await response.json()
                embed = discord.Embed(title="Random Flux HWID", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        elif command == "arc_gen":
            async with session.get(f"{API_BASE_URL}/arc_gen") as response:
                data = await response.json()
                embed = discord.Embed(title="Random Arc HWID", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        elif command == "gen_key":
            async with session.get("https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api/add") as response:
                response_data = await response.json()
                embed = discord.Embed(title="API Response", color=discord.Color.blue())

                if response.status == 201:
                    key = response_data.get('key', 'No key available')
                    expire = response_data.get('expire', 'No expiration provided')

                    if isinstance(expire, int):
                        if expire > 1_000_000_000_000:
                            expire = expire / 1000
                        expire = datetime.fromtimestamp(expire).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        expire = "Invalid expiration format"

                    embed.add_field(name="Generated Key", value=key, inline=False)
                    embed.add_field(name="Expiration Time", value=expire, inline=False)
                else:
                    embed.add_field(name="Error", value=f"Received status code {response.status}", inline=False)
                    embed.add_field(name="Response", value=str(response_data), inline=False)

                await interaction.response.send_message(embed=embed, view=add_invite_button())
                
        elif command == "status":
            async with session.get(f"{API_BASE_URL}/status") as response:
                data = await response.json()
                embed = discord.Embed(title="API Status", description=data)
                await interaction.response.send_message(embed=embed, view=add_invite_button())

        else:
            await interaction.response.send_message("Invalid command. Please choose a valid command.", view=add_invite_button())

# Start the Flask app in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Start the bot
bot.run(TOKEN)
