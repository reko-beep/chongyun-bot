from os.path import exists
from os import getcwd,remove

from json import load,dump

from nextcord import Message,Embed,File
from nextcord.utils import get

from core.paimon import Paimon

from asyncio import sleep


class Bump:
    def __init__(self, pmon: Paimon):
        self.pmon : Paimon = pmon
        self.file = 'bump.json'

        self.bump_channel = pmon.p_bot_config['bump_channel']
        self.bump_role = None
        if pmon.p_bot_config['bump_role'] != 0:
            self.bump_role = get(pmon.guilds[0].roles,id=pmon.p_bot_config['bump_role'])
        self.timer = pmon.p_bot_config['bump_timer']

        self.bump_data = {}
        self.load_bemps()

        self.disboard_bot_id = 302050872383242240

    async def parse_message_for_bump(self, message: Message):

        embed_present = (len(message.embeds) != 0)

        if embed_present:
            
            embed_description = message.embeds[0].description
            bumped = ('Bump Done' in embed_description) and (message.author.id == self.disboard_bot_id)
            if bumped:
                user_id = self.parse_user_id(embed_description)
                await self.send_bump_success_message(message,user_id)
                await self.send_bump_schedule_message(message)

    def save_bump(self, user_id : str):

        if user_id in self.bump_data:
            self.bump_data[user_id] += 1
        else:
            self.bump_data[user_id] = 1
        
        if exists(self.file):
            remove(self.file)        
        with open(self.file,'w') as f:
            dump(self.bump_data,f)

    def load_bumps(self):
        if exists(self.file):
            remove(self.file)        
        with open(self.file,'w') as f:
            self.bump_data = dump(f)

    def get_bump_counter(self, user_id:str):

        return self.bump_data.get(user_id)




    async def send_bump_success_message(self, message: Message, user_id: str):

        message_channel = message.channel

        embed = Embed(title='Paimon thanks!',description=f'<@!{user_id}> thank you for bumping this server!',color=0xf5e0d0)
        file = File(f'{getcwd()}/guides/paimon/happy.png',filename='happy.png')
        embed.set_thumbnail(url=f'attachment://happy.png')
        await message_channel.send(embed=embed,file=file)

    def parse_user_id(self, message_str: str):
        if '<' in message_str:
            return message_str[message_str.find('<')+1:message_str.find('>')]

    async def send_bump_schedule_message(self, message: Message):
        await sleep(self.timer) 

        text = 'Is someone available to bump the server? '
        embed = Embed(title='Please Bump!',description=text,color=0xf5e0d0)
        embed.set_thumbnail(url=f'{self.pmon.user.avatar.url}')
        channel = await self.pmon.fetch_channel(self.bump_channel)

        if self.bump_role:
            await channel.send(f'{self.bump_role.mention}',embed=embed)
            print('bump message sent')
        else:
            await channel.send(embed=embed)
            print('bump message sent')


