from nextcord import Embed, Member, File
from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from nextcord.member import Member
from nextcord.message import Message
from base.database import GenshinDB
from core.paimon import Paimon
import nextcord as discord

from asyncio import sleep
from util.logging import logc

from os import getcwd


class UIDManager(commands.Cog):
    
    def __init__(self, pmon: Paimon):
        # pmon: Paimon = client: Bot.
        self.pmon = pmon
        self.db = GenshinDB(pmon)

    '''
    @commands.command(aliases=['glink'])
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

            # todo: verify uid.
            self.db.save_uid(author_id, int(uid))
            await ctx.message.add_reaction('✅')
    
    '''

    # note: users can send only uid in #dropuid_channel, server will be figured automatically. 
    @commands.Cog.listener('on_message')
    async def on_message(self, message: Message):

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
    
    @commands.command(aliases=['gserv','gservers'])
    async def gserver(self,ctx, user: Member = None):

        if user is not None:
            user = ctx.author
        
        id = str(user.id)
        servers = self.db.get_servers(id)

        if servers:
            embed = discord.Embed(
                        title=f'Genshin Impact servers!'
                        ,color=0xf5e0d0)    

            embed.set_author(name=f'{user.display_name}',icon_url=user.avatar.url)

            for server in servers:
                embed.add_field(name=server.upper(),value=f'UID: {servers[server]}')

            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/898899943807414283/happy.png')

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title='Paimon is angry!',
                    description='What do you wa- want, huh~\n please link the id!',
                    color=0xf5e0d0)
                
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/897757609887670283/angry.png')
            await ctx.send(embed=embed)

    
    @commands.command(aliases=['guid'])
    async def genshinuid(self, ctx, uid: str):
        user , region = self.db.get_discord_user_from_uid(uid)
        if not user and not region:
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
        
    @commands.command(aliases=['gc','genshinchar','gchar','gchars'])
    async def genshincharacters(self,ctx,  region:str, member: Member = None):

        if member:
            member = ctx.author

        uid = self.db.get_uid(str(member.id), region.lower())

        if region != "": 
            
            # if region is not empty
            

            if uid is not None:

                # if user has linked the uid 

                data = self.db.get_uiddata(uid)
                embeds,emojis = self.db.create_characters_embed(data)
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

    @commands.command(aliases=['gstat','gstats'])
    async def genshinstats(self, ctx, region:str, member:Member=None):
        
        if member:
            member = ctx.author

        uid = self.db.get_uid(str(member.id),region.lower())

        if region != "":

            # if region is not empty

            if uid is not None:

                # if user has linked the uid

                data = self.db.get_uiddata(uid)

                if data != None:            
                    embed = self.db.create_stats_embed(data)

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
                                description="What do you wa- want, huh~\ndrop ur uid in <#{self.pmon.p_bot_config['dropuid_channel']}> \nexample **8566512**"
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


    #todo: glink command

def setup(client):
    client.add_cog(UIDManager(client))


def teardown(client):
    client.remove_cog("UIDManager")



