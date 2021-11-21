from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from nextcord.member import Member
from nextcord.message import Message
from base.database import GenshinDB
from core.paimon import Paimon
import nextcord as discord

from asyncio import sleep
from util.logging import logc




class UIDManager(commands.Cog):
    
    def __init__(self, pmon: Paimon):
        # pmon: Paimon = client: Bot.
        self.pmon = pmon
        self.db = GenshinDB(pmon)

    
    @commands.command()
    async def uid(self, ctx, uid=None):
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
                await message.add_reaction('✅')
                await message.channel.send(linked_message)

                await sleep(2)
                await message.delete()
            else:
                if message.author.id != self.pmon.user.id:
                    await message.delete()
    
    @commands.command(aliases=['gserv','gservers'])
    async def gserver(self,ctx, user: Member = None):

        if not user:
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


        






def setup(client):
    client.add_cog(UIDManager(client))


def teardown(client):
    client.remove_cog("UIDManager")



