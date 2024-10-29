import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

# Load your token from an environment variable or file
TOKEN = ('token')  # Set your bot token as an environment variable

# Create a bot instance
bot = commands.Bot(command_prefix='>', intents=discord.Intents.default())

API_BASE_URL = "http://127.0.0.1:5000"  # Replace with your actual API domain

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

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
async def status(interaction: discord.Interaction):
    """Check the health of the API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/status") as response:
            data = await response.json()
            await interaction.response.send_message(data)

# Start the bot
bot.run(TOKEN)
