import discord
from discord.ext import commands
import aiohttp
import os
from flask import Flask, jsonify
from flask import Flask, jsonify
import threading
import time, secrets
import base64
import urllib

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
intents = discord.Intents.default()
intents.members = True  # Enable member join event

# Initialize the bot with the correct command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

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
welcome_channel = None
welcome_message = None
leave_channel = None
leave_message_template = "We’re sad to see you go, <@{user.id}>! Best of luck!"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print("Bot is ready.")
    await bot.tree.sync()
    print("Slash commands have been synced.")

# Command to set the welcome channel
@bot.tree.command(name="setwelcome", description="Sets the welcome channel for the server.")
async def set_welcome_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global welcome_channel
    welcome_channel = channel

    # Send a test welcome message
    embed = discord.Embed(
        title="Welcome Channel Set!",
        description="This is a test message. The welcome channel is now set.",
        color=discord.Color.green()
    )
    await channel.send(embed=embed)
    await interaction.response.send_message(f"Welcome channel has been set to {channel.mention}.", ephemeral=True)

# Event when a new member joins
@bot.event
async def on_member_join(member: discord.Member):
    if welcome_channel:
        embed = discord.Embed(
            title="Welcome to the Server!",
            description=f"Welcome {member.mention} to the server! 🎉 We're excited to have you with us and type /genkey and your Roblox user to get key in getkey channel.",
            color=discord.Color.blue()
        )
        await welcome_channel.send(embed=embed)
        await welcome_channel.send(f"{member.mention}, feel free to explore and introduce yourself!")
    else:
        print("Welcome channel not set. Please set the welcome channel using the /setwelcome command.")

@bot.event
async def on_member_remove(member: discord.Member):
    """Send a customized leave message when a user leaves."""
    if leave_channel and leave_message_template:
        # Format the message by inserting the member's ID
        leave_message = leave_message_template.replace("{user_id}", str(member.id))
        await leave_channel.send(leave_message)

@bot.tree.command(name="setleave", description="Sets the leave message channel and message format.")
async def set_leave(interaction: discord.Interaction, channel: discord.TextChannel, message: str = None):
    """Command to set the leave channel and message format."""
    global leave_channel, leave_message_template
    leave_channel = channel
    
    # If the user provided a custom message, use it; otherwise, use the default message
    if message:
        leave_message_template = message
    else:
        leave_message_template = "We're sad to see you go, <@{user_id}>!"  # Use default message if none provided
    
    # Immediately test the message by simulating a leave event
    test_member = interaction.user  # You can use the user who ran the command for testing purposes
    test_leave_message = leave_message_template.replace("{user_id}", str(test_member.id))
    await leave_channel.send(test_leave_message)
    
    await interaction.response.send_message(
        f"Leave channel has been set to {channel.mention}.\nLeave message set to:\n{leave_message_template}", ephemeral=True
    )
    
# Command to test the welcome message (no manual message required)
@bot.tree.command(name="testwelcome", description="Sends a test welcome embed to the set welcome channel.")
async def test_welcome(interaction: discord.Interaction):
    """Command to send a test welcome embed to the welcome channel."""
    if welcome_channel and welcome_message:
        # Create an embed for the welcome message (auto-use the welcome message set)
        embed = discord.Embed(
            title="Welcome to the Server!",
            description=f"Welcome {interaction.user.mention} to the server! 🎉 We're excited to have you with us.",
            color=discord.Color.green()  # Customize color here
        )
        embed.add_field(name="Get Started", value="Please introduce yourself in the #introductions channel.")
        embed.add_field(name="Read Rules", value="Don't forget to check out the #rules channel.")
        
        # Send the embed to the welcome channel
        await welcome_channel.send(embed=embed)
        await interaction.response.send_message("Test welcome embed sent to the welcome channel.", ephemeral=True)
    else:
        await interaction.response.send_message("Welcome channel or message not set. Please set them using the /setwelcome command.", ephemeral=True)

