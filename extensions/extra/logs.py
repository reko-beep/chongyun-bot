
from nextcord.ext import commands
from nextcord import Embed, File
from nextcord.ui import View

from base.logs import Logs
from extensions.views.guides import NavigatableView
from extensions.views.logs import ExtInformationDropDown

from core.paimon import Paimon


class GenshinLogs(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.logs_handler = Logs(pmon)
        self.name = 'Genshin Logs'
        self.description = 'Fetches and shows the transaction logs of you Genshin Impact Account!'


    @commands.command(aliases=['glogs'], description=f'glogs (feedback link)\nFetches all logs of your account from feedback link!')
    async def genshinlogs(self, ctx, authkey: str=''):
        if authkey != '':
            if authkey.startswith('https://webstatic-sea.mihoyo.com/'):
                
                msg = await ctx.send('Huff... Huff.. working!')
                await self.logs_handler.fetch_alllogs(authkey, msg)

            else:

                embed = Embed(title='Genshin Logs Error!',description=f'Please mention a valid feedback link!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed) 

        else:
    
            embed = Embed(title='Genshin Logs Error!',description=f'Please mention a feedback link!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed) 

    @commands.command(aliases=['gprimogems'], description=f'gprimogems (uid)\nShows primogems transactions of your genshin account!')
    async def genshinprimogems(self, ctx, uid: str=''):
        if uid != '':

            embeds = self.logs_handler.create_primogem_embed(ctx, uid)

            if bool(embeds):
                view = NavigatableView(ctx.author)
                view.add_item(ExtInformationDropDown(embeds, ctx.author))
                await ctx.send('Please select a page from below',view=view) 

            else:

                embed = Embed(title='Genshin Logs Error!',description=f'Could not find any logs\n Please make a fetch of logs before!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed) 

        else:
    
            embed = Embed(title='Genshin Logs Error!',description=f'Please mention the uid!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed) 

    @commands.command(aliases=['gartifacts'], description=f'gartifacts (uid)\nShows artifacts transactions of your genshin account!')
    async def genshinartifacts(self, ctx, uid: str=''):
        if uid != '':

            embeds = self.logs_handler.create_artifact_embed(ctx, uid)

            if bool(embeds):
                view = NavigatableView(ctx.author)
                view.add_item(ExtInformationDropDown(embeds, ctx.author))
                await ctx.send('Please select a page from below',view=view) 

            else:

                embed = Embed(title='Genshin Logs Error!',description=f'Could not find any logs\n Please make a fetch of logs before!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed) 

        else:
    
            embed = Embed(title='Genshin Logs Error!',description=f'Please mention the uid!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed) 
    
    @commands.command(aliases=['gcrystals'], description=f'gcrystals (uid)\nShows crystals transactions of your genshin account!')
    async def genshincrystals(self, ctx, uid: str=''):
        if uid != '':

            embeds = self.logs_handler.create_crystal_embed(ctx, uid)

            if bool(embeds):
                view = NavigatableView(ctx.author)
                view.add_item(ExtInformationDropDown(embeds, ctx.author))
                await ctx.send('Please select a page from below',view=view) 

            else:

                embed = Embed(title='Genshin Logs Error!',description=f'Could not find any logs\n Please make a fetch of logs before!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed) 

        else:
    
            embed = Embed(title='Genshin Logs Error!',description=f'Please mention the uid!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed) 
    
    @commands.command(aliases=['gresins'], description=f'gresins (uid)\nShows resings transactions of your genshin account!')
    async def genshinresins(self, ctx, uid: str=''):
        if uid != '':

            embeds = self.logs_handler.create_resin_embed(ctx, uid)

            if bool(embeds):
                view = NavigatableView(ctx.author)
                view.add_item(ExtInformationDropDown(embeds, ctx.author))
                await ctx.send('Please select a page from below',view=view) 

            else:

                embed = Embed(title='Genshin Logs Error!',description=f'Could not find any logs\n Please make a fetch of logs before!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed) 

        else:
    
            embed = Embed(title='Genshin Logs Error!',description=f'Please mention the uid!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed) 

def setup(pmon):
    pmon.add_cog(GenshinLogs(pmon))


def teardown(pmon):
    pmon.remove_cog("GenshinLogs")
