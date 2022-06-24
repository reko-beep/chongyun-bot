
from os import listdir, remove
from os.path import join, isfile, islink, getsize
from pydoc import describe
from warnings import warn
from nextcord import Embed, Message, Member, Guild
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
from nextcord.utils import get
from asyncio import sleep
from core.bot import DevBot
from base.paginator import PaginatorList, SwitchPaginator

import requests

from dev_log import logc

class Owner(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf
        self.coop = self.bot.coop
    

    @commands.command(aliases=['nuke'])
    async def nukeserver(self, ctx, guild_id: Guild=None):
        if ctx.author.id == self.bot.b_config.get('owner_bot'):
            if self.bot.b_config.get('nuke_enabled', False) == True:
                if guild_id is not None:
                    guild = get(self.bot.guilds, id=guild_id.id)
                    embed = Embed(title='Nuking in process', description='Server is doomed')
                    msg = await ctx.send(embed=embed)
                    for member in guild.members:
                        embed = Embed(title='Nuking in process', description=f'{member.display_name}\n**ID:** : {str(member)}\n*kicked*')
                        await msg.edit(embed=embed)
                        
                        if self.bot.get('nuke_members', None) == True:
                            await member.kick()
                else:
                    embed = Embed(title='Nuke error', description='You have not mentioned a guild!')
                    await ctx.send(embed=embed)
                
            else:
                embed = Embed(title='Nuke error', description='Hahaha pranked, \n wait till bot owner changes his mind!')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Nuke error', description='Hahaha pranked, \n You are not the bot owner!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['nuker'])
    async def nukeowner(self, ctx):
        if ctx.author.id == self.bot.b_config.get('owner_bot'):
            self.bot.b_config['nuke_enabled'] = not self.bot.b_config.get('nuke_enabled', False)
            self.bot.save_config()
            embed = Embed(title='Nuking in process', description=f"Nuke status set to {self.bot.b_config['nuke_enabled']}")
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Nuke error', description='Hahaha pranked, \n You are not the bot owner!')
            await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Owner(bot))


def teardown(bot):
    bot.remove_cog("Owner")
