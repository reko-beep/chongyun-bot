import json
import os 

from asyncio import TimeoutError, sleep
from random import random,choice

import nextcord as discord
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks



from base.lobby import Lobby
from base.notifier import ResetNotifier
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
resetter_ = ResetNotifier(client)


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

@client.command(aliases=['rst'])
async def resettime(ctx):
    
    asia, eu, na = resetter_.get_resettimes()
    
    imgs = ['https://images.wallpapersden.com/image/wxl-fischl-genshin-impact_73974.jpg','https://2.bp.blogspot.com/-YSRL7xmCD2Q/XQ8eHaJ9wkI/AAAAAAAAHtA/0-bVcL3HJmQ4eCCCJY8Sq9y0tGKoVw3IwCKgBGAs/w0/genshin-impact-uhdpaper.com-4K-1.jpg','https://i.pinimg.com/736x/60/65/58/606558b77cb2d8f97487df1f9eba8288.jpg','https://mocah.org/uploads/posts/341533-Genshin-Impact-Video-Game-Characters-Paimon-Klee-Venti-Kaeya-Female-Traveler.jpg','https://wallpaperfordesktop.com/wp-content/uploads/2021/06/Genshin-Impact-Wallpaper.jpg','http://www.movie-trailers-blaze.com/wp-content/uploads/2021/01/genshin-impact-ganyu-abilities-backstory-01.jpg','https://www.nawpic.com/media/2020/genshin-impact-nawpic-3-scaled.jpg','https://wallpaperforu.com/wp-content/uploads/2021/07/Wallpaper-Genshin-Impact-Qiqi-Genshin-Impact-Diona-Ge31.jpg','https://cdn-cf-east.streamable.com/image/fl4fpt.jpg?Expires=1638125580&Signature=jnHu08yqeKWtF~PHsdd6G3cVGlmGhNrOC8ncOU06Rr3~zB0vSfBeaJTWHHxZot03BHbyARtxJju8txdYN1NcePGYvpImwh9-053tV76IgA4M-WH9imKZiZy1CAkrKon20vj0hjg5Wtt~9eWakjAW0450hZV1QM6v5rBlbU5mtzm6t~eXXcjIqPvo2vMlAvdsrzrv1unlQaMZpTBacciXzRdqHcpvTNijN3u10q~TWCxjKIIV7S~Uk5hXHSJHGLzyT~sFa3iVqYmgoxETs3jweah7eENpVJP4tHJKdj1OyWRteUbj10BCsLpVVd2299cjFUXaL72ou-9oVrpzu67L-Q__&Key-Pair-Id=APKAIEYUVEN4EVB2OKEQ','https://c4.wallpaperflare.com/wallpaper/180/788/983/genshin-impact-ganyu-genshin-impact-hd-wallpaper-preview.jpg','https://www.enjpg.com/img/2020/genshin-impact-17.jpg']
    
    embed = discord.Embed(title='Commissions reset times!',description=f'These are calculated according to Pakistan Standard Time',color=0xf5e0d0)  
    embed.add_field(name='Asia', value=asia)
    embed.add_field(name='EU', value=eu)
    embed.add_field(name='NA', value=na)
    embed.set_image(url=choice(imgs))           
    await ctx.send(embed=embed)
   



# client.listen('on_message') replaces client.event
# because former can be used any number of times, without overriding.
# this is preferred way when using Cogs.    
@client.listen('on_message')
async def on_message(message):

    if message.guild is not None:
        if message.channel.id == client.p_bot_config['leak_channel']:

            checks = ('http' in message.content or 'https' in message.content or len(message.embeds) != 0 or len(message.attachments) != 0 or message.webhook_id)
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