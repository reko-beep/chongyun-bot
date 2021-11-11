import json
import os
import asyncio
from nextcord.ext import commands
from nextcord import Embed
from nextcord.message import Message
from nextcord.reaction import Reaction

from core.paimon import Paimon


class GenshinHelp(commands.Cog):
    def __init__(self, pmon):
        self.pmon: Paimon = pmon


        # load embed data.
        embed_data = 'assets/GenshinHelp/embed_data.json'
        if os.path.exists(embed_data):
            with open(embed_data,'r') as f:
                embed_data = json.load(f)

            # preload all embeds.
            self.embeds = []
            for i in embed_data:
                embed = Embed.from_dict(embed_data[i])
                self.embeds.append(embed)



    @commands.command(aliases=['help', 'h'])
    async def ghelp(self, ctx):

        embed_select = 0
        count = len(self.embeds)
        msg: Message = await ctx.send(embed=self.embeds[0])
        
        # add nav butons
        for i in ['⬅️','➡️']:
            await msg.add_reaction(i)

        while True:
            try:
                reaction: Reaction = None
                reaction, _ = await self.pmon.wait_for(
                    'reaction_add',
                    timeout=6,
                    check=(lambda reaction, user:
                           reaction.message.id == msg.id and user == ctx.author))

                await msg.remove_reaction(reaction, ctx.author)
                
            except asyncio.exceptions.TimeoutError:
                await msg.clear_reactions()
                return
            else:                                 
                if reaction.emoji == '➡️':
                    if embed_select < count-1:
                        embed_select += 1
                        await msg.edit(embed=self.embeds[embed_select])                           
                if reaction.emoji == '⬅️':
                    if embed_select >= 1:
                        embed_select -= 1
                        await msg.edit(embed=self.embeds[embed_select])


def setup(bot):
    bot.add_cog(GenshinHelp(bot))


def teardown(bot):
    bot.remove_cog("GenshinHelp")
