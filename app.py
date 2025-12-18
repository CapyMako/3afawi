import discord
from discord.ext import commands
import os
import http.server
import socketserver
import threading

# ========== SIMPLE HTTP SERVER ==========
class HealthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is alive!')
    
    def log_message(self, format, *args):
        pass  # Suppress logs

def run_http_server():
    with socketserver.TCPServer(("", 8080), HealthHandler) as httpd:
        print(f"🌐 HTTP server running on port 8080")
        httpd.serve_forever()

# ========== DISCORD BOT ==========
# Your actual bot code
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot ready: {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# ========== START EVERYTHING ==========
if __name__ == '__main__':
    # Start HTTP server in background thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Start Discord bot
    bot.run(os.getenv('DISCORD_TOKEN'))