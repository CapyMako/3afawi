import discord
from discord.ext import commands
import os
import http.server
import socketserver
import threading

# After the insults update
import random
import asyncio
from datetime import datetime, time
import pytz

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

class ScheduledMessages:
    def __init__(self, bot):
        self.bot = bot
        self.messages = [
            "bsah firas nta bnin ahh",
            "baraa ma ta3rafch tel3ab b zenyata",
            "teroumet baraa hadik fel frach tenta9",
            "yakho hadok baraa w firas chhal fayhin, roho dawcho!",
            "ya l fermaja ta3 firas wektach tel9a lmotivation ya lfayeh lkelb",
            "daymen nog3od w netfakar bali baraa horny for furries",
            "baraa baraa baraa baraa baraa baraa baraa baraa  baraa  baraa  baraa  baraa googoogaga shut your mouth ffs",
            "i'm feeling peacefull today bessah ki tfakart bali kayn firas smatetli",
            "howa chofo kayn 3 3afawyin fi had l3alam, baraa, baraa, and baraa",
            "m9wda tkon thab rejlin, mziya manich firas"
        ]
        self.last_message = None
        self.channel_id = None  # Set this to your channel ID
        self.is_running = False
    
    def get_random_message(self):
        """Get random message that's not the same as last one"""
        available = [msg for msg in self.messages if msg != self.last_message]
        if not available:  # If all messages were used, reset
            available = self.messages
        message = random.choice(available)
        self.last_message = message
        return message
    
    def is_within_time_range(self):
        """Check if current time is between 6 PM and 2 AM"""
        # Set your timezone - change to your local timezone
        tz = pytz.timezone('Africa/Algiers')  # Change this!
        now = datetime.now(tz)
        current_time = now.time()
        
        # Time range: 6:00 PM (18:00) to 2:00 AM (02:00)
        start_time = time(18, 0)  # 6 PM
        end_time = time(2, 0)     # 2 AM
        
        if start_time < end_time:
            # Normal range (e.g., 6 PM to 11 PM)
            return start_time <= current_time <= end_time
        else:
            # Overnight range (6 PM to 2 AM crosses midnight)
            return current_time >= start_time or current_time <= end_time
    
    async def send_scheduled_message(self):
        """Send message if within time range"""
        if not self.channel_id:
            print("❌ No channel ID set for scheduled messages!")
            return
            
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print(f"❌ Channel {self.channel_id} not found!")
            return
            
        if self.is_within_time_range():
            try:
                message = self.get_random_message()
                await channel.send(message)
                print(f"✅ Sent scheduled message: {message[:30]}...")
            except Exception as e:
                print(f"❌ Failed to send scheduled message: {e}")
        else:
            # Optional: Log when not in time range
            # print("⏰ Not in scheduled time range (6 PM - 2 AM)")
            pass
    
    async def start_scheduler(self):
        """Start the hourly scheduler"""
        if self.is_running:
            return
            
        self.is_running = True
        print("⏰ Scheduled messages started (6 PM - 2 AM, hourly)")
        
        while True:
            try:
                await self.send_scheduled_message()
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
            
            # Wait 1 hour before next check
            await asyncio.sleep(3600)  # 3600 seconds = 1 hour

@bot.event
async def on_ready():
    print(f'✅ Bot ready: {bot.user}')

    # Create scheduler instance
    bot.scheduler = ScheduledMessages(bot)
    
    # ⚠️ SET YOUR CHANNEL ID HERE! ⚠️
    # Right-click channel in Discord → Copy ID
    bot.scheduler.channel_id = 1445978728378404987
    
    # Start the scheduler in background
    asyncio.create_task(bot.scheduler.start_scheduler())

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='testschedule')
@commands.has_permissions(administrator=True)
async def test_schedule(ctx):
    """Test the scheduled message system"""
    if hasattr(bot, 'scheduler'):
        message = bot.scheduler.get_random_message()
        await ctx.send(f"🎯 Test message: {message}")
    else:
        await ctx.send("❌ Scheduler not initialized!")

@bot.command(name='forcereset')
@commands.has_permissions(administrator=True)
async def force_reset(ctx):
    """Force reset last message memory"""
    if hasattr(bot, 'scheduler'):
        bot.scheduler.last_message = None
        await ctx.send("✅ Last message memory reset!")

# ========== START EVERYTHING ==========
if __name__ == '__main__':
    # Start HTTP server in background thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Start Discord bot
    bot.run(os.getenv('DISCORD_TOKEN'))