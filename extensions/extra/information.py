
from nextcord.ext import commands, tasks
from nextcord import Embed, File, Role
from nextcord.ui import View

from base.information import GenshinInformation
from extensions.views.base import EmbedView
from extensions.views.information import AllList, InformationDropDown,NavigatableView
from extensions.views.teampcomps import TeampComps
from util.logging import logc
from core.paimon import Paimon
from base.fishing import Fishing


fisher = Fishing()

class Information(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.inf_handler = GenshinInformation(pmon)
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

    @commands.command(aliases=['tc','tcomp'],description='tc (character name), searches a team comp for a character')
    async def teamcomp(self,ctx, *arg: str):
        search = ''.join(arg)   

        if search != '':  
            lists_ = self.inf_handler.search_comps(search)

            if lists_ is not None:
                if len(lists_) != 0:
                    
                    view = NavigatableView(ctx.author)
                    view.add_item(TeampComps(self.pmon, self.inf_handler, lists_, ctx.author,1))

                    await ctx.send(f'Team comps for {search}', view=view)

                else:

                    embed = Embed(title='Information Error', description='could not find a team comp for character!',color=0xf5e0d0) 
                    embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')

                    await ctx.send(embed=embed)

            else:
            

                embed = Embed(title='Information Error', description='could not find a team comp for character!',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')

                await ctx.send(embed=embed)



        else:
    
            embed = Embed(title='Information Error', description='Please write the character name',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['ctc','ctcomp'],description='tc (comp name) (comp chars) (compnotes | optional), searches a team comp for a character')
    async def createteamcomp(self,ctx, comp_name:str, comp_chars:str, comp_notes:str=''):
        role = self.inf_handler.get_comprole()
        if role is not None:
            check = (len(set([role.id]).intersection([r.id for r in ctx.author.roles])) != 0)

            if check:
                if comp_name != '':

                    if comp_chars != '':

                        check,comp = self.inf_handler.create_comp(comp_name, comp_chars, comp_notes, ctx.author)

                        if check is None:

                            embed = Embed(title='Wrong Character format', description="Please write the characters in this format\n 'xingqiu:sub dps, bennett:main dps'\n**NOTE:** write the correct character name else they wont appear in Team Comp image.",color=0xf5e0d0) 
                            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                            await ctx.send(embed=embed)
                        
                        if check is True:

                            embed,file = self.inf_handler.create_embed_comp(comp)
                            await ctx.send(embed=embed, file=file)
                    
                    else:

                        embed = Embed(title='Information Error', description="Please write the characters in this format\n 'xingqiu:sub dps, bennett:main dps'\n**NOTE:** write the correct character name else they wont appear in Team Comp image.",color=0xf5e0d0) 
                        embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                        await ctx.send(embed=embed)

                else:  
            
                    embed = Embed(title='Information Error', description='Please write the comp name',color=0xf5e0d0) 
                    embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                    await ctx.send(embed=embed)
            else:
                embed = Embed(title='Team Comp Error', description=f'You dont have {role.mention}\nAsk a mod to give you the role if you want to contribute!',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Team Comp Error', description=f'Ask mod to set the comp role!',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)



    @commands.command(aliases=['tcr','tcompr'],description='tc (role)')
    async def teamcomprole(self,ctx, role: Role):

        check = (len(set(self.pmon.p_bot_config['mod_role']).intersection([r.id for r in ctx.author.roles])) != 0)

        if check:

        
            check = self.inf_handler.set_comprole(role)

            if check is True:

                embed = Embed(title='Team Comp role changed!', description=f'**Comp contributor role** set to {role.mention}',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)

            
            
        else:  

    
            embed = Embed(title='Information Error', description='You dont have enough privilege to set role!',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['tcrs','tcomprs'],description='tcrs')
    async def teamcomprolestatus(self,ctx):
   
        
        check = self.inf_handler.get_comprole()

        if check is not None:
            embed = Embed(title='Team Comp Contribution role!', description=f'**Comp contributor role set to {check.mention}',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        
        else:
            embed = Embed(title='Team Comp Contribution role!', description='The role is not set!',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)






    @commands.command(aliases=['inf'],description='Opens a interaction to get information about Genshin Impact weapons, and artifacts and characters')
    async def information(self,ctx, option: str=''):        
        view_object = NavigatableView(ctx.author)
        view_object.add_item(AllList(self.pmon,self.inf_handler,option,ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)

    @commands.command(aliases=['dgp'],description='Shows daily genshin posts')
    async def dailygenshinpost(self,ctx, char:str=None):        
        embeds = self.inf_handler.embeds_daily_posts(char)
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

            character, bday, img = self.inf_handler.get_bday(m_num, day)

            embed = Embed(title=f'Your birthday is close to {character}', description=f'Birthday date: {bday}',color=0xf5e0d0) 
            embed.set_thumbnail(url=img)
            await ctx.send(embed=embed)
            
        


def setup(bot):
    bot.add_cog(Information(bot))


def teardown(bot):
    bot.remove_cog("Information")