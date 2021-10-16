import json
import os 

from asyncio import TimeoutError, sleep

import nextcord as discord
from nextcord.ext import commands, tasks



from base.lobby import Lobby
from base.events import GenshinEvents
from base.quests import GenshinQuests
from base.quotes import GenshinQuotes
from base.database import GenshinDB
from base.soundboard import GenshinSoundBoard
from base.guides import GenshinGuides
from base.scraper import search_page,unpack_anime

from core.paimon import Paimon




from core.paimon import Paimon


# client: Bot and paimon: Paimon (subclass of Bot) are same
pmon = Paimon(config_file="settings.json")
client = pmon
settings_data = pmon.get_config()



data = {}

guides_ = GenshinGuides()
soundboard = GenshinSoundBoard(client)
db = GenshinDB()
quotes_ = GenshinQuotes()
events_handler = GenshinEvents(client)
voice_handler = Lobby(client)
quests_handler = GenshinQuests()


class AssignRole:
    def __init__(self):
        self.role = settings_data['approve_role']
mod_role = settings_data['mod_role']
announce_channel = settings_data['announce_channel']
starter_channel = settings_data['verify_channel']
dropuidchannel = settings_data['dropuid_channel']
eventchannel = settings_data['events_channel']
assignrole = AssignRole()
approverole = settings_data['approve_role']
scrutinyrole = settings_data['scrutiny_role']
bumpchannel = settings_data['bump_channel']
lobbycreatevc = settings_data['lobbycreatevc']
@client.command(aliases=['b'])
async def builds(ctx, character_name: str):
    option = 'bd'
    if character_name != "":
        if option != "":            
            stop = False
            ps = 0
            embeds,files = guides_.create_embeds(character_name,option)
            if len(embeds) > 1:
                for embed in range(0,len(embeds),1):            
                    embeds[embed].set_author(name=f'{ctx.author.display_name}',url=f'{ctx.author.avatar.url}')
                    await ctx.send(embed=embeds[embed],file=files[embed])
            else:
                embeds[0].set_author(name=f'{ctx.author.display_name}',url=f'{ctx.author.avatar.url}')
                await ctx.send(embed=embeds[0],file=files[0])                         
        else:
            embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~')
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~')
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

@client.command()
@commands.has_any_role(mod_role)
async def dc(ctx):
    channel = client.get_channel(announce_channel)
    embed = discord.Embed(title='Paimon is going!',description=f'Sorry travellers I will be back soon!',color=0xf5e0d0)
    file = discord.File(f'{os.getcwd()}/guides/paimon/sorry.png',filename='sorry.png')
    embed.set_thumbnail(url=f'attachment://sorry.png')
    await channel.send(embed=embed,file=file)
    await client.close()

@client.command(aliases=['map'])
async def map_(ctx):    
    embed = discord.Embed(title='Genshin Impact Map!',description=f'Where you going traveller? hmmmm~',color=0xf5e0d0)
    file_map = discord.File(f'{os.getcwd()}/guides/Map/map.jpg',filename='map.jpg')
    file_paimon = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
    embed.set_thumbnail(url=f'attachment://happy.png')
    embed.set_image(url=f'attachment://map.jpg')
    await ctx.send(embed=embed,files=[file_map,file_paimon])
   


@client.command(aliases=['as'])
async def ascension(ctx, character_name: str):
    option = 'ast'
    if character_name != "":
        if option != "":
            stop = False            
            ps = 0
            embeds,files = guides_.create_embeds(character_name,option)
            print(embeds,files)            
            if len(embeds) > 1:                
                for embed in range(0,len(embeds),1):            
                    embeds[embed].set_author(name=f'{ctx.author.display_name}',url=f'{ctx.author.avatar.url}')
                    await ctx.send(embed=embeds[embed],file=files[embed])
            else:
                embeds[0].set_author(name=f'{ctx.author.display_name}',url=f'{ctx.author.avatar.url}')
                await ctx.send(embed=embeds[0],file=files[0])             
                         
        else:
            embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~')
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~')
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

@client.command()
@commands.has_any_role(mod_role)
async def scrutiny(ctx,arg):
    if arg == 'on':
        assignrole.role = scrutinyrole
        print(assignrole)
        await ctx.send(f"Members scrutiny turned on!")
    if arg == 'off':
        assignrole.role = approverole
        await ctx.send('Members scrutiny turned off!')

