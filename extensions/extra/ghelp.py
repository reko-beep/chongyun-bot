import json
import os
import asyncio
from nextcord.ext import commands
from nextcord import Embed
from nextcord.message import Message
from nextcord.reaction import Reaction

from core.paimon import Paimon
from extensions.views.help import HelpList, NavigatableView


class GenshinHelp(commands.Cog):
    def __init__(self, pmon):
        self.pmon: Paimon = pmon


        self.name = 'Help commands'
        self.description = 'Help module'


    @commands.command(aliases=['help', 'h'])
    async def ghelp(self, ctx):
        view = NavigatableView(ctx.author)
        view.add_item(HelpList(self.pmon,ctx.author))
        await ctx.send('Select a module from below!',view=view)
      


def setup(bot):
    bot.add_cog(GenshinHelp(bot))


def teardown(bot):
    bot.remove_cog("GenshinHelp")
