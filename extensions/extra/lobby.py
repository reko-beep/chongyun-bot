from nextcord import Embed, Member, File
from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot

from base.lobby import Lobby
from core.paimon import Paimon
import nextcord as discord

from asyncio import sleep
from util.logging import logc

from os import getcwd


class Lobbies(commands.Cog):
    def __init__(self, pmon: Paimon) -> None:
        self.pmon = Paimon
        
        self.voice_handler = Lobby(self.pmon)

    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        await self.voice_handler.auto_delete_event(member)
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.voice_handler.set_settings()


    @commands.command(aliases=['la','lallow'])
    async def lobbyallow(self,ctx, member:discord.Member=None):
        if member != None:
            success = await self.voice_handler.allow_member(ctx.author,member)
            if success == None:
                embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                if success == False:
                    embed = Embed(title=f'Error',
                    description='You dont own a lobby!',
                    color=0x5fe0d0)
                    embed.set_author(name=ctx.author.display_name,
                                        icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    if success:
                        embed = Embed(title=f'Lobby Perms changed!',
                        description=f'{member.mention} can join the lobby now!\n**Lobby:**\n{success.name}',
                        color=0x5fe0d0)
                        embed.set_author(name=ctx.author.display_name,
                                        icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)

    @commands.command(aliases=['lk','lkick'])
    async def lobbykick(self,ctx, member:discord.Member=None):   
        success = await self.voice_handler.kick_member(ctx.author,member)
        if success == None:
            embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            if success == False:
                embed = Embed(title=f'Error',
                description='Either the member is not in vc or please mention a user!!',
                color=0x5fe0d0)
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                if success:
                    embed = Embed(title=f'Lobby Perms changed!',
                    description=f'{member.mention} cannot join the lobby now!\n**Lobby:**\n{success.name}',
                    color=0x5fe0d0)
                    embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['lua','lunallow'])
    async def lobbyunallow(self,ctx, member:discord.Member=None):   
        success = await self.voice_handler.unallow_member(ctx.author,member)
        if success == None:
            embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            if success == False:
                embed = Embed(title=f'Error',
                description='Either the member is not in vc or please mention a user!!',
                color=0x5fe0d0)
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                if success:
                    await self.voice_handler.kick_member(ctx.author,member)
                    embed = Embed(title=f'Lobby Perms changed!',
                    description=f'{member.mention} cannot join the lobby now!\n**Lobby:**\n{success.name}',
                    color=0x5fe0d0)
                    embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['ll','llimit'])
    async def lobbylimit(self,ctx, limit : int):
        success,channel_ = await self.voice_handler.limit_vc(ctx.author,limit)   
        if success == True:
            if limit == 0:
                embed = Embed(title=f'Lobby limit changed!',
                description=f'Limit set to unlimited!\n**Lobby:**\n{channel_.name}',
                color=0x5fe0d0)
                embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = Embed(title=f'Lobby limit changed!',
                description=f'Limit set to {limit}!\n**Lobby:**\n{channel_.name}',
                color=0x5fe0d0)
                embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['llock'])
    async def lobbylock(self,ctx):
        success,channel_ = await self.voice_handler.lock_vc(ctx.author)   
        if success == True:        
            embed = Embed(title=f'Lobby privacy changed!',
                description=f'Your lobby is private now\n**Lobby:**\n{channel_.name}',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['lul','lunlock','lobbyun'])
    async def lobbyunlock(self,ctx):
        success,channel_ = await self.voice_handler.unlock_vc(ctx.author)   
        if success == True:        
            embed = Embed(title=f'Lobby privacy changed!',
                description=f'Your lobby is now public\n**Lobby:**\n{channel_.name}',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error',
                description='You dont own a lobby!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)


    @commands.command(aliases=['lobbyc','lcreate','lc'])
    async def lobbycreate(self,ctx):    
        success,channel_ =  await self.voice_handler.create_vc(ctx.author)
        if success != None and channel_ != None:
            embed = Embed(title=f'Lobby created',
                description=f'Your lobby has been created\n**Lobby:**\n{channel_.name}',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error',
                description='You are already an owner of an channel!',
                color=0x5fe0d0)
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            


def setup(bot):    
    bot.add_cog(Lobbies(bot))


def teardown(bot):
    bot.remove_cog("Lobbies")