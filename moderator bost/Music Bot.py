import asyncio
import discord, yt_dlp, os
import random
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
queuelist = []
filestodelete = []

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, searchword):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    voice = ctx.voice_client

    if searchword[0:4] == "http" or searchword[0:3] == "www":
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(searchword, download=False)
            title = info["title"]
            url = searchword

    if searchword[0:4] != "http" and searchword[0:3] != "www":
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{searchword}", download=False)["entries"][0]
            title = info["title"]
            url = info["webpage_url"]

    download_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{title}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(download_opts) as ydl:
        ydl.download([url])
        
    if voice.is_playing():
        queuelist.append(title)
        await ctx.send(f"Added **{title}** to the queue")
        filestodelete.append(title)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))
    else:
        voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after=lambda e: check_queue(ctx))
        await ctx.send(f"Playing **{title}**")  
        filestodelete.append(title)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))

    
def check_queue(ctx):
    voice = ctx.voice_client
    try:
        if queuelist:
            next_title = queuelist.pop(0)
            voice.play(discord.FFmpegPCMAudio(f"{next_title}.mp3"), after=lambda e: check_queue(ctx))
            coro = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next_title))
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            fut.result()
            filestodelete.append(next_title)
    except IndexError:
        pass
    finally:
        for file in filestodelete:
            os.remove(f"{file}.mp3")
        filestodelete.clear()
                
        
@bot.command()
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Nothing is playing")
        
@bot.command()
async def resume(ctx):
    voice = ctx.voice_client
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resumed")
    else:
        await ctx.send("Nothing is paused")
        
        
@bot.command(aliases=["s", "skip"])
async def stop(ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        voice.stop()
        await ctx.send("Stopped")
    else:
        await ctx.send("Nothing is playing")
        
@bot.command()
async def queuelist(ctx):
    if queuelist:
        await ctx.send(f'Queue: ** {str(queuelist)} ** ')        
        
bot.run("MTI5ODcxNzQ5MjIxMDA0MDkzMw.G2j88a.iISWIBWgxP0x2gVSZtutYGuIHwfixwKb5grNuU")
