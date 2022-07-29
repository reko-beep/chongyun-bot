from calendar import c
from datetime import datetime, timedelta
from json import load, dump
from time import strptime
from nextcord.ext import tasks
from nextcord import Member, Embed, HTTPException, Forbidden, Guild
from nextcord.utils import get
from os import getcwd
from os.path import exists
from base.commstime import get_resettimes, get_remaining_time, get_in_str, get_times

class Reminders:
    def __init__(self, bot) -> None:
        self.reminders = {

        }
        self.bot = bot

        self.resm = self.bot.resource_manager
        self.path = self.bot.resource_manager.db.format(path='reminders.json')
        self.loaded = False
        self.wallpapers = []
        self.load_wallpapers()

    def load_wallpapers(self):
        self.wallpapers = ['https://cdn-cf-east.streamable.com/image/tr1iof.jpg']
        path = self.resm.genpath('data', 'chongyun_wallpapers.json')

        with open(path, 'r') as f:
            self.wallpapers += load(f)['data']


    def load_reminders(self):
        remind_data = {}
        if exists(self.path):

            with open(self.path, 'r') as f:
                remind_data = load(f)

        if len(remind_data) != 0 and not self.loaded:
            for member_id in remind_data:

                reminders = remind_data[member_id]                
                if member_id not in self.reminders:
                    self.reminders[member_id] = {}

                for type_ in reminders:
                    for region in reminders[type_]:

                        if type_ not in self.reminders[member_id]:
                            self.reminders[member_id][type_] = {}

                        reminder = reminders[type_][region]
                        self.reminders[member_id][type_][region] = Reminder(self.bot, reminder['guild'],reminder['type'], reminder['start_time'], reminder['max_value_time'], reminder['member'], reminder['region'], reminder['uid'], reminder['value'], reminder['max_value'])
            self.loaded = True

    def save_reminders(self):

        save_data = {

        }
        for member in self.reminders:
            reminders = self.reminders[member]
            if member not in save_data:
                save_data[member]= {}
            for type_ in reminders:  

                if type_ not in save_data[member]:
                    save_data[member][type_] = {}

                for region in reminders[type_]:         
                    save_data[member][type_][region] = reminders[type_][region].to_dict

        with open(self.path, 'w') as f:
                dump(save_data, f, indent=1)  

    def add_reminder(self, guild: Guild, type_: str, member : Member, region: str, uid: int, value: int, max_value: int=-1):
        member_id = str(member.id)
        if member_id not in self.reminders:
            self.reminders[member_id] = {}
        if type_ not in self.reminders[member_id]:
            self.reminders[member_id][type_] = {}
        
        self.reminders[member_id][type_][region] : Reminder = Reminder(self.bot, guild, type_, datetime.now(), None, member, region, uid, value)
        self.save_reminders()
        return self.reminders[member_id][type_][region]

    def remove_reminder(self, type_: str, member: Member, region: str):
        member_id = str(member.id)
        if member_id  not in self.reminders:
            return False
        if type_ in self.reminders[member_id]:
            if region in self.reminders[member_id][type_]:
                self.reminders[member_id][type_][region].stopr()
                self.reminders[member_id][type_].pop(region)
                self.save_reminders()
                return True

    def get_reminders(self, member: Member, type_: str = ''):

        embeds = []
        member_id = str(member.id)
        reminders = self.reminders[member_id] if member_id in self.reminders else None
        if reminders is not None:
            if type_ in reminders:                 
                 for rem in reminders[type_]:
                        region = rem
                        embed = reminders[type_][rem].create_status_embed()
                        embeds.append(embed)
            else:
                if type_ == '':
                    for type__ in reminders:
                        for rem in reminders[type__]:
                            region = rem
                            embed = reminders[type__][rem].create_status_embed()
                            embeds.append(embed)

        
        return None if len(embeds) == 0 else embeds
                        



