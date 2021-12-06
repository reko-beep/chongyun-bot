import json
import os 

from asyncio import TimeoutError, sleep

import nextcord as discord
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks



from base.lobby import Lobby
from base.quests import GenshinQuests
from base.quotes import GenshinQuotes
from base.database import GenshinDB

from base.guides import GenshinGuides
from base.scraper import search_page,unpack_anime

from ast import literal_eval

from core.paimon import Paimon


#   DUPLICATE MAYBE
#
# client: Bot and paimon: Paimon (subclass of Bot) are same
#pmon = Paimon(config_file="settings.json")
#client = pmon


#settings_data = pmon.get_config()


# client: Bot and paimon: Paimon (subclass of Bot) are same
pmon = Paimon(config_file="settings.json")
client = pmon




data = {}


quotes_ = GenshinQuotes()



@client.command(aliases=['pq'])
async def paimonquotes(ctx,arg:str="",quotes:str=""):
    if arg == 'add':
        if quotes != "":
            quotes_.add_quote(quotes)
            embed = discord.Embed(title='Paimon thanks you!',description=f'{quotes} added in paimon mind!',color=0xf5e0d0)            
            file_paimon = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
            embed.set_thumbnail(url=f'attachment://happy.png')            
            await ctx.send(embed=embed,file=file_paimon)
    else:
        if arg == "":
            quote_ = quotes_.get_random_quote()
            embed = discord.Embed(title='Paimon says!',description=f'{quote_}',color=0xf5e0d0)            
            file_paimon = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
            embed.set_thumbnail(url=f'attachment://happy.png')            
            await ctx.send(embed=embed,file=file_paimon)




# client.listen('on_message') replaces client.event
# because former can be used any number of times, without overriding.
# this is preferred way when using Cogs.    
@client.listen('on_message')
async def on_message(message):

    if message.guild is not None:
        if message.channel.id == client.p_bot_config['leak_channel']:

            checks = ('http' in message.content or 'https' in message.content or len(message.embeds) != 0 or len(message.attachments != 0))
            if checks: 
                pass
            else:
                await message.delete()

    
                


@client.event
async def on_ready():
    
    """
    channel = client.get_channel(announce_channel)
   
    
    
    embed = discord.Embed(title='Paimon is live!',description=f'Hello tra-travel-traveller!\n Paimon is here!',color=0xf5e0d0)
    file = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
    embed.set_thumbnail(url=f'attachment://happy.png')
    await channel.send(embed=embed,file=file)
    
    announce_data = {}
    if os.path.exists('announcement.json'):
        with open('announcement.json','r') as f:
            announce_data = json.load(f)
    if announce_data['announce'] == 'true':
        embed = discord.Embed.from_dict(announce_data['embed'])   
        await channel.send(embed=embed)   
    """


@client.command()
async def hold(ctx):    
    if ctx.voice_client is not None:
        await ctx.send('I am already holding a channel')
    else:
        connected = ctx.author.voice
        if connected:            
            await connected.channel.connect()
            await ctx.send(f'Holding {connected.channel.name} for you')
        else:
            await ctx.send('You are not in any voice channel')

@client.command()
async def leave(ctx):    
    if ctx.voice_client is None:
        await ctx.send("I'm not in a voice channel, use the hold command to make me join")
    else:        
        await ctx.voice_client.disconnect()
        await ctx.send('Bot left')
       

    
@client.command()
async def announce( ctx, *,arg: str):
    check_roles = client.p_bot_config['mod_role']
    user_roles = [r.id for r in ctx.author.roles]
    check = (len(set(check_roles).intersection(user_roles)) != 0)    
    dict_ = ''.join(arg)
    print(dict_)
    if check:        
        dict_ = json.loads(dict_)
        embed = Embed.from_dict(dict_)

        await ctx.send(embed=embed)
    else:
        embed = Embed(title='Administration Error!',description=f'You dont have enough perms!',color=0xf5e0d0)  
        embed.set_author(name=ctx.author.display_name,
                            icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
        await ctx.send(embed=embed)



# start paimon bot.  
pmon.p_start()