@client.event
async def on_member_join(member):
    role = member.guild.get_role(assignrole.role)
    print('Assigned Role',role)
    await member.add_roles(role)
    if assignrole.role == scrutinyrole:
        channel = client.get_channel(starter_channel)
        embed = discord.Embed(title=f' Paimon wants to know something!',description=f'{member.mention} Please tell me \n **Where did you find the server on?**\n**From which country you are from?**',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
        embed.set_thumbnail(url=f'attachment://happy.png')
        embed.set_footer(text='if you dont find any guide, please contact archons! or you can provide them to archon to add it!')
        await channel.send(embed=embed,file=file)

@client.command()
@commands.has_any_role(mod_role)
async def approve(ctx, member: discord.Member=None):
    if member != None:
        await member.edit(roles=[])
        role = ctx.guild.get_role(approverole)
        print(role)
        await member.add_roles(role)
        await ctx.send(f"{member} have been approved")
    else:
        await ctx.send("Hmpfh, please mention a user?")


@client.command(aliases=['gs','gstats'])
async def genshinstats(ctx, arg:str):
    print(ctx.author.id)
    uid = db.get_uid(str(ctx.author.id),arg)
    print(uid)
    if arg != "":
        if uid != None:
            data = db.get_uiddata(uid)
            print(data)
            if data != None:            
                embed = db.create_stats_embed(data)
                if embed != None:
                    embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Paimon is going!',description=f'Sorry traveller, You have not made your data public!',color=0xf5e0d0)
                file = discord.File(f'{os.getcwd()}/guides/paimon/sorry.png',filename='sorry.png')
                embed.set_thumbnail(url=f'attachment://sorry.png')
                await ctx.send(embed=embed,file=file)
        else:
            embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\ndrop ur uid as server_name:uid\nexample **eu:9566512**\njust write the id in #drop-your-uid',color=0xf5e0d0)
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n Which server~\n I will eat you!',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

@client.command(aliases=['gc'])
async def gcharacters(ctx,arg:str):
    print(ctx.author.id)
    uid = db.get_uid(str(ctx.author.id),arg)
    print(uid)
    if arg != "":
        if uid != None:
            data = db.get_uiddata(uid)
            embeds,emojis = db.create_characters_embed(data)
            print(embeds)
            count = len(embeds)-1
            select = 0
            stop = False            
            if len(embeds) > 1:
                embeds[str(select)]['character'].set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
                msg = await ctx.send(embed=embeds[str(select)]['character'])
                for i in emojis:
                    await msg.add_reaction(i)
                while stop == False:
                    try:
                        def check(reaction,user):
                            return reaction.message.id == msg.id and user == ctx.author
                        reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)
                    except TimeoutError:
                        await msg.clear_reactions()
                    else:                    
                        if reaction.emoji in emojis:
                            if reaction.emoji == '⚔️':
                                await msg.edit(embed=embeds[str(select)]['weapon'])
                            if reaction.emoji == '➡️':
                                if select < count:
                                    select += 1
                                    await msg.edit(embed=embeds[str(select)]['character'])                           
                            if reaction.emoji == '⬅️':
                                if select >= 1:
                                    select -= 1
                                    await msg.edit(embed=embeds[str(select)]['character'])
            else:
                embeds['0']['character'].set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar.url)
                msg = await ctx.send(embed=embeds[str(select)]['character'])
                while stop == False:
                    try:
                        def check(reaction,user):
                            return reaction.message.id == msg.id and user == ctx.author
                        reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)
                    except TimeoutError:
                        await msg.clear_reactions()
                    else:                    
                        if reaction.emoji in emojis:
                            if reaction.emoji == '⚔️':
                                await msg.edit(embed=embeds['0']['weapon'])
        else:                                   
            embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\ndrop ur uid as server_name:uid\nexample **eu:9566512**\njust write the id in #drop-your-uid',color=0xf5e0d0)
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n Which server~\n I will eat you!',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)


@client.command(aliases=['ev'])
async def events(ctx,arg:str):
    if arg != '':
        events_ = events_handler.fetch(arg)
        if 'last_id' in events_:
            events_.pop('last_id')
        if len(events_) > 1:
            for i in events_:
                embed,file = events_handler.create_embed(events_[i])
                await ctx.send(embed=embed,file=file)
                await sleep(5)
        else:
            embed = discord.Embed(title='Paimon is angry!',description=f'What do you wa- want, huh~\n {arg.capitalize()} events are already posted!\n\n',color=0xf5e0d0)
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n I will eat you!',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