@bot.tree.command(name="say", description="Bot repeats the message you provide twice in embeds.")
async def say(interaction: discord.Interaction, message: str):
    """Makes the bot say a message in the channel twice as embeds without replying."""

    # Create the embed for the message
    embed = discord.Embed(title="", description=message, color=discord.Color.blue())

    # Send the first embed
    await interaction.response.defer()  # Prevents initial reply-style message
    await interaction.followup.send(embed=embed)

    # Send the second embed
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="lock", description="Locks a channel to make it read-only.")
@commands.has_permissions(administrator=True)  # Ensure only admins can use this command
async def lock_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Locks the specified channel, making it read-only for regular members."""
    
    channel = channel or interaction.channel  # Use the specified channel or the one where the command was used
    
    # Attempt to update permissions to make the channel read-only for @everyone
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False  # Prevents everyone from sending messages in the channel

    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(f"{channel.mention} has been locked and is now read-only.", ephemeral=True)

@lock_channel.error
async def lock_channel_error(interaction: discord.Interaction, error):
    # Error handling if the user doesn't have permission
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred while locking the channel.", ephemeral=True)

@bot.tree.command(name="search", description="Search for a term using the ScriptBlox API.")
async def search(interaction: discord.Interaction, search_input: str, mode_select: str, page: int = 1):
    """Fetches search results from the ScriptBlox API with pagination support."""
    
    # Construct the API URL
    api_url = f"https://scriptblox-api-proxy.vercel.app/api/search?q={urllib.parse.quote(search_input)}&mode={urllib.parse.quote(mode_select)}&page={page}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()  # Parse the JSON response
                # You can format the response here as needed
                await interaction.response.send_message(f"Results for '{search_input}' in mode '{mode_select}', page {page}:\n{data}", ephemeral=True)
            else:
                # Send the error message received from the API
                error_message = await response.text()  # Get the text of the error response
                await interaction.response.send_message(f"Error: {error_message}", ephemeral=True)

@bot.tree.command(name="delta", description="Fetch a bypassed link for the provided URL.")
async def bypass(interaction: discord.Interaction, url: str):
    """Sends a URL to the executor bypass API and returns the bypassed link."""
    api_endpoint = f"http://de01-2.uniplex.xyz:1575/api/executorbypass?url={url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_endpoint) as response:
            # Get the response body as text for debugging
            response_text = await response.text()
            print(f"API Request URL: {api_endpoint}")  # Print the URL being accessed
            print(f"API Response if not work ask axera to decode delta lootlabs (Status Code: {response.status}): {response_text}")  # Print the status code and response text

            # Always send the response text to Discord
            await interaction.response.send_message(
                f"API request completed with status code {response.status}. Response: {response_text}",
                ephemeral=False
            )

            if response.status == 200:
                try:
                    data = await response.json()  # Attempt to parse the response as JSON
                    bypassed_link = data.get("bypassed_link")  # Adjust based on the actual API response structure

                    if bypassed_link:
                        await interaction.followup.send(f"Bypassed Link: {bypassed_link}", ephemeral=True)
                    else:
                        # If the key doesn't exist, send the entire response for debugging
                        await interaction.followup.send("Bypassed link not found in response. Full response: " + response_text, ephemeral=True)
                        print("Bypassed link not found in response:", response_text)
                except ValueError as e:
                    await interaction.followup.send("Error processing the response. Response was not valid JSON.", ephemeral=True)
                    print(f"JSON parsing error: {e}, Response: {response_text}")
            else:
                # Send the full response text even if there's an error
                await interaction.followup.send(
                    f"API request failed: {response_text}",
                    ephemeral=True
                )

@bot.tree.command(name="bypassbeta", description="Fetch a bypassed link for the provided URL.")
async def bypass(interaction: discord.Interaction, url: str):
    """Sends a URL to the executor bypass API and returns the bypassed link."""
    api_endpoint = f"http://de01-2.uniplex.xyz:1575/api/executorbypass?url={url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_endpoint) as response:
            # Get the response body as text (not JSON)
            response_text = await response.text()
            print(f"API Request URL: {api_endpoint}")  # Print the URL for debugging
            print(f"API Response (Status Code: {response.status}): {response_text}")  # Print status and full response text

            # Send the API response to the user, including status code and text
            await interaction.response.send_message(
                f"API Response (Status: {response.status}): {response_text}",
                ephemeral=True
                    )
            
@bot.tree.command(name="genkey")
async def jdjd_command(interaction: discord.Interaction):
    """Responds with 'key ' when the /genkey command is invoked."""
    # Send the response to the channel
    await interaction.response.send_message("Key is B3f9xT2W8kZ1uL7jP6yV")
    print("Responded with 'ejjeje' for /jdjd command.")

                

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

@bot.tree.command(name="search_api")
async def search_api(interaction: discord.Interaction, search_input: str, mode_select: str):
    """Search the given input with the API and return the results."""
    api_url = f"https://scriptblox-api-proxy.vercel.app/api/search?q={search_input}&mode={mode_select}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                # Assuming the response contains a 'results' field for this example
                results = data.get('results', [])
                if results:
                    formatted_results = "\n".join([f"- {item}" for item in results[:5]])  # Show top 5 results
                    embed = discord.Embed(
                        title="Search Results",
                        description=formatted_results,
                        color=discord.Color.blue()
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("No results found.", ephemeral=True)
            else:
                error_text = await response.text()
                await interaction.response.send_message(
                    f"API request failed with status code {response.status}.\nDetails: {error_text}",
                    ephemeral=True
                )

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
