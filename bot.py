import discord
from discord.ext import commands
import aiohttp
import os
from flask import Flask, jsonify
from flask import Flask, jsonify
import threading
import time, secrets
import base64

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

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # GitHub token from environment variable
REPO_NAME = "Bhhhhh"  # Your GitHub repository name
FILE_PATH = "Key"  # Path to the file you want to update
API_BASE_URL = "https://bhhhhh-2.onrender.com/"  # Replace with your actual API domain
INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1289846587333546073&permissions=8&integration_type=0&scope=bot"  # Replace with your bot's invite URL
REPO_NAME = "Hiplitehehe/Bhhhhh"  
FILE_PATH = "Key"  # Path to the file you want to update
API_BASE_URL = "https://bhhhhh-2.onrender.com/"  # Replace with your actual API domain
INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1289846587333546073&permissions=8&integration_type=0&scope=bot"  # Replace with your bot's invite URL
AUTO_EXPIRATION = 3 * 24 * 60 * 60  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print("Bot is ready.")
    await bot.tree.sync()  # Sync slash commands with Discord

@bot.tree.command(name="genkey")
async def gen_key(interaction: discord.Interaction, username: str):
    """Generate a key for a user with a 3-day expiration time."""

    # Generate a secure random key and set it to expire in 3 days
    generated_key = secrets.token_hex(16)
    expiration_time = int(time.time()) + AUTO_EXPIRATION
    new_content = f"{username}:{generated_key}:{expiration_time}\n"

    # Send the first message while the bot works on fetching/updating
    await interaction.response.send_message("Generating a key for you, please wait...", ephemeral=False)

    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with session.get(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", headers=headers) as response:
            if response.status != 200:
                await interaction.followup.send(
                    f"Failed to fetch the existing file. GitHub API response: {await response.text()}",
                    ephemeral=True
                )
                return

            existing_file_data = await response.json()
            existing_content = base64.b64decode(existing_file_data['content']).decode()
            sha = existing_file_data['sha']

        # Append new key info to the existing file content
        updated_content = existing_content + new_content
        encoded_content = base64.b64encode(updated_content.encode()).decode()

        payload = {
            "message": f"Add new key for {username}",
            "content": encoded_content,
            "sha": sha,
            "branch": "main"
        }

        async with session.put(f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}", json=payload, headers=headers) as response:
            if response.status == 200:
                # Send a second follow-up message with the key and expiration
                await interaction.followup.send(f"Key for {username}: `{generated_key}` (expires in 3 days)", ephemeral=True)
            else:
                await interaction.followup.send(
                    f"Failed to update the file. GitHub API response: {await response.text()}",
                    ephemeral=True
                 )
                

async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print("Bot is ready.")
    await bot.tree.sync()  # Sync slash commands with Discord

@bot.tree.command(name="test")
async def gen_key(interaction: discord.Interaction, username: str):
    """Generate a key for a user and update an existing file in a GitHub repository."""
    
    # Generate a secure random key
    key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string
    new_content = f"{username}: {key}\n"  # Content to bind the key to the username

    # Create a session to interact with the GitHub API
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Step 1: Fetch the current content of the file
        async with session.get(f"https://api.github.com/repos/Hiplitehehe/{REPO_NAME}/contents/{FILE_PATH}", headers=headers) as response:
            if response.status != 200:
                await interaction.response.send_message(
                    "Failed to fetch the existing file. GitHub API response: " + str(await response.text()),
                    ephemeral=True
                )
                return

            existing_file_data = await response.json()
            existing_content = base64.b64decode(existing_file_data['content']).decode()  # Decode existing content
            sha = existing_file_data['sha']  # Get the SHA of the file for updating

        # Step 2: Append the new content to the existing content
        updated_content = existing_content + new_content
        encoded_content = base64.b64encode(updated_content.encode()).decode()  # Re-encode the updated content

        # Step 3: Update the file with the new content
        payload = {
            "message": f"Update Key file with new generated key for {username}",
            "content": encoded_content,
            "sha": sha,  # The SHA of the file to update
            "branch": "main"  # Specify the branch where the file should be updated
        }

        async with session.put(f"https://api.github.com/repos/Hiplitehehe/{REPO_NAME}/contents/{FILE_PATH}", json=payload, headers=headers) as response:
            if response.status == 200:  # HTTP status for success
                await interaction.response.send_message(f"File updated successfully! New Key for {username}: {key}", ephemeral=False)
            else:
                await interaction.response.send_message(
                    "Failed to update the file. GitHub API response: " + str(await response.text()),
                    ephemeral=True
            )
                
@bot.tree.command(name="hggg")
async def gen_key(interaction: discord.Interaction):
    """Handle the Generate Key command and create a new file in an existing GitHub repository."""
    github_token = os.getenv('GITHUB_TOKEN')  # Your GitHub token from an environment variable
    repo_name = "Bhhhhh"  # Your GitHub repository name
    file_name = f"generated_key_{interaction.user.id}_{int(time.time())}.txt"  # Unique file name
    file_content = "This is a generated key."  # Content of the file (modify as needed)

    # Prepare file content for GitHub API
    encoded_content = base64.b64encode(file_content.encode()).decode()

    # Create file in GitHub repository
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "message": f"Add generated key file: {file_name}",
            "content": encoded_content,
            "branch": "main"  # Specify the branch where the file should be created
        }
        
        try:
            async with session.put(f"https://api.github.com/repos/Hiplitehehe/{repo_name}/contents/{file_name}", json=payload, headers=headers) as response:
                if response.status == 201:  # HTTP status for created
                    await interaction.response.send_message("File creation was successful!", ephemeral=False)
                else:
                    await interaction.response.send_message("Failed to create file. GitHub API response: " + str(await response.text()), ephemeral=True)
        except aiohttp.ClientError as e:
            await interaction.response.send_message(f"Error creating file: {str(e)}", ephemeral=True)

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

@bot.tree.command(name="cvvv")
async def gen_key(interaction: discord.Interaction):
    """Handle the Generate Key command and create a new GitHub repository with 'main' as the default branch."""
    github_token = os.getenv('GITHUB_TOKEN')  # Your GitHub token from an environment variable
    repo_name = f"repo-{interaction.user.id}-{int(time.time())}"  # Unique repo name based on user ID and timestamp
    username = "Hiplitehehe"  # Your GitHub username

    # Create GitHub repository
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "name": repo_name,
            "private": False,  # Set to True if you want to create a private repository
            "description": "This repository was created by a Discord bot.",
            "auto_init": True,  # Automatically create an initial commit
        }

        try:
            async with session.post(f"https://api.github.com/user/repos", json=payload, headers=headers) as response:
                if response.status == 201:  # HTTP status for created
                    response_data = await response.json()
                    repo_url = response_data.get('html_url')  # Get the URL of the created repository
                    await interaction.response.send_message("Key generation was successful!", ephemeral=False)
                    await interaction.followup.send(f"Repository created: {repo_url}", ephemeral=True)
                else:
                    await interaction.response.send_message("Failed to generate a key. GitHub API response: " + str(await response.text()), ephemeral=True)
        except aiohttp.ClientError as e:
            await interaction.response.send_message(f"Error creating repository: {str(e)}", ephemeral=True)
        
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

@bot.tree.command(name="delete")
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

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()


# Run the bot
bot.run(TOKEN)