@tasks.loop(hours=6)
async def events():
    if eventchannel != 0:
        channel_ev = client.get_channel(eventchannel)
        events_ = events_handler.fetch('upcoming')
        if len(events_) > 2:
            print(f'New Events found {events_}')
            for i in events_:
                embed,file = events_handler.create_embed(events_[i])
                await channel_ev.send(embed=embed,file=file)
                await sleep(5)
        else:
            print('No New events found!')



@client.command(aliases=['psb','psoundboard'])
async def paimonsoundboard(ctx):
    embed,file,emojis = soundboard.create_embed()
    msg = await ctx.send(embed=embed,file=file)
    for i in emojis:
        await msg.add_reaction(i)
    try:
        def check(reaction,user):        
            return reaction.message.id == msg.id and user.id == ctx.author.id
        reaction,user = await client.wait_for('reaction_add',check=check,timeout=60)    
    except TimeoutError:
        await msg.clear_reactions()
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)
    else:
        if reaction.emoji in emojis:
            print(reaction.emoji)
            title = soundboard.get_title(reaction.emoji)
            print(title)
            embed.set_footer(text=f'Paimon playing {title} now!')
            await msg.edit(embed=embed)
            await soundboard.play_file(ctx,reaction.emoji)
            await msg.clear_reactions()

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


@client.command(aliases=['gserv'])
async def gservers(ctx):
    id_ = str(ctx.author.id)
    servers  = db.get_servers(id_)
    if servers != None:
        serv_ = ''
        for i in servers:
            serv_ += f'**{i.upper()}**\nUID: {servers[i]}\n\n'
        embed = discord.Embed(title=f'{ctx.author.display_name} Genshin Impact Servers', description=f'\n{serv_}',color=0xf5e0d0)    
        embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar.url}')
        file_paimon = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
        embed.set_thumbnail(url=f'attachment://happy.png')            
        await ctx.send(embed=embed,file=file_paimon)
    else:        
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n please link the id!',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

@client.command(aliases=['gl'])
async def glink(ctx,server:str,uid:str):
    id_ = str(ctx.author.id)
    if server != '':
        if uid != '':
            if uid.isdigit():
                link = f'{server.lstrip().rstrip().lower()}:{uid.lstrip().rstrip()}'
                db.serveruid(id_,link)
                embed = discord.Embed(title=f'{ctx.author.display_name} Genshin Impact profile link!', description=f'\n Your uid {uid} linked with region **{server.upper()}**',color=0xf5e0d0)    
                embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar.url}')
                file_paimon = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
                embed.set_thumbnail(url=f'attachment://happy.png')            
                await ctx.send(embed=embed,file=file_paimon)
            else:
                embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n **UID must be digits**!',color=0xf5e0d0)
                file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')
        else:
            embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n **You have not written UID**',color=0xf5e0d0)
            file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
            embed.set_thumbnail(url=f'attachment://angry.png')
            await ctx.send(embed=embed,file=file)
    else:
        embed = discord.Embed(title='Paimon is angry!',description='What do you wa- want, huh~\n **Please write the region: eu, asia, na**',color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/angry.png',filename='angry.png')
        embed.set_thumbnail(url=f'attachment://angry.png')
        await ctx.send(embed=embed,file=file)

  
        


@client.command(aliases=["anim"])
async def anime(ctx, *,arg:str):
    arg = ''.join(arg)
    print(arg)
    if arg != "":
        s,url = search_page(arg)
        if s != None:
            data = unpack_anime(s)
            if len(data) > 0:
                show = ['english', 'japanese','genres','type', 'source', 'synopsis', 'episodes', 'status', 'aired',
                            'season', 'genres', 'duration', 'rating',
                            'score', 'popularity']
                count = 5
                pages = len(show) / count
                if isinstance(pages, float):
                    pages += 1
                    pages = int(pages)
                page_embed = []
                print(data)
                for page in range(1, pages + 1, 1):
                    emb = discord.Embed(title=data['title'], description=f"[Link to {data['title']}]({url})",color=0xf5e0d0)      
                    for i in range(0, len(show) - 1, 1):                            
                        if ((page * count) - 6) < i < ((page * count)):
                            print(i)
                            k_ = show[i]                                
                            print(k_)
                            v = ''
                            if k_ in data:                                
                                print(f"Item {k_} added!")
                                print("List:", type(data[k_]) is list)
                                if type(data[k_]) is list:
                                    if len(data[k_]) > 1:
                                        v = ','.join(data[k_])
                                    else:
                                        v = ''.join(data[k_])
                                    emb.add_field(name=f"{k_.capitalize()}", value=f"{v}", inline=True)
                                else:
                                    if k_ == 'synopsis':
                                        v = data[k_][:495] + "..."
                                        emb.add_field(name=f"{k_.capitalize()}", value=f"{v}", inline=False)
                                    else:
                                        v = data[k_]
                                        emb.add_field(name=f"{k_.capitalize()}", value=f"{v}", inline=True)
                            print(v)
                    emb.set_thumbnail(url=data['images']['sd'])
                    page_embed.append(emb)
                if len(page_embed) > 0:
                    ps = 0
                    stop = False
                    help = await ctx.send(embed=page_embed[0])
                    await help.add_reaction('⬅')
                    await help.add_reaction('➡')
                    await help.add_reaction('🟥')

                    def check(reaction, user):
                        return reaction.message.channel == ctx.channel and user == ctx.author

                    while stop == False:
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=30, check=check)
                        except TimeoutError:
                            await help.clear_reaction('⬅')
                            await help.clear_reaction('➡')
                            await help.clear_reaction('🟥')
                            return None
                        else:
                            if reaction.emoji == '⬅':
                                if ps > 0:
                                    # print(ps)
                                    ps -= 1
                                    await help.edit(embed=page_embed[ps])
                            if reaction.emoji == '➡':
                                if ps < len(page_embed) - 1:
                                    ps += 1
                                    # print(ps)
                                    await help.edit(embed=page_embed[ps])
                            if reaction.emoji == '🟥':
                                await help.clear_reaction('⬅')
                                await help.clear_reaction('➡')
                                await help.clear_reaction('🟥')
                                stop = True         

