import discord
from discord.ext import commands
import aiohttp
import os
from flask import Flask, jsonify

# Create a Flask app
flask_app = Flask(__name__)

@flask_app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

def run_flask():
    """Run the Flask app."""
    flask_app.run(host='0.0.0.0', port=5050)

# Load your token from an environment variable or file
TOKEN = os.getenv('token')  # Set your bot token as an environment variable

# Create a bot instance
bot = commands.Bot(command_prefix='>', intents=discord.Intents.default())

API_BASE_URL = "https://bhhhhh-2.onrender.com/"  # Replace with your actual API domain
INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1289846587333546073&permissions=8&integration_type=0&scope=bot"  # Replace with your bot's invite URL

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print("Bot is ready.")
    await bot.tree.sync()  # Sync slash commands with Discord

@bot.tree.command(name="fluxus")
async def fluxus(interaction: discord.Interaction, link: str = None):
    """Handle the Fluxus command with an optional link."""
    async with aiohttp.ClientSession() as session:
        # Use the provided link or mention the user if no link is given
        if link is None:
            link = interaction.user.mention
        async with session.get(f"{API_BASE_URL}/api/fluxus?link={link}") as response:
            data = await response.json()
            embed = discord.Embed(title="Fluxus Data", description=data)
            await interaction.response.send_message(embed=embed, ephemeral=True)  # Set ephemeral to False

@bot.tree.command(name="bloxfruits_stock")
async def bloxfruits_stock(interaction: discord.Interaction):
    """Handle the Blox Fruits Stock command."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/api/bloxfruits/stock") as response:
            data = await response.json()
            embed = discord.Embed(title="Blox Fruits Stock", description=data)
            await interaction.response.send_message(embed=embed, ephemeral=False)  # Set ephemeral to False

@bot.tree.command(name="addlink")
async def addlink(interaction: discord.Interaction, url: str):
    """Handle the Add Link command."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/TestHub/addlink?url={url}") as response:
            data = await response.json()
            embed = discord.Embed(title="Add Link", description=data)
            await interaction.response.send_message(embed=embed, ephemeral=False)  # Set ephemeral to False

@bot.tree.command(name="flux_gen")
async def flux_gen(interaction: discord.Interaction):
    """Handle the Flux Gen command."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/flux_gen") as response:
            data = await response.json()
            embed = discord.Embed(title="Random Flux HWID", description=data)
            await interaction.response.send_message(embed=embed, ephemeral=False)  # Set ephemeral to False

@bot.tree.command(name="arc_gen")
async def arc_gen(interaction: discord.Interaction):
    """Handle the Arc Gen command."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/arc_gen") as response:
            data = await response.json()
            embed = discord.Embed(title="Random Arc HWID", description=data)
            await interaction.response.send_message(embed=embed, ephemeral=False)  # Set ephemeral to False

@bot.tree.command(name="gen_key")
async def gen_key(interaction: discord.Interaction):
    """Handle the Generate Key command."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api/add") as response:
            response_data = await response.json()
            
            if response.status == 201:
                key = response_data.get('key')
                await interaction.response.send_message("Key generation was successful!", ephemeral=False)  # First message
                await interaction.followup.send(f"Generated Key: {key}", ephemeral=True)  # Second message
            else:
                await interaction.response.send_message("Failed to generate a key.", ephemeral=False)  # Single failure message

@bot.tree.command(name="status")
async def status_command(interaction: discord.Interaction):
    """Handle the Status command."""
    embed = discord.Embed(title="Bot Status", description="The bot is online and running!")
    await interaction.response.send_message(embed=embed, ephemeral=False)  # Set ephemeral to False

@bot.tree.command(name="commands")
async def commands_list(interaction: discord.Interaction):
    """Send a message with a list of available commands."""
    command_list = """
    **Available Commands:**
    /fluxus - Handle the Fluxus command (optional link)
    /bloxfruits_stock - Handle the Blox Fruits Stock command
    /addlink <url> - Handle the Add Link command
    /flux_gen - Handle the Flux Gen command
    /arc_gen - Handle the Arc Gen command
    /gen_key - Handle the Generate Key command
    /status - Get the bot's status
    """
    await interaction.response.send_message(command_list, ephemeral=False)  # Set ephemeral to False

# Run the bot
bot.run(TOKEN)
