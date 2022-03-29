from nextcord import Embed, Message
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands

from core.bot import DevBot

from base.resource_manager import ResourceManager
from base.information import Information
from base.paginator import PaginatorList

class InformationCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf

    @commands.command(aliases=['char','character'], description='char (character name)\nshows the full info from database for a character')
    async def characterinfo(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(char, [],False, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
        await message.edit(embed=embeds[0],view=view)


def setup(bot):
    bot.add_cog(InformationCog(bot))


def teardown(bot):
    bot.remove_cog("InformationCog")
