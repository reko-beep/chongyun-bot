from nextcord.ext import commands
from nextcord import Embed, File,Member
from nextcord.ui import View
from nextcord.utils import get

from base.bump import Bump

from core.paimon import Paimon
from util.logging import logc

class Bumper(commands.Cog):
    def __init__(self, pmon : Paimon):
        '''
        initializes bump cog
        '''
        self.pmon = pmon
        self.bump_handler = Bump(pmon)

    @commands.Cog.listener()
    async def on_message(self,message):
        '''
        look for bump message if successful sets a reminder to set message
        '''
        await self.bump_handler.parse_message_for_bump(message)
    
    @commands.command()
    async def bumps(self, ctx, user: Member = None):
        if user == None:
            user = ctx.author

        bumps = self.bump_handler.get_bump_counter(str(user.id))

        if bumps:
            embed = Embed(title='Bumps', 
                        description=f'bumped this server {bumps} times!',
                        color=0xf5e0d0) 
            embed.set_author(name=user.display_name,
                                icon_url=user.avatar.url)
            await ctx.send(embed=embed)

        else:
            embed = Embed(title='Bumps', 
                        description=f'have never bumped this server!',
                        color=0xf5e0d0) 

            embed.set_author(name=user.display_name,
                                icon_url=user.avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['btop','bt'])
    async def bumptop(self,ctx):

        top_bumper = self.bump_handler.get_topbumper()
        bumps = self.bump_handler.get_bump_counter(str(top_bumper))
        logc(f'Top Bumper userid: {top_bumper}', f'Count {bumps}')

        user = get(ctx.guild.members,id=int(top_bumper))
        logc(f'Use fetched: {user}')

        if top_bumper != None:
            if user != None:
                embed = Embed(title='Top Bumper',
                        description=f'**{user}** have bumped this server most time\n around {bumps} times!',
                        color=0xf5e0d0) 
                embed.set_author(name=user.display_name,
                                icon_url=user.avatar.url)

                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Error', 
                            description=f'Could not find any top bumper',
                            color=0xf5e0d0) 

                embed.set_author(name=user.display_name,icon_url=user.avatar.url)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Error', 
                            description=f'Could not find any top bumper',
                            color=0xf5e0d0) 

            embed.set_author(name=user.display_name,icon_url=user.avatar.url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Bumper(bot))


def teardown(bot):
    bot.remove_cog("Bumper")