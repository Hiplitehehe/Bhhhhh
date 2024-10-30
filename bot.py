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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync()
    print("Commands synced")

@bot.tree.command(name="multi_command")
@app_commands.describe(
    option="Choose an option to execute",
    link="Enter a link if needed",
    url="Enter a URL if needed"
)
async def multi_command(interaction: discord.Interaction, option: str, link: str = None, url: str = None):
    """Execute multiple commands with one command."""
    async with aiohttp.ClientSession() as session:
        try:
            if option == "fluxus" and link:
                async with session.get(f"{API_BASE_URL}/api/fluxus?link={link}") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "bloxfruits_stock":
                async with session.get(f"{API_BASE_URL}/api/bloxfruits/stock") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "addlink" and url:
                async with session.get(f"{API_BASE_URL}/TestHub/addlink?url={url}") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "flux_gen":
                async with session.get(f"{API_BASE_URL}/flux_gen") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "arc_gen":
                async with session.get(f"{API_BASE_URL}/arc_gen") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "gen_key":
                async with session.get("https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api/add") as response:
                    response_data = await response.json()
                    embed = discord.Embed(title="API Response", color=discord.Color.blue())

                    if response.status == 201:
                        key = response_data.get('key', 'No key available')
                        expire = response_data.get('expire', 'No expiration provided')
                        if isinstance(expire, int) and expire > 1_000_000_000_000:
                            expire = datetime.fromtimestamp(expire / 1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            expire = "Invalid expiration format"
                        embed.add_field(name="Generated Key", value=key, inline=False)
                        embed.add_field(name="Expiration Time", value=expire, inline=False)
                        await interaction.response.send_message(embed=embed)
                    else:
                        embed.add_field(name="Error", value=f"Received status code {response.status}", inline=False)
                        await interaction.response.send_message(embed=embed)

            elif option == "hydro_gen":
                async with session.get(f"{API_BASE_URL}/hydro_gen") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "boost_ink" and url:
                async with session.get(f"{API_BASE_URL}/boost.ink?url={url}") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)

            elif option == "status":
                async with session.get(f"{API_BASE_URL}/status") as response:
                    data = await response.json()
                    await interaction.response.send_message(data)
            else:
                await interaction.response.send_message("Invalid option or missing parameters.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

# Start the Flask app in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Start the bot
bot.run(TOKEN)
