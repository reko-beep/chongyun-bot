import os
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import asyncio

class GenshinSoundBoard:
    def __init__(self,bot):
        self.bot = bot
        self.path = os.getcwd()
        self.oi = f'{self.path}/soundboard/oi.mp3'
        self.laughter = f'{self.path}/soundboard/laughter.mp3'
        self.thinking = f'{self.path}/soundboard/thinking.mp3'
        self.ehenandayo = f'{self.path}/soundboard/ehenandayo.mp3'
        self.files = {'1':{'Oi':self.oi},'2':{'Laugh':self.laughter},'3':{'Think':self.thinking},'4':{'Eh Nandayo':self.ehenandayo}}
        pass

    def numoji(self,num):        
        n = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        return n[num]

    def num(self,j):
        z = 0
        noj = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i in noj:
            if j == i:
                return z
            else:
                z += 1


    def get_file(self,num: str):
        if num in ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']:
            num = str(self.num(num))
        if num in self.files:
            key_ = list(self.files[num].keys())[0]
            print(self.files[num][key_])
            return self.files[num][key_]
    
    def get_title(self, num:str):
        if num in ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']:
            num = str(self.num(num))
        if num in self.files:
            key = list(self.files[num].keys())[0]
            print(list(self.files[num].keys()))
            print(list(self.files[num].keys())[0])
            return key
        



    def create_embed(self):        
        descript_ = ''
        emojis = []
        for i in self.files:
            descript_ += f'{self.numoji(int(i))} : **{self.get_title(i)}**\n'
            emojis.append(self.numoji(int(i)))
        embed = discord.Embed(title='Paimon Soundboard',description=f'Paimon its me~\nreact to one and I will bless you with my voice\n\n{descript_}',color=0xf5e0d0)
        file = discord.File(f'{self.path}/guides/paimon/happy.png',filename='happy.png')
        embed.set_thumbnail(url=f'attachment://happy.png')
        return embed,file,emojis


    async def play_file(self, ctx: commands.Context,num:str):
        path_= os.getcwd()+'/ffmpeg.exe'
        file_ = self.get_file(num)
        print('Playing',file_)
        src = discord.FFmpegPCMAudio(file_,executable='ffmpeg')       
        if ctx.voice_client is not None:
            c_ = ctx.voice_client            
            c_.play(src, after=None)
            await asyncio.sleep(15)
            await ctx.voice_client.disconnect()
        else:
            connected = ctx.author.voice
            if connected:
                await connected.channel.connect()
                c_ = ctx.voice_client                
                c_.play(src, after=None)
                await asyncio.sleep(15)
                await ctx.voice_client.disconnect()
            else:
                embed = discord.Embed(title='Hufff!',description=f"I can't sound dumb now, can I!\n You are not in a vc!",color=0xf5e0d0)
                file = discord.File(f'{self.path}/guides/paimon/angry.png',filename='angry.png')
                embed.set_thumbnail(url=f'attachment://angry.png')
                await ctx.send(embed=embed,file=file)
   


