import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if token exists
if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN not found!")
    exit(1)

# ======================
# FLASK SERVER FOR PINGER
# ======================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    """Run Flask server in a separate thread"""
    app.run(host='0.0.0.0', port=8080)

# ======================
# DISCORD BOT
# ======================
# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready! Logged in as {bot.user.name}')
    print(f'🔗 Invite URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    
    # Set status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help"
        )
    )

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

@bot.command(name='hello')
async def hello(ctx):
    """Say hello"""
    await ctx.send(f'👋 Hello {ctx.author.mention}!')

@bot.command(name='help')
async def help_command(ctx):
    """Show help menu"""
    embed = discord.Embed(
        title="🤖 Bot Commands",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!hello", value="Get a greeting", inline=False)
    embed.add_field(name="!help", value="Show this menu", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

# ======================
# MAIN EXECUTION
# ======================
if __name__ == '__main__':
    print("🚀 Starting Discord bot with Flask server...")
    
    # Start Flask in a daemon thread (will close when main thread closes)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask server started on port 8080")
    
    # Start Discord bot
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Invalid Discord token! Check your environment variables.")
    except Exception as e:
        print(f"❌ Error: {e}")