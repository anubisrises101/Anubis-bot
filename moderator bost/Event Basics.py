import discord
import random
from discord.ext import commands
intents = discord.Intents.all()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print('BOT IS ONLINE')
    
@bot.event
async def on_message(message): 
    username = message.author.display_name
    if message.author == bot.user:
        return
    else:
        if message.content == "hello":
            await message.channel.send("Hello " + username + "!") 

@bot.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}!")
    
@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    
    if emoji == "⛰️" and message_id == 1298727575111208990:
        role = discord.utils.get(guild.roles, name="THE CAVE")
        await member.add_roles(role)
        
    if emoji == "💕" and message_id == 1298727575111208990:
        role = discord.utils.get(guild.roles, name="Cave Allies")
        await member.add_roles(role)
    
@bot.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name
    user_id = payload.user_id
    member = guild.get_member(payload.user_id)
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    
    if emoji == "⛰️" and message_id == 1298727575111208990:
        role = discord.utils.get(guild.roles, name="THE CAVE")
        await member.remove_roles(role)
        
    if emoji == "💕" and message_id == 1298727575111208990:
        role = discord.utils.get(guild.roles, name="Cave Allies")
        await member.remove_roles(role)
    


  
bot.run('MTI5ODcxNzQ5MjIxMDA0MDkzMw.G2j88a.iISWIBWgxP0x2gVSZtutYGuIHwfixwKb5grNuU')

