import os
import sys
import logging
from dotenv import load_dotenv

# Set up logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check for token
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    logger.error("❌ DISCORD_TOKEN not found in environment variables!")
    logger.info("Make sure you've set it in Render dashboard → Environment")
    sys.exit(1)

try:
    import discord
    from discord.ext import commands
    logger.info("✅ Successfully imported discord.py")
except ImportError as e:
    logger.error(f"❌ Failed to import discord.py: {e}")
    logger.info("Try using py-cord instead: pip install py-cord")
    sys.exit(1)

# Set up bot with minimal intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None  # We'll add custom help
)

@bot.event
async def on_ready():
    logger.info(f'✅ Logged in as {bot.user.name}')
    logger.info(f'📊 Connected to {len(bot.guilds)} servers')
    
    # Simple status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help"
        )
    )

# Basic commands
@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

@bot.command(name='help')
async def help_command(ctx):
    """Show available commands"""
    embed = discord.Embed(
        title="🤖 Bot Help",
        description="Available commands:",
        color=discord.Color.blue()
    )
    
    commands_list = [
        ("!ping", "Check bot latency"),
        ("!hello", "Get a greeting"),
        ("!info", "Bot information"),
        ("!server", "Server information")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='hello')
async def hello(ctx):
    """Say hello"""
    await ctx.send(f'👋 Hello {ctx.author.mention}!')

@bot.command(name='info')
async def info(ctx):
    """Bot information"""
    embed = discord.Embed(
        title="Bot Info",
        description="A simple Discord bot",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Python", value=sys.version.split()[0], inline=True)
    embed.add_field(name="Library", value="discord.py", inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("❌ An error occurred. Please try again.")

# Health check endpoint for Render
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord Bot is running!", 200

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    """Run Flask in background for health checks"""
    import threading
    import waitress
    
    def run():
        waitress.serve(app, host="0.0.0.0", port=8080)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    logger.info("✅ Flask health check server started on port 8080")

# Start everything
if __name__ == "__main__":
    logger.info("🚀 Starting Discord bot...")
    
    # Start Flask for health checks (Render needs this)
    run_flask()
    
    # Start Discord bot
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        logger.error("❌ Invalid Discord token!")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")