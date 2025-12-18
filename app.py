import os
import threading
from flask import Flask, jsonify
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "alive", "bot": "online"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Your Discord bot code starts here
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready: {bot.user}')

# Run Flask in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Start Flask when you run the script
if __name__ == '__main__':
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Discord bot
    bot.run(TOKEN)