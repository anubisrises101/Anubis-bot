import discord
import random
from discord.ext import commands
from datetime import datetime


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('BOT IS ONLINE')
    await bot.load_extension("Cogs")


def is_me(ctx):
    return ctx.author.id == 350624641028456459


@bot.command()
async def ping(context):
    await context.send("Pong!")


@bot.command()
async def coinflip(ctx):
    num = random.randint(1, 2)

    if num == 1:
        await ctx.send("Heads!")
    if num == 2:
        await ctx.send("Tails!")


@bot.command()
async def rps(ctx, hand):
    hands = ["✊", "✋", "✌️"]
    bot_hand = random.choice(hand)

    if hand == bot_hand:
        await ctx.send("It's a tie!")
    elif hand == "✊" and bot_hand == "✋":
        await ctx.send("I win! I chose ✋.")
    elif hand == "✊" and bot_hand == "✌️":
        await ctx.send("You win! I chose ✌️.")
    elif hand == "✋" and bot_hand == "✊":
        await ctx.send("You win! I chose ✊.")
    elif hand == "✋" and bot_hand == "✌️":
        await ctx.send("I win! I chose ✌️.")
    elif hand == "✌️" and bot_hand == "✊":
        await ctx.send("I win! I chose ✊.")
    elif hand == "✌️" and bot_hand == "✋":
        await ctx.send("You win! I chose ✋.")
    else:
        await ctx.send("Invalid input. Please choose ✊, ✋, or ✌️.")


@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Commands", description="List of commands for the bot", color=0x00FF00
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/129871749221004093/5f4d2b1e6e5a8b1d4c1f6b2a4b3c8c3d.png"
    )
    embed.add_field(name="!ping", value="Returns Pong!", inline=False)
    embed.add_field(name="!coinflip", value="Flips a coin", inline=False)
    embed.add_field(
        name="!rps",
        value="Play rock, paper, scissors with the bot by using ✊, ✋, or ✌️",
        inline=False,
    )
    await ctx.send(embed=embed)


@bot.group()
@commands.has_role("Admin")
async def edit(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid edit command passed...")


@edit.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@edit.command()
@commands.has_role("Admin")
async def servername(ctx, *, input):
    await ctx.guild.edit(name=input)
    await ctx.send("Server name changed.")


@servername.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@edit.command()
@commands.has_role("Admin")
async def rtc_region(ctx, *, input):
    await ctx.guild.edit(name=input)
    await ctx.send("Region changed.")


@rtc_region.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@edit.command()
@commands.has_role("Admin")
async def createtextchannel(ctx, *, input):
    await ctx.guild.create_text_channel(name=input)
    await ctx.send("Text channel created.")


@createtextchannel.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@edit.command()
@commands.has_role("Admin")
async def createvoicechannel(ctx, *, input):
    await ctx.guild.create_voice_channel(name=input)
    await ctx.send("Voice channel created.")


@createvoicechannel.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@edit.command()
@commands.has_role("Admin")
async def createrole(ctx, *, input):
    await ctx.guild.create_role(name=input)
    await ctx.send("Role created.")


@createrole.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.kick(member, reason=reason)


@kick.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.ban(member, reason=reason)


@ban.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def unban(ctx, *, input):
    name = input
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        if name == username:
            await ctx.guild.unban(bannedmember.user)
            await ctx.send(f"Unbanned {bannedmember.user.mention}")
            return


@unban.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def purge(
    ctx, amount, day: int = None, month: int = None, year: int = datetime.now().year
):
    if amount == "/":
        if day == None or month == None:
            await ctx.send("Please enter a day and month.")
            return
        else:
            await ctx.channel.purge(after=datetime(year, month, day))
    else:
        await ctx.channel.purge(limit=int(amount) + 1)
    await ctx.send(f"Purged {amount} messages.")


@purge.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter the amount of messages to delete.")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Please enter a valid amount of messages to delete.")


@bot.command()
@commands.has_role("Admin")
async def mute(ctx, user: discord.Member):
    await user.edit(mute=True)
    await ctx.send(f"{user.mention} has been muted.")


@mute.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def unmute(ctx, user: discord.Member):
    await user.edit(mute=False)
    await ctx.send(f"{user.mention} has been muted.")


@unmute.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def deafen(ctx, user: discord.Member):
    await user.edit(deafen=True)
    await ctx.send(f"{user.mention} has been muted.")


@deafen.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def undeafen(ctx, user: discord.Member):
    await user.edit(deafen=False)
    await ctx.send(f"{user.mention} has been muted.")


@undeafen.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_role("Admin")
async def voicekick(ctx, user: discord.Member):
    await user.edit(voice_channel=None)
    await ctx.send(f"{user.mention} has been kicked from the voice channel.")


@voicekick.error
async def errorhandles(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

@bot.command()
@commands.has_role("Admin")
async def unload(ctx, extension):
    bot.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} has been unloaded.")

@bot.command()
@commands.has_role("Admin")
async def reload(ctx, extension):
    bot.reload_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} has been reloaded.")










bot.run("MTI5ODcxNzQ5MjIxMDA0MDkzMw.G2j88a.iISWIBWgxP0x2gVSZtutYGuIHwfixwKb5grNuU")