class Reminder:
    def __init__(self,bot, guild: Guild,  type_: str, current_time: datetime, max_value_time:datetime, discord_member: Member, region:str, uid: int, value:int,  max_value: int = -1, ) -> None:
        self.type = type_
        self.member = discord_member
        self.value = value
        self.max_value = self.get_max_value() if max_value == -1 else max_value
        self.start_time = current_time
        self.max_value_time = max_value_time
        self.region = region
        self.uid = uid
        self.bot = bot
        self.guild = guild
        self.general_channel = self.bot.b_config.get('general_channel', None)
        self.comm_reset = self.bot.b_config.get('comm_reset_hr', 1)
        self.resin_msg = False
        self.com_counter = 0
        self.com_max = 0
        self.load_values()
        print('max time init', self.max_value_time)
        if self.max_value_time is None:
            self.get_max_time()
        self.set_reminder_interval()
    
    @tasks.loop()
    async def reminder_setup(self):
        if self.type == 'resin':    
            if self.resin_msg == True:        
                dm = self.member.dm_channel
                if dm is None:
                    dm = await self.member.create_dm()
                
                embed = Embed(title='Resin Reminder', description=f"Region: **{self.region.upper()}**\nYour resin has been capped")
                embed.set_author(name=self.member.name, icon_url=self.member.display_avatar.url)
                try:
                    await dm.send(embed=embed)
                except HTTPException or Forbidden:
                    if self.general_channel is not None:
                        await self.general_channel.send(self.member.mention, embed=embed)
                self.max_value = 9999
                self.reminder_setup.cancel()

            if self.resin_msg == False:
                self.resin_msg = True
                

        if self.type == 'comms':        

            if self.com_counter < self.com_max:   
                dm = self.member.dm_channel
                if dm is None:
                    dm = await self.member.create_dm()
                
                embed = Embed(title='Commission Reminder', description=f'Region: **{self.region.upper()}**\nYou have {self.status} left to do ur commissions')
                embed.set_author(name=self.member.name, icon_url=self.member.display_avatar.url)

                try:
                    await dm.send(embed=embed)
                except HTTPException or Forbidden:
                    if self.general_channel is not None:
                        await self.general_channel.send(self.member.mention, embed=embed)
                self.com_counter += 1

                print(self.com_max, self.com_counter)
            else:
                self.get_max_time()
                self.set_reminder_interval()

        

    def get_max_value(self):
        if self.type == 'resin':
            return 160
        if self.type == 'comms':
            return 4
    
    def get_resin_value(self):
        if self.type == 'resin':

            if self.max_value_time is None:
                self.get_max_time()
            if self.max_value_time > datetime.now():
                return self.value + int(((datetime.now()-self.start_time).total_seconds() // 60)// 8)
            else:
                self.max_value

    def get_max_time(self):
        
        if self.type == 'resin':
            if self.max_value_time == None:
               minutes_to_full = (self.max_value-self.value) * 8
               self.max_value_time = self.start_time + timedelta(minutes=minutes_to_full)
            
        if self.type == 'comms':
            self.max_value_time = get_resettimes(1,self.region)
            

    def get_time_to_max(self):

        if self.type == 'resin':
    
            if self.max_value_time is None:
                self.get_max_time()
            
            if self.max_value_time > self.start_time:
                return (self.max_value_time-self.start_time).total_seconds() 
        

        if self.type == 'comms':

            if self.max_value_time is None:
                self.get_max_time()
            

            if self.max_value_time > self.start_time:
                return (self.max_value_time-self.start_time).total_seconds() 
            
                    

    def set_reminder_interval(self):

        if self.type == 'resin':

            if self.reminder_setup.is_running():
                self.reminder_setup.cancel()
            
            self.reminder_setup.change_interval(seconds=((self.max_value_time-self.start_time).seconds))
            
            self.reminder_setup.start()
        
        if self.type == 'comms':

            if self.reminder_setup.is_running():
                    self.reminder_setup.cancel()                    
            self.reminder_setup.change_interval(hours=((self.max_value_time-self.start_time).total_seconds() // 60 // 60) // 3)
            self.com_max = int((self.max_value_time-self.start_time).total_seconds() // 60 // 60 // 3)
            
            print('[COMMS Reminder]', 'No of times', self.com_max, 'HR Timer', (self.max_value_time-self.start_time).total_seconds() // 60 // 60 // 3) 
            self.com_counter = 0
            self.reminder_setup.start()


    def load_values(self):

        
        
        if isinstance(self.start_time, str):
            self.start_time = datetime.strptime(self.start_time, '%c')
        if isinstance(self.max_value_time, str):
            self.max_value_time = datetime.strptime(self.max_value_time, '%c')
           
            
        if type(self.guild) == int or type(self.guild) == str:
            print(self.bot.guilds, self.guild)
            self.guild = get(self.bot.guilds, id=int(self.guild))
            self.member = get(self.guild.members, id=int(self.member))

            if self.general_channel is None:
                if self.guild is not None:
                    self.general_channel = get(self.guild.channels, id=self.general_channel)
                    
        print([self.__dict__[k] for k in self.__dict__ if k in ['member', 'guild', 'general_channel']])
          


    def create_status_embed(self):
        if self.type == 'resin':
            desc = f"Region: {self.region.upper()}\nResin: {self.current_value}\nTime left to fill up **{self.reset_time}**"
        else:
            desc = f"Region: {self.region.upper()}\nTime left to do commissions: **{self.reset_time}**"
        embed = Embed(title=f'{self.type.title()} reminder', description=f"{desc}", color=self.bot.resource_manager.get_color_from_image(self.member.display_avatar.url))
        embed.set_author(name=self.member.display_name, icon_url=self.member.display_avatar.url)
        embed.set_thumbnail(url=self.member.display_avatar.url)
        if self.type == 'comms':
            embed.set_footer(text=f"Commission reminder ({self.com_counter}/{self.com_max})")
        return embed
    
    def stopr(self):
        self.reminder_setup.cancel()

    @property
    def current_value(self):
        if self.type == 'resin':
            return self.get_resin_value()
        else:            
            return self.value
    
    @property
    def reset_time(self):        
        if self.max_value_time > datetime.now():
            td = self.max_value_time - datetime.now()
            return get_in_str(td)
        else:
            if self.type == 'resin':
                return ': No time remaining\nNoob go farm some materials\nResin capped  (160/160)'


    @property
    def status(self):
        if self.type == 'resin':
            return self.current_value
        else:
            if self.type == 'comms':
                return self.reset_time
    




    @property
    def to_dict(self):
        return_dict = {

        }
        for k in self.__dict__:

            if isinstance(self.__dict__[k], datetime):
                return_dict[k] = self.__dict__[k].strftime('%c')
            else:
                if k == 'value':
                    return_dict[k] = self.current_value
                else:
                    if isinstance(self.__dict__[k], (Member, Guild)):
                        return_dict[k] = self.__dict__[k].id
                    else:
                        if k not in  ['reminder_setup','bot']:
                            return_dict[k] = self.__dict__[k]
                    

        return return_dict


