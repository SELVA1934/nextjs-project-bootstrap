import discord
import random
import asyncio
from discord.ext import commands
import os

TOKEN_FILE = "token.txt"
SOUNDS_DIR = "sounds"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")
    else:
        await ctx.send("I am not connected to any voice channel.")

@bot.command()
async def play_random(ctx):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return
    voice_client = ctx.voice_client
    sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith(('.mp3', '.wav', '.ogg'))]
    if not sounds:
        await ctx.send("No sound files found in sounds directory.")
        return
    sound_file = random.choice(sounds)
    source = discord.FFmpegPCMAudio(os.path.join(SOUNDS_DIR, sound_file))
    voice_client.play(source)
    await ctx.send(f"Playing sound: {sound_file}")

if __name__ == "__main__":
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()
    bot.run(token)
