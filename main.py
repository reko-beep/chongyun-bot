import json
import os 
from json import load

from asyncio import TimeoutError, sleep
from random import random,choice,seed, shuffle

import nextcord as discord
from nextcord import Webhook
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks
import time
import aiohttp

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


#
#
# load character names and icons for webhooks
#
#

q_webhook  = 'webhook url'
webhook_data = {}
webhook_quotes = {}

with open(os.getcwd()+ '/assets/char_quotes.json', 'r') as f:
    webhook_quotes = load(f)
   

with open(os.getcwd()+ '/assets/Information/characters.json', 'r') as f:
    d = load(f)
    for key in d:
        if 'image' in d[key]:
            image = d[key]['image']
            portrait = [i for i in image if 'thumb' in i.lower()]
            webhook_data[key] = image[0]
            if bool(portrait):
                webhook_data[key] = portrait[0]

print(webhook_data)
print(webhook_quotes)

def random_webhook_character(goodmorning: bool, goodnight: bool):

    if bool(webhook_data):
        seed(time.perf_counter())
        if goodnight:
            good_night_quotes = {}
            for i in webhook_data:
                if i in webhook_quotes:
                    quotes = webhook_quotes[i]
                    for q in quotes:
                        if 'good night' in q.lower():
                            if i in good_night_quotes:
    
                                good_night_quotes[i].append(q) 
                            else:
                                good_night_quotes[i] = [q]

            print('gn quotes', good_night_quotes)      
            print(list(good_night_quotes.keys()))
            chars = choice(list(good_night_quotes.keys()))
            icon_url = webhook_data[chars]
            quote = good_night_quotes[chars][0]
            if len(good_night_quotes[chars]) > 1:
                quote = choice(good_night_quotes[chars])
            return chars, icon_url, quote

        if goodmorning:
            good_morning_quotes = {}
            for i in webhook_data:
                if i in webhook_quotes:
                    quotes = webhook_quotes[i]
                    for q in quotes:
                        if 'good morning' in q.lower():
                            if i in good_morning_quotes:

                                good_morning_quotes[i].append(q) 
                            else:
                                good_morning_quotes[i] = [q]
            
            print('gm quotes', good_morning_quotes)    
            chars = choice(list(good_morning_quotes.keys()))
            icon_url = webhook_data[chars]
            quote = good_morning_quotes[chars][0]

            if len(good_morning_quotes[chars]) > 1:
                quote = choice(good_morning_quotes[chars])
            return chars, icon_url, quote

        chars = choice(list(webhook_data.keys()))
        icon_url = webhook_data[chars]
        quote = choice(webhook_quotes[chars])
        return chars, icon_url, quote
    return None, None, None





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
        
        if message.channel.id == 926478421914173500:

            if message.content.lower() == 'gn' or 'good night' == message.content.lower() or 'goodnight' == message.content.lower():

                char, icon, quote = random_webhook_character(False, True)

                if char == icon == quote:
                    pass
                else:

                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(q_webhook, session=session)
                        await webhook.send(content=quote, username=char, avatar_url=icon)

            if message.content.lower() == 'gm' or 'good morning' == message.content.lower() or 'goodmorning' == message.content.lower():
    
                char, icon, quote = random_webhook_character(True, False)

                if char == icon == quote:
                    pass
                    
                else:

                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(q_webhook, session=session)
                        await webhook.send(content=quote, username=char, avatar_url=icon)
            
            if 'quote' == message.content:
        
                char, icon, quote = random_webhook_character(False, False)

                if char == icon == quote:
                    pass
                else:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(q_webhook, session=session)
                        await webhook.send(content=quote, username=char, avatar_url=icon)

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
