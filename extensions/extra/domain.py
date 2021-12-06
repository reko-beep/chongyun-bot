from nextcord.embeds import Embed
from nextcord.ext import commands,tasks
from core.paimon import Paimon
from base.domains import Domains
from extensions.views.information import InformationDropDown, NavigatableView

class GenshinDomains(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.pmon = pmon

        self.domains_handler = Domains(self.pmon)
        self.name = 'Genshin Domains'
        self.description = 'Provides schedule for domains!'
        self.domain_update.start()

    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild is not None:   
            self.domains_handler.load_domain_channel()

    @tasks.loop(hours=24)
    async def domain_update(self):
        await self.domains_handler.update_event()

    @commands.command(aliases=['dsc','domainchannel'],description='Sets domain channel for domain schedule messages!')
    async def setdomainchannel(self, ctx):
        check = self.domains_handler.set_domain_channel(ctx,ctx.channel)

        if check == True:
            embed = Embed(title='Domain channel set', description=f"Domain rotation schedule will be posted to <#{self.pmon.p_bot_config['domain_channel']}>",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error', description=f"You dont have enough privilege!",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['ds'],description='Shows the domain channel set!')
    async def domainstatus(self, ctx):
        check = self.domains_handler.domain_channel

        if check is not None:
            embed = Embed(title='Domain Status', description=f"Domain rotation schedule will be posted every 24hrs to {check.mention}",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error', description=f"You dont have enough privilege!**or\nDomain channel is not set!",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['dlist'],description='dlist (day)\nShows the domains rotation for a specific day!')
    async def domainlist(self, ctx, day: str = ''):
        check = await self.domains_handler.embeds_list(day)

        if bool(check):
            view = NavigatableView(ctx.author)
            view.add_item(InformationDropDown(check, ctx.author))
            await ctx.send('Domains schedule',view=view)
        else:
            embed = Embed(title='Sowwyy!', description=f"Sorry could not find enything!",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(aliases=['du'],description='du (day)\nUpdates domain rotation according to day!')
    async def domainupdate(self, ctx, day: str):
        check = await self.domains_handler.update_event(day)

        if check is not None:
            embed = Embed(title='Domain rotations updated!', description=f"Success! Hurr-rrr-rr-ay",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Failed to update!', description=f"Sow-w-wwy I guess!",color=0xf5e0d0)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


def setup(pmon):
    pmon.add_cog(GenshinDomains(pmon))


def teardown(pmon):
    pmon.remove_cog("GenshinDomains")
