from nextcord.channel import DMChannel, VoiceChannel
from nextcord.ext import commands
from nextcord import Embed, File,Member, Role
from nextcord.ext.commands.core import command
from nextcord.ui import View
from nextcord.utils import get

from base.administration import AdministrationBase

from core.paimon import Paimon
from util.logging import logc


class Administration(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.administration_handler = AdministrationBase(pmon)
        self.pmon = pmon
        self.name = 'Administration'
        self.description = 'Mod only commands! Nothing to see here!'

    
    @commands.command(aliases=['aq','addq'],description='aq (question)\n adds a question to list, which are to be asked when scrutiny is turned one ')
    async def addquestions(self, ctx , *,arg : str):
        question = ''.join(arg)
        check = self.administration_handler.add_questions(ctx,question)
        if question != '':
            if check:
                embed = Embed(title='Question added for scrutiny!',description=f'**Question:**\n{question}',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'Please write a question!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['cq','clearq'],description='Clears all question from list')
    async def clearquestions(self, ctx ):
        check = self.administration_handler.clear_questions(ctx)

        if check == True:
            embed = Embed(title='All questions removed for scrutiny!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['tq','testq'],description='Sends a test question list to check!')
    async def testquestions(self, ctx ):
        embed = self.administration_handler.create_question_embed(ctx.author)        
        await ctx.send(embed=embed)

    @commands.command(aliases=['scr'],description='Toggles scrutiny status!')
    async def scrutiny(self, ctx ):
        check = self.administration_handler.toggle_scrutiny(ctx)

        if check is not None:
            embed = Embed(title='Scrutiny option changed!', description=f'**Status:**\n{check}',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['scrc'],description='scrc \nsets channel where questions are to be asked')
    async def scrutinychannel(self, ctx ):
        check = self.administration_handler.set_scrutiny_channel(ctx, ctx.message.channel)

        if check is not None:
            embed = Embed(title='Scrutiny Channel changed!', description=f'**Channel set to <#{ctx.channel.id}>',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['aprv'],description='aprv\n approves a member')
    async def approve(self, ctx , member: Member= None):        
        if member is not None:
            check = await self.administration_handler.approve_member(ctx, member)
            if check is True:
                embed = Embed(title='Approved!', description=f'{member.display_name} approved.',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'Failed to approve member\n it may be due to perms!!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'Please mention a member!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(aliases=['coopc'],description='coopc \nsets channel where people ask for help')
    async def coopchannel(self, ctx ):
        check = self.administration_handler.set_helper_channel(ctx, ctx.message.channel)

        if check is not None:
            embed = Embed(title='Coop Channel changed!', description=f'**Channel set to <#{ctx.channel.id}>',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(aliases=['eventc','evc'],description='evc \nsets channel where events will posted')
    async def eventchannel(self, ctx ):
        check = self.administration_handler.set_event_channel(ctx, ctx.message.channel)

        if check is not None:
            embed = Embed(title='Event Channel changed!', description=f'**Channel set to <#{ctx.channel.id}>',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(description='coop \nShows the channel where events will posted')
    async def coop(self, ctx ):
        check = self.administration_handler.get_helper_channel()

        if check is not None:
            embed = Embed(title='Co-op Channel!', description=f'**Channel set to <#{check.id}>',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['eventconfig','evcc'],description='evc \nShows the channel where events will posted')
    async def eventchannelconfig(self, ctx ):
        check = self.administration_handler.get_event_channel(ctx)

        if check is not None:
            embed = Embed(title='Event Channel!', description=f'**Channel set to <#{check.id}>',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(aliases=['scrs'],description='Shows scrutiny status!')
    async def scrutinystatus(self, ctx ):
        check = self.administration_handler.get_scrutiny()
        channel = self.administration_handler.get_scrutiny_channel()
        role = self.administration_handler.scrutiny_role
        text = ''
        if check == True:
            text = f'**Status:**\nActive.'
        if check == False:
            text = f'**Status:**\nUnactive.'
        if check is not None:
            if channel is not None:
                text += f'\n**Channel:**\n{channel.mention}'
            if role is not None:
                text += f'\n**Role:**\n {role.mention}'
            embed = Embed(title='Scrutiny!', description=text,color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['fmr','filterrole','scrr'],description='scrr (role)\nSets the scrutiny role')
    async def filtermemberrole(self, ctx ,role: Role = None):
        if role is not None:
            check = self.administration_handler.set_scrutiny_role(ctx, role)
            
            if check is not None:
                embed = Embed(title='Scrutiny role set!', description=f'**Role set to **\n{role.mention}',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You have not mentioned the role!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # roundabout way to solve on_ready not working
        if message.guild is not None:        
            guild = message.guild
            self.administration_handler.get_essentials(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        status = self.administration_handler.get_scrutiny()
        await self.administration_handler.assign_role(member)
        if status == True:
            embed = self.administration_handler.create_question_embed(member)
            channel = self.administration_handler.get_scrutiny_channel()
            if channel is not None:
                await channel.send(member.mention, embed=embed)

    @commands.command(aliases=['mods'],description='Shows the list of mod roles, which are allowed to use these commands!')
    async def moderator(self, ctx):
        
        check = self.administration_handler.get_mod_roles()
        
        if len(check) != 0:
            text = '\n'.join(check)
            embed = Embed(title='Mod Roles!', description=f'{text}',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'No Mod role set!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
    
    @commands.command(description='Shows the list of carry roles!')
    async def carry(self, ctx):
        
        check = self.administration_handler.get_carry_roles()
        
        if len(check) != 0:
            text = '\n'.join(check)
            embed = Embed(title='Carry Roles!', description=f'{text}',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'No carry role set!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(description='addcarry (role)\nAdds the specified role to carry roles list!')
    async def addcarry(self, ctx, role: Role):
        if role is not None:
            check = self.administration_handler.add_carry_role(ctx, role)
            
            if check is not None:
                embed = Embed(title='Carry role added!', description=f'{role.mention} added!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You have not mentioned the role!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['rcarry'],description='rcarry (role)\n Removes the role from carry list!')
    async def removecarry(self, ctx, role: Role):
        if role is not None:
            check = self.administration_handler.remove_carry_role(ctx, role)
            
            if check is not None:
                embed = Embed(title='Carry role removed!', description=f'{role.mention} removed!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You have not mentioned the role!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)


    @commands.command(aliases=['addmods'],description='addmods (role)\nAdds the specified role to mod list!')
    async def addmoderator(self, ctx, role: Role):
        if role is not None:
            check = self.administration_handler.add_mod_role(ctx, role)
            
            if check is not None:
                embed = Embed(title='Mod role added!', description=f'{role.mention} added!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You have not mentioned the role!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['rmods'],description='rmods (role)\n Removes the role from mod list!')
    async def removemoderator(self, ctx, role: Role):
        if role is not None:
            check = self.administration_handler.remove_mod_role(ctx, role)
            
            if check is not None:
                embed = Embed(title='Mod role removed!', description=f'{role.mention} removed!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)
            else:
                embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0) 
                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You have not mentioned the role!',color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['lbc'], description='lbc (voice channel id or mention)\nSets the vc to create custom lobbies when joined!')
    async def lobbychannel(self, ctx , channel : VoiceChannel):
        check = self.administration_handler.set_voicecreate_channel(ctx, channel)

        if check is not None:
            embed = Embed(title='🔊 Lobby Channel changed!', description=f'**You can now join <#{channel.id}> to create custom lobbies.\n**Category:**\n{channel.category.mention}',color=0xf5e0d0)  
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0)  
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['lb'],description='Shows custom lobbies status!')
    async def lobbystatus(self, ctx ):
        channel = self.administration_handler.get_lobby_channel()
        category = self.administration_handler.get_lobby_category()        
        text = f'**Status:**\n Active.'
        if channel is not None:
            text += f'\n**Channel:**\n{channel.mention}'
            if category is not None:
                text += f'\n**Category:**\n{category.mention}'
            embed = Embed(title='🔊 Custom Lobbies!', description=text,color=0xf5e0d0) 
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0)  
            embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Administration(bot))


def teardown(bot):
    bot.remove_cog("Administration")
