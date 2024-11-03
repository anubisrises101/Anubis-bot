from discord.ext import commands, tasks
from datetime import datetime

async def setup(bot):
    await bot.add_cog(MyCog(bot))

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            if message.content == "hello":
                await message.channel.send("Hello " + message.author.display_name + "!")

    @commands.command()
    async def black(self, ctx):
        await ctx.send("White!")
        
    @tasks.loop(seconds=1)
    async def alarm(self, ctx, hour, minute):
        now = datetime.now().time()
        if now.hour == hour and now.minute == minute:
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("ALARM!")
            self.alarm.stop()
            
    @commands.command()
    async def startalarm(self, ctx, date):
        hour, minute = date.split(":")
        hour = int(hour)
        minute = int(minute)
        self.alarm.start(ctx, hour, minute)
    
    