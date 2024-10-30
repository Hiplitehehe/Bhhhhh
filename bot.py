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
    flask_app.run(host='0.0.0.0', port=5000)

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

class CommandView(discord.ui.View):
    """A view that contains command buttons."""
    
    @discord.ui.button(label="Fluxus", style=discord.ButtonStyle.primary)
    async def fluxus_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "fluxus")

    @discord.ui.button(label="Blox Fruits Stock", style=discord.ButtonStyle.primary)
    async def bloxfruits_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "bloxfruits_stock")

    @discord.ui.button(label="Add Link", style=discord.ButtonStyle.primary)
    async def addlink_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "addlink")

    @discord.ui.button(label="Flux Gen", style=discord.ButtonStyle.primary)
    async def flux_gen_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "flux_gen")

    @discord.ui.button(label="Arc Gen", style=discord.ButtonStyle.primary)
    async def arc_gen_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "arc_gen")

    @discord.ui.button(label="Generate Key", style=discord.ButtonStyle.primary)
    async def gen_key_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "gen_key")

    @discord.ui.button(label="Status", style=discord.ButtonStyle.primary)
    async def status_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.execute_command(interaction, "status")

    async def execute_command(self, interaction: discord.Interaction, command: str):
        """Execute the command based on the button clicked."""
        async with aiohttp.ClientSession() as session:
            if command == "fluxus":
                link = interaction.user.mention  # Use user mention or prompt for input
                async with session.get(f"{API_BASE_URL}/api/fluxus?link={link}") as response:
                    data = await response.json()
                    embed = discord.Embed(title="Fluxus Data", description=data)
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "bloxfruits_stock":
                async with session.get(f"{API_BASE_URL}/api/bloxfruits/stock") as response:
                    data = await response.json()
                    embed = discord.Embed(title="Blox Fruits Stock", description=data)
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "addlink":
                url = "http://example.com"  # Replace with actual user input handling
                async with session.get(f"{API_BASE_URL}/TestHub/addlink?url={url}") as response:
                    data = await response.json()
                    embed = discord.Embed(title="Add Link", description=data)
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "flux_gen":
                async with session.get(f"{API_BASE_URL}/flux_gen") as response:
                    data = await response.json()
                    embed = discord.Embed(title="Random Flux HWID", description=data)
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "arc_gen":
                async with session.get(f"{API_BASE_URL}/arc_gen") as response:
                    data = await response.json()
                    embed = discord.Embed(title="Random Arc HWID", description=data)
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "gen_key":
                async with session.get("https://code-o4xxbr303-hiplitehehes-projects.vercel.app/api/add") as response:
                    response_data = await response.json()
                    embed = discord.Embed(title="API Response", color=discord.Color.blue())

                    if response.status == 201:
                        key = response_data.get('key')
                        embed.description = f"Generated Key: {key}"
                    else:
                        embed.description = "Failed to generate a key."
                    await interaction.response.edit_message(embed=embed, view=add_invite_button())

            elif command == "status":
                embed = discord.Embed(title="Bot Status", description="The bot is online and running!")
                await interaction.response.edit_message(embed=embed, view=add_invite_button())

def add_invite_button():
    """Add an 'Add Me!' button."""
    button = discord.ui.Button(label="Add Me!", url=INVITE_URL)
    view = discord.ui.View()
    view.add_item(button)
    return view

@bot.command()
async def commands(ctx):
    """Send a message with command buttons."""
    view = CommandView()
    await ctx.send("Please select a command:", view=view)

# Run the bot
bot.run(TOKEN)