@client.event
async def on_voice_state_update(member,before,after):
    vc = member.voice
    if vc:
        if lobbycreatevc != 0:
            if vc.channel.id == lobbycreatevc:    
                check,vc_ = await voice_handler.create_vc(member)
                if check != None:
                    await member.move_to(vc_)
    channel = before.channel   
    await voice_handler.voice_remove(channel)
    
    

@client.command(aliases=['la','lallow'])
async def lobbyallow(ctx, member:discord.Member=None):
    if member != None:
        success = await voice_handler.allow_member(ctx.author,member)
        if success == None:
            await ctx.send(f'You dont own a lobby!')
        else:
            if success == False:
                await ctx.send(f"You don't own a lobby!")
            else:
                if success:
                    await ctx.send(f"{member.name} can now join <#{success.id}>")

@client.command(aliases=['lk','lkick'])
async def lobbykick(ctx, member:discord.Member=None):   
    success = await voice_handler.kick_member(ctx.author,member)
    if success == None:
        await ctx.send(f'You dont own a lobby!')
    else:
        if success == False:
            await ctx.send(f"Either the user is not in vc or Please mention a member!")
        else:
            if success:
                await ctx.send(f"{member.name} can now join <#{success.id}>")

@client.command(aliases=['lua','lunallow'])
async def lobbyunallow(ctx, member:discord.Member=None):   
    success = await voice_handler.unallow_member(ctx.author,member)
    if success == None:
        await ctx.send(f'You dont own a lobby!')
    else:
        if success == False:
            await ctx.send(f"Either the user is not in vc or Please mention a member!")
        else:
            if success:
                await ctx.send(f"{member.name} can now join <#{success.id}>")

@client.command(aliases=['ll','llimit'])
async def lobbylimit(ctx, limit : int):
    success,channel_ = await voice_handler.limit_vc(ctx.author,limit)   
    print(channel_)
    if success == True:
        if limit == 0:
            await ctx.send(f'<#{channel_.id}> limit removed')
        else:
            await ctx.send(f'<#{channel_.id}> limited to {limit} members!')
    else:
        await ctx.send(f'You dont own a lobby!')

@client.command(aliases=['llock'])
async def lobbylock(ctx):
    success,channel = await voice_handler.lock_vc(ctx.author)   
    if success == True:        
        await ctx.send(f'<#{channel.id} now locked!')
    else:
        await ctx.send(f'You dont own a lobby!')

@client.command(aliases=['lul','lunlock'])
async def lobbyunlock(ctx):
    success,channel_ = await voice_handler.unlock_vc(ctx.author)   
    if success == True:        
        await ctx.send(f'<#{channel_.id} now public!')
    else:
        await ctx.send(f'You dont own a lobby!')


