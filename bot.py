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
import requests
import json
from discord import ButtonStyle, ui
import asyncio
from discord import app_commands

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
keywords = ["hello", "key", "detected"]  # Add more keywords as needed
trigger_word = "hello"  # The word that triggers the response
auto_response_text = "Hello! How can I assist you today?"
JOURNEY_API_URL = "https://api.zukijourney.com/v1/chat/completions"
JOURNEY_API_KEY = ""
# Specific channel ID where the response should trigger
auto_response_channel_id = 1284874380194611200  # Replace with your specific channel ID
RANDOM_W = ""
discord_webhook_url = "https://discord.com/api/webhooks/1304997756687093811/TeWIS5VyfXXGiHleog5xCzsZrBXskkVBlCSzQkdNjmcW2s2ieFXvB9nURKEhNx5WupEC"
platoboost_url = "https://gateway.platoboost.com/a/8?id="
bypass_url = "https://bhhhhh-1-sebx.onrender.com"

# Command to trigger the bypass with HWID

def time_convert(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours} Hours {mins} Minutes"

async def send_discord_webhook(link, channel):
    embed = discord.Embed(
        title="Security Check Detected!",
        description=f"**Please solve the Captcha**: [Open]({link})",
        color=0x5783719
    )
    await channel.send(embed=embed)

async def get_turnstile_response():
    await asyncio.sleep(1)  # Simulated delay for response
    return "simulated-captcha-response"

async def delta(id, channel):
    try:
        response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        if response.status_code != 200:
            raise Exception(f"Access to Platoboost failed: {response.status_code}")

        already_pass = response.json()
        if 'key' in already_pass:
            time_left = time_convert(already_pass['minutesLeft'])
            await channel.send(f"**INFO** Remaining time: {time_left} - KEY: {already_pass['key']}")
            return

        captcha = already_pass.get('captcha')
        post_data = {
            "captcha": await get_turnstile_response() if captcha else "",
            "type": "Turnstile" if captcha else ""
        }
        response = requests.post(
            f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}",
            json=post_data
        )

        if response.status_code != 200:
            security_check_link = f"{platoboost_url}{id}"
            await send_discord_webhook(security_check_link, channel)
            raise Exception("Security Check: Notified on Discord!")

        loot_link = response.json()['redirect']
        await asyncio.sleep(1)  # Simulated delay

        r = requests.utils.urlparse(loot_link).query.split("r=")[-1]
        decoded = requests.utils.unquote(r).encode('ascii')
        tk = requests.utils.parse_qs(decoded)['tk'][0]
        await asyncio.sleep(5)  # Simulated delay

        response = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/{tk}")
        if response.status_code != 200:
            raise Exception(f"Key creation failed: {response.status_code}")

        response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        pass_data = response.json()
        if 'key' in pass_data:
            time_left = time_convert(pass_data['minutesLeft'])
            await channel.send(f"**INFO** Remaining time: {time_left} - KEY: {pass_data['key']}")
    except Exception as e:
        await channel.send(f"**ERROR**: {e}")

# This command will be the parent command
@bot.tree.command(name="bypass", description="Start the bypassing process using a specific HWID")
@app_commands.describe(hwid="The HWID to bypass.")
async def bypass_command(interaction: discord.Interaction, hwid: str):
    await interaction.response.send_message(f"Starting bypass for HWID: {hwid}")
    await delta(hwid, interaction.channel)

# Subcommand to start HWID bypass

# Define the hangman stagesjjjj


# Define the hangman stages (visual representation of wrong attempts)
HANGMAN_STAGES = [
    "```\n  -----\n  |   |\n      |\n      |\n      |\n      |\n  -----\n```",  # 0 incorrect guesses
    "```\n  -----\n  |   |\n  O   |\n      |\n      |\n      |\n  -----\n```",  # 1 incorrect guess
    "```\n  -----\n  |   |\n  O   |\n  |   |\n      |\n      |\n  -----\n```",  # 2 incorrect guesses
    "```\n  -----\n  |   |\n  O   |\n /|   |\n      |\n      |\n  -----\n```",  # 3 incorrect guesses
    "```\n  -----\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n  -----\n```",  # 4 incorrect guesses
    "```\n  -----\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n  -----\n```",  # 5 incorrect guesses
    "```\n  -----\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n  -----\n```"   # 6 incorrect guesses (game over)
]

