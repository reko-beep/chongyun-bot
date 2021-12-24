
from nextcord.ext import commands, tasks
from nextcord import Embed, File
from nextcord.ui import View

from base.information import GenshinInformation
from extensions.views.information import AllList, InformationDropDown,NavigatableView
from util.logging import logc
from core.paimon import Paimon

inf_handler = GenshinInformation()
class Information(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.name = 'Information'
        self.description = 'Provides general information and ascension materials required for basic genshin weapons and artifacts and characters!'
        self.dgp_posts.start()


    @tasks.loop(hours=24)
    async def dgp_posts(self):
        inf_handler.save_daily_posts()
        logc('Daily genshin posts updated!')



    @commands.command(aliases=['inf'],description='Opens a interaction to get information about Genshin Impact weapons, and artifacts and characters')
    async def information(self,ctx):        
        view_object = NavigatableView(ctx.author)
        view_object.add_item(AllList(self.pmon,'',ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)

    @commands.command(aliases=['dgp'],description='Shows daily genshin posts')
    async def dailygenshinpost(self,ctx):        
        embeds = inf_handler.embeds_daily_posts()
        view_object = NavigatableView(ctx.author)
        view_object.add_item(InformationDropDown(embeds, ctx.author))
        await ctx.send('Please select a post from below?',view=view_object)

def setup(bot):
    bot.add_cog(Information(bot))


def teardown(bot):
    bot.remove_cog("Information")