@client.command(aliases=['lc','lcreate'])
async def lobbycreate(ctx):    
    success,channel_ =  await voice_handler.create_vc(ctx.author)
    if success != None and channel_ != None:
        await ctx.send(f'{channel_.name} created!')
    else:
        await ctx.send(f'You are already owner of an channel!')
    
@client.event
async def on_message(message):
    if message.channel.id == dropuidchannel:
        author_ = str(message.author.id)
        db.serveruid(author_,message.content)
    if bumpchannel != 0:
        if message.channel.id == bumpchannel:
            if len(message.embeds) != 0 and message.author.id == 302050872383242240:
                embed = message.embeds[0]
                print(embed.description)
                mention_ = embed.description[:embed.description.find('>')+1]
                print(mention_)
                if 'Bump done!' in embed.description:
                    embed = discord.Embed(title='Paimon thanks!',description=f'{mention_} thank you for bumping this server!',color=0xf5e0d0)
                    file = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
                    embed.set_thumbnail(url=f'attachment://happy.png')
                    await message.channel.send(embed=embed,file=file)
                
    await client.process_commands(message)

@client.command()
async def quest(ctx,*,arg:str=''):
    str_ = ''.join(arg)
    stop = False
    select = 0
    embeds,emojis = quests_handler.create_quest_embed(str_)
    count = len(embeds)
    msg = await ctx.send(embed=embeds[0])
    for i in emojis:
        await msg.add_reaction(i)
    while stop == False:
        try:
            def check(reaction,user):
                return reaction.message.id == msg.id and user == ctx.author
            reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)
        except TimeoutError:
            await msg.clear_reactions()
        else:                    
            if reaction.emoji in emojis:                
                if reaction.emoji == '➡️':
                    if select < count-1:
                        select += 1
                        await msg.edit(embed=embeds[select])                           
                if reaction.emoji == '⬅️':
                    if select >= 1:
                        select -= 1
                        await msg.edit(embed=embeds[select])
@client.command()
async def chapter(ctx,*,arg:str=''):
    str_ = ''.join(arg)
    stop = False
    select = 0
    embeds,emojis = quests_handler.create_chapter_embeds(str_)
    count = len(embeds)
    msg = await ctx.send(embed=embeds[0])
    for i in emojis:
        await msg.add_reaction(i)
    while stop == False:
        try:
            def check(reaction,user):
                return reaction.message.id == msg.id and user == ctx.author
            reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)
        except TimeoutError:
            await msg.clear_reactions()
        else:                    
            if reaction.emoji in emojis:                
                if reaction.emoji == '➡️':
                    if select < count-1:
                        select += 1
                        await msg.edit(embed=embeds[select])                           
                if reaction.emoji == '⬅️':
                    if select >= 1:
                        select -= 1
                        await msg.edit(embed=embeds[select])

@client.command()
async def act(ctx,*,arg:str=''):
    str_ = ''.join(arg)
    stop = False
    select = 0
    embeds,emojis = quests_handler.create_acts_embeds(str_)
    count = len(embeds)
    msg = await ctx.send(embed=embeds[0])
    for i in emojis:
        await msg.add_reaction(i)
    while stop == False:
        try:
            def check(reaction,user):
                return reaction.message.id == msg.id and user == ctx.author
            reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)
        except TimeoutError:
            await msg.clear_reactions()
        else:                    
            if reaction.emoji in emojis:                
                if reaction.emoji == '➡️':
                    if select < count-1:
                        select += 1
                        await msg.edit(embed=embeds[select])                           
                if reaction.emoji == '⬅️':
                    if select >= 1:
                        select -= 1
                        await msg.edit(embed=embeds[select])


@client.event
async def on_ready():
    channel = client.get_channel(announce_channel)
    events.start()
    voice_handler.set_guild(client.guilds[0])
    """
    
    embed = discord.Embed(title='Paimon is live!',description=f'Hello tra-travel-traveller!\n Paimon is here!',color=0xf5e0d0)
    file = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')
    embed.set_thumbnail(url=f'attachment://happy.png')
    await channel.send(embed=embed,file=file)
    """
    announce_data = {}
    if os.path.exists('announcement.json'):
        with open('announcement.json','r') as f:
            announce_data = json.load(f)
    if announce_data['announce'] == 'true':
        embed = discord.Embed.from_dict(announce_data['embed'])   
        await channel.send(embed=embed)   
    
    


    
pmon.p_start()