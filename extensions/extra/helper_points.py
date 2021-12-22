from nextcord.channel import DMChannel, VoiceChannel
from nextcord.ext import commands
from nextcord import Embed, File,Member, Role
from nextcord.message import Message

from nextcord.ui import View
from nextcord.utils import get

from base.helper_point import HelperBase

from core.paimon import Paimon
from extensions.views.guides import NavigatableView
from extensions.views.information import InformationDropDown
from util.logging import logc


class HelperPoints(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        self.help_handler = HelperBase(self.pmon)
        pass

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id == self.pmon.p_bot_config['coop_channel']:
            print('coop', 'yes')
            check = self.help_handler.add_asker(message.author, message.role_mentions) 
            print(check)
            if check:
                embed = Embed(title='Co-op',description=f'You are eligible to give a co-op point after you have received help!',color=0xf5e0d0) 
                embed.set_footer(text=f'!cogp (usermention)')
                await message.channel.send(embed=embed)
            if check is False:
                embed = Embed(title='Co-op',description=f'You havr been banned from giving co-op points!!',color=0xf5e0d0) 
                await message.channel.send(embed=embed)

    @commands.command(aliases=['colb'],description='colb\nShows coop leaderboard!')
    async def coopleaderboard(self, ctx):
        embeds = self.help_handler.create_lbpages(10)
        view = NavigatableView(ctx.author)
        view.add_item(InformationDropDown(embeds, ctx.author))
        await ctx.send(content='Co-op leaderboard', view=view)
    
    @commands.command(aliases=['colbrs'], description='colbrs\nResets the leader board')
    async def coopleaderboardreset(self, ctx):
        check = self.help_handler.reset_lb(ctx)
        if check:
            embed = Embed(title=f'Co-op points added!', description=f'Co-op leaderboard reset!',color=0xf5e0d0)            
            embed.set_thumbnail(url='https://i.imgur.com/CDYa78r.png')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error!', description='You donnot have administration privilege!',color=0xf5e0d0)            
            embed.set_thumbnail(url='https://i.imgur.com/CDYa78r.png')
            await ctx.send(embed=embed)

        

    @commands.command(aliases=['cogpoint','cogp'], description='cogp (member)\nGives other co-op point')
    async def coopgivepoint(self, ctx, member: Member=None):
        if member == None:
            
            embed = Embed(title=f'Co-op error', description='Please mention a user',color=0xf5e0d0) 
            await ctx.send(embed=embed)
        
        else:
            if member is not ctx.author:
                check = self.help_handler.add_helper_point(ctx, member)

                if check:
                    embed = Embed(title=f'Co-op points added!', description=f'You have given {member.display_name} one co-op point!',color=0xf5e0d0) 
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(title=f'Co-op error', description='You have not asked for help yet\nTag a carry role!',color=0xf5e0d0) 
                    await ctx.send(embed=embed)

            else:
                embed = Embed(title=f'Co-op error', description='You cant give yourself co-op point!',color=0xf5e0d0) 
                await ctx.send(embed=embed)

    @commands.command(aliases=['copoints','cops'], description='cops (member)\n Shows yours or other members co-op point!')
    async def cooppoints(self, ctx, member: Member=None):
        if member is None:
            member = ctx.author
        
        embed = self.help_handler.get_coopoint(member)

        if embed is  None:

            embed = Embed(title=f'Co-op error', description='Could not find your co-op points',color=0xf5e0d0) 
            await ctx.send(embed=embed)
        
        else:
            
            await ctx.send(embed=embed)

    @commands.command(aliases=['coegp'], description='cops (member)\n Shows yours or other members eligible co-op point that he or you can give!')
    async def coopeligible(self, ctx, member: Member=None):
        if member is None:
            member = ctx.author
        
        value = self.help_handler.get_eligible_points(member)

        if value is  None:

            embed = Embed(title=f'Co-op error', description='Could not find your eligible co-op points',color=0xf5e0d0) 
            await ctx.send(embed=embed)
        
        else:
            emoji = get(ctx.guild.emojis, name='coop')
            embed = Embed(title=f'{member.display_name} Eligible co-op points', description=f'can give {value} {emoji} co-op points',color=0xf5e0d0) 
            await ctx.send(embed=embed)

    @commands.command(aliases=['coregp'], description='coregp (member)\n Removes all eligible votes of a user!')
    async def coopremoveeligible(self, ctx, member: Member=None):
        
        
        if member is not None:
            check = self.help_handler.remove_eligible_points(ctx, member)

            if check is  None:

                embed = Embed(title=f'Co-op error', description=f'Could not remove {member.display_name} eligible points!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
            
            else:
                emoji = get(ctx.guild.emojis, name='coop')
                embed = Embed(title=f'{member.display_name} Eligible co-op points', description=f'All eligible points removed!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Co-op error', description='Please mention a user',color=0xf5e0d0) 
            await ctx.send(embed=embed)

    @commands.command(aliases=['cogban'], description='cogban (member)\n Ban user from giving points!')
    async def coopgiveban(self, ctx, member: Member=None):
        
        
        if member is not None:
            check = self.help_handler.ban_asker(ctx, member)

            if check is  None:

                embed = Embed(title=f'Co-op error', description=f'You are not the bot owner!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
            
            else:
                emoji = get(ctx.guild.emojis, name='coop')
                embed = Embed(title=f'{member.display_name} status', description=f'banned from giving co-op points!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Co-op error', description='Please mention a user',color=0xf5e0d0) 
            await ctx.send(embed=embed)

    @commands.command(aliases=['cogunban'], description='cogunban (member)\n Unbans user!')
    async def coopgiveunban(self, ctx, member: Member=None):
        
        
        if member is not None:
            check = self.help_handler.removeban_asker(ctx, member)

            if check is  None:

                embed = Embed(title=f'Co-op error', description=f'You are not the bot owner!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
            
            else:
                emoji = get(ctx.guild.emojis, name='coop')
                embed = Embed(title=f'{member.display_name} status', description=f'unbbanned , he can now give co-op points!',color=0xf5e0d0) 
                await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Co-op error', description='Please mention a user',color=0xf5e0d0) 
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(HelperPoints(client))


def teardown(client):
    client.remove_cog("HelperPoints")


    
    