# Fetch a random word from the API
def fetch_random_word():
    url = "https://random-word-api.herokuapp.com/word?number=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0].upper()  # Convert word to uppercase
    return "HANGMAN"  # Default word if API fails

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the game variables
guessed_letters = set()
incorrect_guesses = 0
HANGMAN_WORD = fetch_random_word()
MAX_INCORRECT_GUESSES = len(HANGMAN_STAGES) - 1

def display_word():
    """Display the word with unguessed letters as underscores."""
    return ' '.join([letter if letter in guessed_letters else '_' for letter in HANGMAN_WORD])

# Create alphabet buttons (A-Z)
def create_alphabet_buttons(page=0):
    buttons = []
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Split alphabet into two parts, A-M and N-Z, and show buttons for the selected page
    start = page * 13
    end = start + 13
    for letter in alphabet[start:end]:
        button = discord.ui.Button(label=letter, custom_id=letter)
        buttons.append(button)
    
    return buttons

# Next and Previous buttons to navigate pages
class AlphabetPaginationView(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=60.0)
        self.page = page
        self.update_buttons()

    def update_buttons(self):
        # Remove old buttons
        for button in self.children:
            self.remove_item(button)

        # Add new alphabet buttons for the current page
        buttons = create_alphabet_buttons(self.page)
        for button in buttons:
            self.add_item(button)

        # Add previous and next page navigation buttons
        if self.page > 0:
            self.add_item(discord.ui.Button(label="Previous", custom_id="previous"))
        self.add_item(discord.ui.Button(label="Next", custom_id="next"))

    async def on_button_click(self, interaction: discord.Interaction):
        if interaction.custom_id == "next":
            self.page += 1
        elif interaction.custom_id == "previous":
            self.page -= 1

        self.update_buttons()
        await interaction.response.edit_message(view=self)

# Create a function to start a new hangman game
@bot.tree.command(name="hangman", description="Play hangman with a random word!")
async def hangman(interaction: discord.Interaction):
    global guessed_letters, incorrect_guesses, HANGMAN_WORD
    guessed_letters = set()
    incorrect_guesses = 0
    HANGMAN_WORD = fetch_random_word()  # Fetch a new word each time the game is started

    embed = discord.Embed(title="Hangman Game", description="Start guessing letters!")
    embed.add_field(name="Word", value=display_word(), inline=False)
    embed.add_field(name="Attempts Left", value=HANGMAN_STAGES[incorrect_guesses], inline=False)

    # Create a view for alphabet buttons with pagination
    view = AlphabetPaginationView()

    # Send the initial embed with the alphabet buttons
    await interaction.response.send_message(embed=embed, view=view)

    # Handle button interaction for guessing letters
    def check(interaction: discord.Interaction):
        return interaction.user == interaction.user and interaction.custom_id in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    while incorrect_guesses < MAX_INCORRECT_GUESSES:
        try:
            # Wait for button click
            interaction = await bot.wait_for("interaction", check=check, timeout=60.0)
            guess = interaction.custom_id.lower()

            # If letter has already been guessed
            if guess in guessed_letters:
                await interaction.response.send_message(f"You've already guessed '{guess}'. Try again!")
                continue

            guessed_letters.add(guess)

            if guess in HANGMAN_WORD.lower():
                await interaction.response.send_message(f"Good guess! '{guess}' is in the word.")
            else:
                incorrect_guesses += 1
                await interaction.response.send_message(f"Incorrect guess! '{guess}' is not in the word.")

            # Update the embed with the current state of the game
            embed = discord.Embed(title="Hangman Game", description="Start guessing letters!")
            embed.add_field(name="Word", value=display_word(), inline=False)
            embed.add_field(name="Attempts Left", value=HANGMAN_STAGES[incorrect_guesses], inline=False)
            await interaction.edit_original_response(embed=embed)

            # Check for win condition
            if all(letter in guessed_letters for letter in HANGMAN_WORD.lower()):
                await interaction.response.send_message(f"Congratulations! You've guessed the word: {HANGMAN_WORD} 🎉")
                break

        except asyncio.TimeoutError:
            await interaction.response.send_message("Time's up! The word was: " + HANGMAN_WORD)
            break

    # If the user used up all attempts
    if incorrect_guesses >= MAX_INCORRECT_GUESSES:
        await interaction.response.send_message(f"Game over! You've run out of attempts. The word was: {HANGMAN_WORD}")

    # Add logic for guessing letters, updating the embed as needed, etc.

