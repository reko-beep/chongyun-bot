from nextcord import Embed, Member, File
from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from nextcord.member import Member
from nextcord.message import Message
from base.database import GenshinDB
from base.resin import Reminder
from core.paimon import Paimon
import nextcord as discord

from asyncio import sleep
from extensions.views.information import InformationDropDown, NavigatableView
from util.logging import logc

from os import getcwd
from asyncio.exceptions import TimeoutError

class UIDManager(commands.Cog):
    
    def __init__(self, pmon: Paimon):
        # pmon: Paimon = client: Bot.
        self.pmon = pmon
        self.db = GenshinDB(pmon)
        self.resin_loaded = None
        self.name = 'UID Manager'
        self.description = f"Commands for Genshin Impact Profiles\n <#{self.pmon.p_bot_config['dropuid_channel']}> is channel where user can drop their uids and get them linked!"

    
    @commands.command(aliases=['glink'],description='glink (uid)\n Links the UID and Region with the user!')
    async def genshinlink(self, ctx, uid=None):
        author_id = str(ctx.author.id)

        # show present uids
        if uid == None:
            servers = self.db.get_servers(author_id)

            if servers != None: # UIDs found.
                description = ''
                for i in servers:
                    description += f'**{i.upper()}**\nUID: {servers[i]}\n\n'

                embed = discord.Embed(
                    title=f'{ctx.author.display_name} Genshin Impact Servers',
                    description=f'\n{description}',
                    color=0xf5e0d0)    

                embed.set_author(
                    name=f'{ctx.author.display_name}',
                    icon_url=f'{ctx.author.avatar.url}')
                
                # note: got rid of files. because file uploads makes response slow.
                # we can have a resources mapper function instead.
                # pamonhappy => https://example.com/paimonhappy.png etc.,
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/898899943807414283/happy.png')            
                await ctx.send(embed=embed)
            
            else: # no UIDs found.   
                embed = discord.Embed(
                    title='Paimon is angry!',
                    description='What do you wa- want, huh~\n please link the id!',
                    color=0xf5e0d0)
                
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/897757609887670283/angry.png')
                await ctx.send(embed=embed)
       
        # add new uid
        else:
            self.db.save_uid(author_id, int(uid))
            linked_message = self.db.prettify_linked_message(ctx.author.display_name, int(uid))
            embed = Embed(title='UID Linked!',
                        description=linked_message
                        ,color=0xf5e0d0)

            await ctx.send(embed=embed)

    # note: users can send only uid in #dropuid_channel, server will be figured automatically. 
    @commands.Cog.listener('on_message')
    async def on_message(self, message: Message):
        if message.guild is not None:   
            if self.resin_loaded is None:
                self.resin_loaded = await self.db.load_resin_reminder()
            if message.channel.id == self.pmon.p_bot_config['dropuid_channel']:            
                author_id = str(message.author.id)
                if message.content.isdigit():

                    uid = int(message.content)
                    # todo: verify uid.
                    self.db.save_uid(author_id, uid)
                    linked_message = self.db.prettify_linked_message(message.author.display_name, uid)
                    embed = Embed(title='UID Linked!',
                                description=linked_message
                                ,color=0xf5e0d0)

                    await message.add_reaction('✅')
                    await message.channel.send(embed=embed)

                    await sleep(2)
                    await message.delete()
                else:
                    if message.author.id != self.pmon.user.id:
                        await message.delete()
        
    @commands.command(aliases=['gwl'])
    async def gworldlevel(self, ctx, region:str = '', worldlevel: str= ''):
        if region != '':
            if worldlevel != '':
                if worldlevel.isdigit() and 1 <= int(worldlevel) <= 8:                
                    check = self.db.set_world_level(ctx.author, region, worldlevel)
                    print(check)

                    if check is not None:
                        embed = Embed(title='WL set!',
                                description=f'{region.upper()} world level set to {worldlevel}'
                                ,color=0xf5e0d0)

                        await ctx.send(embed=embed)
                    
                    else:
                        embed = Embed(title='Failed!',
                                description=f'Failed to set {region.upper()} world level to {worldlevel}'
                                ,color=0xf5e0d0)

                        await ctx.send(embed=embed)
                else:
                    embed = Embed(title='Failed!',
                            description=f'Please provide a number (1-8) as world level!'
                            ,color=0xf5e0d0)

                    await ctx.send(embed=embed)
            
            else:
                embed = Embed(title='Failed!',
                        description=f'Please provide a region (eu, asia, na)!'
                        ,color=0xf5e0d0)

                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Failed!',
                    description=f'Please provide a region (eu, asia, na)!'
                    ,color=0xf5e0d0)

            await ctx.send(embed=embed)




    
    @commands.command(aliases=['gserv','gservers'],description='gserv (user `optional`)\nShows the linked uids of a user or either the user who has invoked the command ')
    async def gserver(self,ctx, user: Member = None, region:str = ''):

        if not user:
            user = ctx.author
        
        id = str(user.id)
        servers = self.db.get_servers(id)
        worldlevel = self.db.get_wls(id)
        print(worldlevel)
        if servers:
            embed = discord.Embed(
                        title=f'Genshin Impact servers!'
                        ,color=0xf5e0d0)    

            embed.set_author(name=f'{user.display_name}',icon_url=user.avatar.url)
            if region == '':

                for server in servers:
                    desp_ = f'UID: {servers[server]}'                
                    if worldlevel is not None:              
                        if server in worldlevel:
                            desp_ += f'\nWorld level: {worldlevel[server]}'
                        else:
                            desp_ += f'\nuse !gwl ({server}) (world level)!'
                    else:
                        desp_ += f'\nuse !gwl ({server}) (world level)!'
                    embed.add_field(name=server.upper(),value=f'{desp_}', inline=True)  
                    
            
            else:

                if region in servers:
                    desp_ = f'UID: {servers[region]}'   
                    
                    if region in worldlevel:
                        desp_ += f'\nWorld level: {worldlevel[region]}'
                    else:
                        desp_ += f'\nuse !gwl ({region}) (world level)!'
                    embed.add_field(name=region.upper(),value=f'{desp_}', inline=True)  
                else:
                    embed.add_field(name=region.upper(),value=f'Not linked yet!')

           
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/898899943807414283/happy.png')

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title='Paimon is angry!',
                    description='What do you wa- want, huh~\n please link the id!',
                    color=0xf5e0d0)
                
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/897757609887670283/angry.png')
            await ctx.send(embed=embed)

    
    @commands.command(aliases=['guid'],description='guid (uid)\n shows the discord user which has linked the uid!')
    async def genshinuid(self, ctx, uid: str):
        user , region = self.db.get_discord_user_from_uid(uid)
        if user is not None and region is not None :
            embed = Embed(title='Genshin Impact account'
                    ,color=0xf5e0d0)
            embed.add_field(name='UID',value=uid)
            embed.add_field(name='Region',value=region.upper())
            embed.set_author(name=str(user),icon_url=user.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Error'
                    ,description='Pai-paimon is sorry!\ncould not find any discord user having that uid!'
                    ,color=0xf5e0d0)
            await ctx.send(embed=embed)
        
    @commands.command(aliases=['gc','genshinchar','gchar','gchars'],description='gchar (region) (member `optional`)\nShows the most used characters of a user from genshin api!')
    async def genshincharacters(self,ctx,  region:str, member: Member = None):

        if member is None:
            member = ctx.author

        uid = self.db.get_uid(str(member.id), region.lower())

        if region != "": 
            
            # if region is not empty
            


            # if user has linked the uid 

            embeds,emojis = self.db.create_characters_embed(uid)
            count = len(embeds)-1
            select = 0
            stop = False            
            if len(embeds) > 1:

                embeds[str(select)]['character'].set_footer(text= f'{member.display_name}')
                embeds[str(select)]['character'].set_thumbnail(url=member.avatar.url)
                msg = await ctx.send(embed=embeds[str(select)]['character'])
                for emoji in emojis:
                    await msg.add_reaction(emoji)

                while stop == False:
                    try:
                        def check(reaction,user):
                            return reaction.message.id == msg.id and user == ctx.author
                        reaction, user = await self.pmon.wait_for('reaction_add',
                                                                check=check,
                                                                timeout=60)
                    except TimeoutError:
                        await msg.clear_reactions()
                    else:  
                        if reaction.emoji == '⚔️':
                            embeds[str(select)]['character'].set_footer(text= f'{member.display_name}')
                            embeds[str(select)]['weapon'].set_thumbnail(url=member.avatar.url)
                            await msg.edit(embed=embeds[str(select)]['weapon'])

                        if reaction.emoji == '➡️':
                            if select < count:
                                select += 1
                                embeds[str(select)]['character'].set_footer(text= f'{member.display_name}')
                                embeds[str(select)]['character'].set_thumbnail(url=member.avatar.url)
                                await msg.edit(embed=embeds[str(select)]['character']) 

                        if reaction.emoji == '⬅️':
                            if select >= 1:
                                select -= 1
                                embeds[str(select)]['character'].set_footer(text= f'{member.display_name}')
                                embeds[str(select)]['character'].set_thumbnail(url=member.avatar.url)
                                await msg.edit(embed=embeds[str(select)]['character'])
            else:
                if len(embeds) != 0:
                    embeds['0']['character'].set_author(name=member.display_name,icon_url=member.avatar.url)
                    msg = await ctx.send(embed=embeds[str(select)]['character'])
                    while stop == False:
                        try:
                            def check(reaction,user):
                                return reaction.message.id == msg.id and user == ctx.author
                            reaction, user = await self.pmon.wait_for('reaction_add',
                                                                        check=check,
                                                                        timeout=60)
                        except TimeoutError:
                            await msg.clear_reactions()
                        else:                    
                            if reaction.emoji in emojis:
                                if reaction.emoji == '⚔️':
                                    await msg.edit(embed=embeds['0']['weapon'])
                else:                                   
                    embed = Embed(title='Paimon is angry!',
                            description=f"What do you wa- want, huh~\ndrop ur uid in <#{self.pmon.p_bot_config['dropuid_channel']}> \nexample **8566512**",
                            color=0xf5e0d0)
                    file = File(f'{getcwd()}/guides/paimon/angry.png',
                                    filename='angry.png')

                    embed.set_thumbnail(url=f'attachment://angry.png')
                    await ctx.send(embed=embed,file=file)
        else:
            embed = Embed(title='Paimon is angry!',
                            description='What do you wa- want, huh~\n Which server~\n I will eat you!',
                            color=0xf5e0d0)
            file = File(f'{getcwd()}/guides/paimon/angry.png',
                            filename='angry.png')

            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)

    @commands.command(aliases=['gstat','gstats'],description='gstat (region)\nShows the stat of a user genshin impact account!')
    async def genshinstats(self, ctx, region:str = '', member:Member=None):
        
        if member is None:
            member = ctx.author

        uid = self.db.get_uid(str(member.id),region.lower())

        if region != "":

            # if region is not empty

            if uid is not None:

                # if user has linked the uid

                        
                embed = self.db.create_stats_embed(member,uid)

                if embed != None:
                    embed.set_footer(text= f'{member.display_name}')
                    embed.set_thumbnail(url=member.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(title='Paimon is going!',
                    description=f'Sorry traveller, You have not made your data public!',
                                    color=0xf5e0d0)
                    file = File(f'{getcwd()}/guides/paimon/sorry.png',
                                    filename='sorry.png')
                    embed.set_thumbnail(url=f'attachment://sorry.png')

                    await ctx.send(embed=embed,file=file)
            else:
                embed = discord.Embed(title='Paimon is angry!',
                                description=f"What do you wa- want, huh~\ndrop ur uid in <#{self.pmon.p_bot_config['dropuid_channel']}> \nexample **8566512**"
                                ,color=0xf5e0d0)
                file = File(f'{getcwd()}/guides/paimon/angry.png',
                            filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')

                await ctx.send(embed=embed,file=file)
        else:
            embed = discord.Embed(title='Paimon is angry!',
                                description='What do you wa- want, huh~\n Which server~\n I will eat you!',
                                color=0xf5e0d0)
            file = discord.File(f'{getcwd()}/guides/paimon/angry.png',
                                filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')

            await ctx.send(embed=embed,file=file)

    @commands.command(aliases=['gaby','gabyss'],description='gabyss (region)\nShows the abyss stats of a user genshin impact account!')
    async def genshinabyss(self, ctx, region:str = '', member:Member=None):
        
        if member is None:
            member = ctx.author

        uid = self.db.get_uid(str(member.id),region.lower())

        if region != "":

            # if region is not empty

            if uid is not None:

                # if user has linked the uid
                        
                embeds = self.db.create_abyss_embeds(member,uid)
                uid_member = self.db.get_discord_user_from_uid(uid)
                if embeds != None:
                    view = NavigatableView(member)
                    view.add_item(InformationDropDown(embeds, member))
                    await ctx.send(f'Shows abyss stats for {uid_member}',view=view)
                else:
                    embed = Embed(title='Paimon is going!',
                    description=f'Sorry traveller, You have not made your data public!',
                                    color=0xf5e0d0)
                    file = File(f'{getcwd()}/guides/paimon/sorry.png',
                                    filename='sorry.png')
                    embed.set_thumbnail(url=f'attachment://sorry.png')

                    await ctx.send(embed=embed,file=file)
            else:
                embed = discord.Embed(title='Paimon is angry!',
                                description=f"What do you wa- want, huh~\ndrop ur uid in <#{self.pmon.p_bot_config['dropuid_channel']}> \nexample **8566512**"
                                ,color=0xf5e0d0)
                file = File(f'{getcwd()}/guides/paimon/angry.png',
                            filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')

                await ctx.send(embed=embed,file=file)
        else:
            embed = discord.Embed(title='Paimon is angry!',
                                description='What do you wa- want, huh~\n Which server~\n I will eat you!',
                                color=0xf5e0d0)
            file = discord.File(f'{getcwd()}/guides/paimon/angry.png',
                                filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')

            await ctx.send(embed=embed,file=file)



    @commands.command(aliases=['rs'],description='rs (region)\nShows your resin status!')
    async def resinstatus(self, ctx, region: str = ''):
        if region != '':
            reminder: Reminder = self.db.get_resin_reminder(str(ctx.author.id), region)

            if reminder is not None:
                embed, image = reminder.create_status_embed(ctx.author)
                await ctx.send(embed=embed,file=image)

            else:
                embed = discord.Embed(title='Paimon is angry!',
                                    description='You have not set up the reminder!',
                                    color=0xf5e0d0)
                file = discord.File(f'{getcwd()}/guides/paimon/angry.png',
                                    filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')

                await ctx.send(embed=embed,file=file)
        else:
            embed = discord.Embed(title='Paimon is angry!',
                            description=f"What do you wa- want, huh~\nYou either have not linked the id for this region or have not set up the reminder!"
                            ,color=0xf5e0d0)
            file = File(f'{getcwd()}/guides/paimon/angry.png',
                        filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)

    @commands.command(aliases=['rt'],description='rt (region)\nShows your remaining time for resin to fill up!')
    async def resintime(self, ctx, region: str = ''):
        if region != '':
            reminder: Reminder = self.db.get_resin_reminder(str(ctx.author.id), region)

            if reminder is not None:
                remaining, next = reminder.get_remaining_time()
                resin = reminder.get_current_resin() 
                embed = Embed(title=f'Resin remaining time!',description=f'**Current Resin:**\n{resin}\n**Remaining time for resin to fill up:**\n{remaining}\n**Time for resin to turn {resin+ 1}:**\n{next}',color=0xf5e0d0)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url='https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png')
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title='Paimon is angry!',
                                    description='You have not set up the reminder!',
                                    color=0xf5e0d0)
                file = discord.File(f'{getcwd()}/guides/paimon/angry.png',
                                    filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')

                await ctx.send(embed=embed,file=file)
        else:
            embed = discord.Embed(title='Paimon is angry!',
                                description=f"What do you wa- want, huh~\nYou either have not linked the id for this region or have not set up the reminder!"
                                ,color=0xf5e0d0)
            file = File(f'{getcwd()}/guides/paimon/angry.png',
                        filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)


    @commands.command(aliases=['rr'],description='rr (region) (resin)\nShows your resin status!')
    async def resinreminder(self, ctx, region: str = '',resin : str='0'):

        
        
        account = self.db.get_servers(str(ctx.author.id))

        if account is None:

            embed = discord.Embed(title='Paimon is angry!',
                                description=f"What do you wa- want, huh~\ndrop ur uid in <#{self.pmon.p_bot_config['dropuid_channel']}> \nexample **8566512**"
                                ,color=0xf5e0d0)
            file = File(f'{getcwd()}/guides/paimon/angry.png',
                        filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)

        else:
            
            if region.lower() in account:
                resin = int(resin)
                reminder: Reminder = await self.db.add_resin_reminder(ctx.author, region, resin, ctx)

                if reminder is not None:
                    
                    embed, image = reminder.create_status_embed(ctx.author)
                    await ctx.send(embed=embed,file=image)

                else:
                    embed = discord.Embed(title='Paimon is sorry!',
                                        description='Could not setup the reminder!',
                                        color=0xf5e0d0)
                    file = discord.File(f'{getcwd()}/guides/paimon/angry.png',
                                        filename='angry.png')
                    embed.set_thumbnail(url=f'attachment://angry.png')

                    await ctx.send(embed=embed,file=file)
            
            else:
                embed = discord.Embed(title='Paimon is angry!',
                                description=f"What do you wa- want, huh~\nYou either have not linked the id for this region!"
                                ,color=0xf5e0d0)
                file = File(f'{getcwd()}/guides/paimon/angry.png',
                            filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')
                await ctx.send(embed=embed,file=file)



def setup(client):
    client.add_cog(UIDManager(client))


def teardown(client):
    client.remove_cog("UIDManager")



