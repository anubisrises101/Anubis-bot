import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!")

class Battleships(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.board1 = ''
        self.board2 = ''
        self.boardtoshow1 = ''
        self.boardtoshow2 = ''


    async def render(self, ctx, board):
        
        numbers = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:'] 
        
        alphabets = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:', ':regional_indicator_g:', ':regional_indicator_h:', ':regional_indicator_i:', ':regional_indicator_j:']

        stringboard = ''

        stringboard = stringboard + ':black_mediuam_small_square:'
        for x in range(len(board[0])):
            stringboard = stringboard + alphabets[x]
        stringboard = stringboard + '\n'
            
        i = 0
        for row in board:
            stringbboard = stringboard + numbers[i]
            i = i + 1
        for square in row:
            stringboard = stringboard + square
        stringboard = stringboard + '\n'
        
        await ctx.send(stringboard)
        
        
@bot.command()
async def battleships(self, ctx, player2 : discord.Member, ver : int = 5, hor : int = 5):

    if self.playing == False:
        self.playing = True
    

    
    
# [[':blue_square:', ':blue_sqaure:', ':blue_square:', ':blue_square:', ':blue_square:'],
#  [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'],
#  [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'],
#  [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'],
#  [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:']]

















bot.run("MTI5ODcxNzQ5MjIxMDA0MDkzMw.G2j88a.iISWIBWgxP0x2gVSZtutYGuIHwfixwKb5grNuU")



