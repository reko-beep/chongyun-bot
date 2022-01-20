
from nextcord.ext import commands, tasks
from nextcord import Embed, File
from nextcord.ui import View

from base.information import GenshinInformation
from extensions.views.base import EmbedView
from extensions.views.information import AllList, InformationDropDown,NavigatableView
from util.logging import logc
from core.paimon import Paimon
from base.fishing import Fishing

inf_handler = GenshinInformation()
fisher = Fishing()

class Information(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.name = 'Information'
        self.description = 'Provides general information and ascension materials required for basic genshin weapons and artifacts and characters!'


    @commands.command(aliases=['fp'],description='fp (fishname), searches location for a fish')
    async def fishingpoint(self,ctx, *arg: str):
        search = ''.join(arg)   

        if search != '':  
            lists_ = fisher.create_embeds(search)

            if len(lists_) != 0:
                check_dict = (type(lists_[0]) == dict)
                
                view = EmbedView(self.pmon, ctx, lists_, 0)

                if check_dict:
                    message = await ctx.send(embed=lists_[0]['embed'], file=lists_[0]['file'], view=view)
                
                else:
                    await ctx.send(embed=lists_[0], view=view)

            else:

                embed = Embed(title='Information Error', description='could not search for fish!',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')

                await ctx.send(embed=embed)

        else:
    
            embed = Embed(title='Information Error', description='Please write the fish name',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)




    @commands.command(aliases=['inf'],description='Opens a interaction to get information about Genshin Impact weapons, and artifacts and characters')
    async def information(self,ctx):        
        view_object = NavigatableView(ctx.author)
        view_object.add_item(AllList(self.pmon,'',ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)

    @commands.command(aliases=['dgp'],description='Shows daily genshin posts')
    async def dailygenshinpost(self,ctx, char:str=None):        
        embeds = inf_handler.embeds_daily_posts(char)
        view_object = NavigatableView(ctx.author)
        view_object.add_item(InformationDropDown(embeds, ctx.author))
        await ctx.send('Please select a post from below?',view=view_object)
    
    @commands.command(aliases=['gbday'], description='gbday (month) (day)')
    async def genshin_birthday(self, ctx, month: str, day:str):

        if not day.isdigit():
            embed = Embed(title='Information Error', description='Please correct date!',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
        
        else:

            day = int(day)
            
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            m_num = 0
            for c,m in enumerate(months,1):
                if month.lower() in m:
                    m_num = c                   

            character, bday, img = inf_handler.get_bday(m_num, day)

            embed = Embed(title=f'Your birthday is close to {character}', description=f'Birthday date: {bday}',color=0xf5e0d0) 
            embed.set_thumbnail(url=img)
            await ctx.send(embed=embed)
            
        


def setup(bot):
    bot.add_cog(Information(bot))


def teardown(bot):
    bot.remove_cog("Information")