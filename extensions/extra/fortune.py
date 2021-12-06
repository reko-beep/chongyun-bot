import random
import nextcord
from nextcord.ext import commands
import asyncio
import json

from nextcord.ext.commands.context import Context
from util.logging import logc

class Fortune(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sticks_held = {}
        
        with open('assets/Fortune/fortune_data.json') as f:
            self.fortune_data = json.load(f)
        
        self.name = 'Fortune'
        self.description = 'Genshin Impact like fortune sticks implemented in discord!'

    
    @commands.command(aliases=['df'],description='Draws a fortune stick!')
    async def drawfortune(self, ctx):
        userid = ctx.author.id
        if self.sticks_held.get(userid):
            await ctx.send('Fortune Stick already claimed')
            return
            
        # draw stick
        await ctx.send(file=nextcord.File("assets/Fortune/draw_stick.gif"))
        await asyncio.sleep(5)
        await ctx.send("obtained Fortune Stick x1")
        self.sticks_held[userid] = 1

    @commands.command(aliases=['of'], description='Opens a fortune stick')
    async def openfortune(self, ctx: Context, *args):

        if not args:
            target_user = ctx.author.id
        else:
            target_user = ctx.message.mentions[0].id

      

        if not self.sticks_held.get(target_user):
            await ctx.send("draw a fortune first!")

        else:
            self.sticks_held[target_user] -= 1
            
            fortunate = random.choice(list(self.fortune_data.keys()))
            fortune = random.choice(self.fortune_data[fortunate])

            if fortunate == "Great Fortune":
                color = 0x008800
            elif fortunate == "Good Fortune":
                color = 0x888800
            else:
                color = 0x000000

            embed = nextcord.Embed(title=fortunate,description=f'*{fortune}*',color=color)
            embed.set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.avatar.url)
       
            embed.set_thumbnail(url='https://i.imgur.com/7m0eiTs.png')
            await ctx.send(embed=embed)


def setup(pmon):
    pmon.add_cog(Fortune(pmon))


def teardown(pmon):
    pmon.remove_cog("Fortune")
