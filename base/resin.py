from os import getcwd
from json import dump,load
import threading
import genshinstats as gs

from datetime import date, datetime, timedelta
from threading import Thread
from genshinstats.transactions import current_resin

from nextcord import Embed,TextChannel, Member,  DMChannel
from nextcord.ext.commands import Context
from nextcord.ext import tasks
from nextcord.utils import get
from core.paimon import Paimon
from asyncio import sleep


from PIL import Image
from io import BytesIO
from nextcord import File
from util.logging import log


class Reminder:
    def __init__(self,data: dict, manager, pmon: Paimon, discord_member: Member=None, region: str=None, resin: int=0):
        
        if bool(data):
            self.__dict__ = data  
            self.start_time = datetime.strptime(self.start_time,'%c')
            self.full_time = datetime.strptime(self.full_time,'%c')      

        else:            
            self.discord_id = str(discord_member.id)
            self.region = region
            self.uid = 0
            self.resin = resin
            self.resin_cap = 160
            self.start_time = datetime.now()
            self.full_time: datetime = 0
        self.time_for_one = 0
        self.time_remaining = 0
        self.start = False
        self.full = f'{getcwd()}/assets/resin_full.png'
        self.empty = f'{getcwd()}/assets/resin_empty.png'
        self.manager = manager        
        self.pmon = pmon
        self.guild = self.pmon.guilds[0]  
        self.set_uid()
    
    def get_resin_bar(self):
        resin = self.get_current_resin()
        filled = (resin / 160)
        size = (373,228)
        image = Image.new(mode='RGBA',size=size)        
        empty_bar = Image.open(self.empty,'r')        
        full_bar = Image.open(self.full,'r')
        crop = (0,0,filled*373,228)
        filled_bar = full_bar.crop(box=crop)
        image.paste(empty_bar,(0,0))
        image.paste(filled_bar,(0,0))
        buffer = BytesIO()        
        image.save(buffer,format='PNG')
        buffer.seek(0)
        file = File(buffer, filename='bar.png')
        return file

    def create_full_embed(self, member: Member):
        
        embed = Embed(title=f'Resin Reminder', description='Your resins are full\n no cap!', color=0xf5e0d0)
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png')
        embed.set_author(name=member.display_name,icon_url=member.avatar.url)
        return embed


    def get_remaining_time(self):
        seconds_remaining = ((self.full_time - datetime.now()).seconds)

        new_resin = self.get_current_resin() - self.resin
        
        time_for_next = self.start_time + timedelta(minutes=(new_resin + 1) * 8)

        time_remaining_for_next = time_for_next - datetime.now()





        return str(timedelta(seconds=seconds_remaining)), time_remaining_for_next

    def get_current_resin(self):
        time_now = datetime.now()

        elapsed_time = (time_now - self.start_time).seconds
        minutes = divmod(elapsed_time,60)[0]
        resin_to_add = divmod(minutes,8)[0]

        return self.resin + resin_to_add

    def create_status_embed(self, member: Member):

        resin = self.get_current_resin()         
        file = self.get_resin_bar()
        embed = Embed(title=f'Resin Reminder',description='Resin serves as the energy resource in Genshin Impact. Original Resin is used to claim challenge rewards from Ley Line Blossoms, Petrified Trees (Domains), and Trounce Blossoms (Bosses), as well as Event-exclusive challenges.', color=0xf5e0d0)
        embed.add_field(name='Resin',value=resin)
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png')
        embed.set_author(name=member.display_name,icon_url=member.avatar.url)
        embed.set_image(url=f'attachment://bar.png')
        return embed,file

    def calculate_time_for_full(self):

        remaining_seconds_to_full_resin = (self.resin_cap - self.resin) * 8 * 60

        self.full_time = self.start_time + timedelta(seconds=remaining_seconds_to_full_resin)


    def set_uid(self):
        account = self.manager.get_servers(self.discord_id)
        if account is not None:
            if self.region in account:
                self.uid = account[self.region]


    async def get_resin(self, base_delay:int = 0, base_loop:bool = False):
        if base_loop:
    
            await sleep(base_delay)
            gs.set_cookie(ltuid=self.manager.ltuid,ltoken=self.manager.ltoken)
            resin_data = gs.get_notes(self.uid)

            # todo: check if resin is emptied

            if resin_data['resin'] != self.resin:
            
                self.calculate_time_for_full()

                #loop starts here
                await self.send_filled_message()
            else:
                await self.get_resin(60*60,True)
        else:

            gs.set_cookie(ltuid=self.manager.ltuid,ltoken=self.manager.ltoken)
            resin_data = gs.get_notes(self.uid)

            self.resin = resin_data['resin']

            
            
            self.calculate_time_for_full()

            #loop starts here
            await self.send_filled_message()


    async def set_resin(self, resin: int, base_delay: int=0, base_loop:bool=False):
        if base_loop:
            log('Reminder reset','stats in ',base_delay,' seconds')
            await sleep(base_delay)        
            
        if self.resin >= 0 and self.resin < 160:
            self.resin = resin
                
            self.calculate_time_for_full()
            self.save()
            
            if self.notifier.is_running():
                self.notifier.cancel()
            
            self.notifier.change_interval(seconds=((self.full_time-self.start_time).seconds))
            self.notifier.start()
               

            

    @tasks.loop()
    async def notifier(self):
        if self.start == True:
            member = get(self.guild.members,id=int(self.discord_id))
            if member is not None:
                if member.dm_channel is None:
                    dm = await member.create_dm()
                else:
                    dm = member.dm_channel
                embed = self.create_full_embed(member)
                embed.set_footer(text='Please write time after which you want to counter to restart!')
                msg = await dm.send(embed=embed)

                def check(message):
                    return isinstance(message.channel,DMChannel) and message.author.id == member.id
                m = await self.pmon.wait_for('message',check=check)
                hour = 0
                minute = 0
                second = 0
                if 'h' in m.content:
                    hour = m.content.split('h')[0]
                if 'm' in m.content:
                    minute = m.content.split('m')[0]
                    if 'h' in minute:
                        minute = minute.split('h')[1]
                if 's' in m.content:
                    second = m.content.split('s')[0]
                    if 'm' in second:
                        second = second.split('m')[1]
                start_second = (datetime.now() + timedelta(hours=int(hour),minutes=int(minute),seconds=int(second)) - (datetime.now())).seconds
                embed = Embed(title='Resin reminder',description=f'Resin will reset to 0, reminder will start in {hour} hr, {minute} minute(s), {second} second(s)',
                color=0xf5e0d0)
                embed.set_author(name=member.display_name,icon_url=member.avatar.url)
                await dm.send(embed=embed)
                await self.manager.add_resin_reminder(member, self.region, 0, None, True, start_second)
                self.notifier.cancel()
        else:
            self.start = True
            log('Loop started','will notify in ',((self.full_time-self.start_time).seconds))
            
        

            


    def save(self):
        data_save = {}
            
        for key in self.__dict__:
            if key in ['start_time', 'full_time']:
                data_save[key] = datetime.strftime(self.__dict__[key],'%c')
            else:
                if key in ['discord_id','region','resin','resin_cap','full','empty','start']:
                    data_save[key] = self.__dict__[key]

        with open(f'{getcwd()}/assets/resin/{self.discord_id}_{self.region}.json','w') as f:
            dump(data_save,f,indent=1)

async def reminder_set(data: dict, manager, pmon: Paimon, discord_member: Member=None, region: str=None, resin: int=0, ctx: Context = None, base_loop: bool = False, base_delay: int = 0):
    remind = Reminder(data, manager, pmon, discord_member, region, resin)
    if ctx is not None:
        await ctx.send('Resin reminder setup!')
    log('created resin reminder for',remind.discord_id,'resin',remind.resin)
    await remind.set_resin(remind.resin,base_delay,base_loop)    
    
    return remind




