from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from nextcord.message import Message
from base.database import GenshinDB
from core.paimon import Paimon
import nextcord as discord

from util.logging import logc


db = GenshinDB()

class UIDManager(commands.Cog):
    def __init__(self, pmon: Paimon):
        # pmon: Paimon = client: Bot.
        self.pmon = pmon

    
    @commands.command()
    async def uid(self, ctx, uid=None):
        author_id = str(ctx.author.id)

        # show present uids
        if uid == None:
            servers = db.get_servers(author_id)

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
            db.save_uid(author_id, int(uid))
            await ctx.message.add_reaction('✅')
    

    # note: users can send only uid in #dropuid_channel, server will be figured automatically. 
    @commands.Cog.listener('on_message')
    async def on_message(self, message: Message):

        if message.channel.id == self.pmon.p_bot_config['dropuid_channel']:
            author_id = str(message.author.id)
            uid = int(message.content)
            # todo: verify uid.
            db.save_uid(author_id, uid)
            await message.add_reaction('✅')
    






def setup(client):
    client.add_cog(UIDManager(client))


def teardown(client):
    client.remove_cog(UIDManager(client))



