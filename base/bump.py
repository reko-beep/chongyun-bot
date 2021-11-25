from os.path import exists
from os import getcwd,remove

from json import load,dump

from nextcord import Message,Embed,File
from nextcord.utils import get

from core.paimon import Paimon

from asyncio import sleep
from util.logging import logc

class Bump:
    def __init__(self, pmon: Paimon):
        '''
        Initialization
        '''
        self.pmon : Paimon = pmon
        self.file = 'bump.json'

        self.bump_channel = pmon.p_bot_config['bump_channel']
        self.bump_role = None
        if pmon.p_bot_config['bump_role'] != 0:
            self.bump_role = get(pmon.guilds[0].roles,id=pmon.p_bot_config['bump_role'])
        self.timer = pmon.p_bot_config['bump_timer']

        self.bump_data = {}
        self.load_bumps()

        self.disboard_bot_id = 302050872383242240

    async def parse_message_for_bump(self, message: Message):
        '''

        This looks for bump message by disboard, and adds a role to user who bumped it if the role is set!
        also adds a reminder for set time to notify users to bump
        '''
        
        channel_set = (self.bump_channel != 0)

        if channel_set:
            if message.channel.id == self.bump_channel:
                embed_present = (len(message.embeds) != 0)

                if embed_present and (message.author.id == self.disboard_bot_id):
                    
                    embed_description = str(message.embeds[0].description)
                    bumped = ('bump done' in embed_description.lower()) 
                    if bumped:
                        user_id = self.parse_user_id(embed_description)
                        await self.send_bump_success_message(message,user_id)
                        await self.send_bump_schedule_message()
                        self.save_bump(user_id)

                        if self.bump_role:
                            user = get(self.pmon.guilds[0].members,id=int(user_id))
                            await user.add_roles(self.bump_role)

    def get_topbumper(self):
        if len(self.bump_data) != 0:
            return max(self.bump_data, key=self.bump_data.get)

    def save_bump(self, user_id : str):
        '''
        save bump counts to file
        '''

        if user_id in self.bump_data:
            self.bump_data[user_id] += 1
        else:
            self.bump_data[user_id] = 1
        
        if exists(self.file):
            remove(self.file)        
        with open(self.file,'w') as f:
            dump(self.bump_data,f)

    def load_bumps(self):
        '''
        loads bump counts from file
        '''    
        if exists(self.file):
            with open(self.file,'r') as f:
                self.bump_data = load(f)

    def get_bump_counter(self, user_id:str):
        '''
        returns a user bump count if exists
        else none
        '''

        return self.bump_data.get(user_id)




    async def send_bump_success_message(self, message: Message, user_id: str):
        '''
        sends thank you bump message
        '''

        message_channel = message.channel

        embed = Embed(title='Paimon thanks!',description=f'<@!{user_id}> thank you for bumping this server!',color=0xf5e0d0)
        file = File(f'{getcwd()}/guides/paimon/happy.png',filename='happy.png')
        embed.set_thumbnail(url=f'attachment://happy.png')
        await message_channel.send(embed=embed,file=file)

    def parse_user_id(self, message_str: str):
        '''
        gets user id from disboard bump message

        '''
        if '<' in message_str:
            return message_str[message_str.find('<')+1:message_str.find('>')].replace('@','',1).replace('!','',1)

    async def send_bump_schedule_message(self):
        '''
        sends a bump reminder
        '''
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


