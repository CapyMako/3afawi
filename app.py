import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from .env
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if token exists
if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
    print("Make sure your .env file contains: DISCORD_TOKEN=your_token_here")
    exit(1)

# Set up bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # If you want to access member info

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'🎯 Connected to {len(bot.guilds)} guilds')
    print('------')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help"
        )
    )

# Command: !ping
@bot.command(name='ping', help='Check if the bot is alive')
async def ping(ctx):
    # Calculate latency
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    
    # Create embed for nicer response
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: **{latency}ms**",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)

# Command: !hello
@bot.command(name='hello', help='Say hello to the bot')
async def hello(ctx):
    # Mention the user who invoked the command
    await ctx.send(f'👋 Hello {ctx.author.mention}! How can I help you today?')

# Command: !info
@bot.command(name='info', help='Get bot information')
async def info(ctx):
    embed = discord.Embed(
        title="🤖 Bot Information",
        description="A simple Discord bot created with discord.py",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Creator", value="Your Name", inline=True)
    embed.add_field(name="Library", value="discord.py", inline=True)
    embed.add_field(name="Prefix", value="!", inline=True)
    embed.add_field(name="Server Count", value=len(bot.guilds), inline=True)
    embed.add_field(name="User Count", value=len(bot.users), inline=True)
    embed.add_field(name="Uptime", value="Online", inline=True)
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    
    await ctx.send(embed=embed)

# Command: !echo
@bot.command(name='echo', help='Repeat your message')
async def echo(ctx, *, message: str):
    await ctx.send(f"📢 {ctx.author.name} says: {message}")

# Command: !serverinfo
@bot.command(name='serverinfo', help='Get server information')
async def serverinfo(ctx):
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name} Info",
        color=discord.Color.purple()
    )
    
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
    
    await ctx.send(embed=embed)

# Error handler for missing permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument. Use `!help {ctx.command}` for usage.")
    else:
        print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    print("🚀 Starting bot...")
    print(f"📁 Token loaded: {'Yes' if TOKEN else 'No'}")
    
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ ERROR: Invalid token! Check your .env file.")
    except Exception as e:
        print(f"❌ ERROR: {e}")