# Define a function to send requests to the Journey API
def get_ai_response(user_message):
    headers = {
        'Authorization': f'Bearer {JOURNEY_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "caramelldansen-1",  # Replace with the model you want to use
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    # Send the POST request to the Journey API
    response = requests.post(JOURNEY_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the /ask command
@bot.tree.command(name="ask", description="Ask the AI a question!")
async def ask_command(interaction: discord.Interaction, question: str):
    await interaction.response.defer()  # Acknowledge the command
    ai_response = get_ai_response(question)  # Get the AI response from the Journey API
    await interaction.followup.send(ai_response)  # Send the response back to Discord

@bot.event
async def on_message(message):
    # Ensure the message is from a different user (not the bot itself)
    if message.author != bot.user:
        # Check if the message is in the correct channel and contains the trigger word
        if message.channel.id == auto_response_channel_id and trigger_word in message.content.lower():
            await message.channel.send(auto_response_text)
    
    # Process commands normally after handling messages
    await bot.process_commands(message)

@bot.command(name="test_autorespond")
async def test_autorespond(ctx):
    # Let the user know the bot is working
    await ctx.send(f"Auto-response is set to trigger when '{trigger_word}' is detected in the channel.")

# Event listener to check messages and respo
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    keywords = ["hello", "key", "detected"]

    for keyword in keywords:
        if keyword.lower() in message.content.lower():
            await message.channel.send(f"Keyword '{keyword}' detected!")
            break
    # Ensure that commands still work if the bot needs to process any commands
    await bot.process_commands(message)

# Ensure the bot is ready and syncs slash commands if used
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands if you're using them
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Bot is ready.")

    # Print the success message and synced command names
    for command in bot.tree.get_commands():
        print(f"Command '{command.name}' has been successfully synced!")

# Command to set the welcome channel
@bot.tree.command(name="setwelcome", description="Sets the welcome channel for the server.")
async def set_welcome_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global welcome_channel
    welcome_channel = channel

    # Send a test welcome message once during the setup of the channel
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
        # Send the welcome embed message only once here
        await welcome_channel.send(embed=embed)
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
async def set_leave(interaction: discord.Interaction, channel: discord.TextChannel = None, message: str = None):
    """Command to set the leave channel and message format."""
    global leave_channel, leave_message_template
    
    # If no channel is provided, use a default channel (you can set this to any channel ID you prefer)
    if not channel:
        channel = interaction.guild.system_channel  # Default to the system channel (if it exists)
        if not channel:
            return await interaction.response.send_message("No valid channel found to set the leave message.", ephemeral=True)
    
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

@bot.tree.command(name="bypass", description="Start bypass with a given HWID")
async def bypass_command(interaction: discord.Interaction, hwid: str):
    """Command to bypass using the provided HWID."""
    
    # Prepare the data payload
    data = {
        "hwid": hwid
    }

    try:
        # Send POST request to the bypass API
        response = requests.post(bypass_url, json=data)

        # Always attempt to extract JSON response, even in case of failure
        if response.status_code == 200:
            api_response = response.json()  # Parse the JSON response
            message = f"Bypass successful! API Response: {api_response}"
        else:
            api_response = response.json()  # Parse the error JSON response
            message = f"Failed to initiate bypass. API Response: {api_response}"

    except Exception as e:
        # In case of any exceptions (e.g., network errors)
        api_response = {"error": str(e)}
        message = f"An error occurred while trying to bypass. API Response: {api_response}"

    # Send the message with the API response, regardless of success or failure
    await interaction.response.send_message(message)

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
            
@bot.tree.command(name="genkey", description="Responds with sjjsndnd.")
async def say_command(interaction: discord.Interaction):
    await interaction.response.send_message("sjjsndnd")
                
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
