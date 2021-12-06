
from nextcord.ext import commands
from nextcord import Embed, File
from nextcord.ui import View

from base.guides import GenshinGuides
from extensions.views.information import AllList,NavigatableView

from core.paimon import Paimon


class Information(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.name = 'Information'
        self.description = 'Provides general information and ascension materials required for basic genshin weapons and artifacts and characters!'


    @commands.command(aliases=['inf'],description='Opens a interaction to get information about Genshin Impact weapons, and artifacts and characters')
    async def information(self,ctx):        
        view_object = NavigatableView(ctx.author)
        view_object.add_item(AllList(self.pmon,'',ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)


def setup(bot):
    bot.add_cog(Information(bot))


def teardown(bot):
    bot.remove_cog("Information")