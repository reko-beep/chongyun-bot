from calendar import c
from datetime import datetime, timedelta
from json import load, dump
from time import strptime
from nextcord.ext import tasks
from nextcord import Member
from os import getcwd
from os.path import exists

class Reminders:
    def __init__(self) -> None:
        self.reminders = {

        }
        pass

    def load_reminders(self):
        remind_data = {}
        if exists(getcwd()+'/reminders.json'):

            with open(getcwd()+'/reminders.json', 'r') as f:
                remind_data = load(f)

        if len(remind_data) != 0:
            for member_id in remind_data:
                reminders = remind_data[member_id]
                for reminder in reminders:
                    if member_id not in self.reminders:
                        self.reminders[member_id] = {}
                    self.reminders[member_id][reminder['type']] = Reminder(reminder['type'], datetime.now(), reminder['max_value_time'], reminder['member'], reminder['value'], reminder['max'])



class Reminder:
    def __init__(self, type_: str, current_time: datetime, max_value_time:datetime,  discord_member: str,  value:int, max_value: int = -1) -> None:
        self.type = type_
        self.member = discord_member
        self.value = value
        self.max_value = self.get_max_value() if max_value == -1 else max_value
        self.start_time = current_time
        self.max_value_time = max_value_time
        if self.max_value_time is None:
            self.get_max_time()

        if self.reminder_setup.is_running():
            self.reminder_setup.cancel()
            
        self.reminder_setup.change_interval(seconds=((self.max_value_time-self.start_time).seconds))
        print(f"[Reminder] {self.type.upper()} reminder: will remind you in {(self.max_value_time-self.start_time).seconds} when resin will cap\nStart Time:{self.start_time.strftime('%c')} End Time: {self.max_value_time.strftime('%c')}")
        self.reminder_setup.start()
    
    @tasks.loop(seconds=60)
    async def reminder_setup(self):

        print(f" [Reminder] \n{self.type.upper()} reminder\nMember: {self.member}\nCurrent {self.type.title()}: ({self.current_value}/{self.max_value})\nStart Time: {self.start_time.strftime('%c')}\nEnd Time: {self.max_value_time.strptime('%c')}\n\n Dictionary Format: {self.to_dict}")

    
    def get_max_value(self):
        if self.type == 'resin':
            return 160
        if self.type == 'comms':
            return 4
    
    def get_resin_value(self):
        if self.type == 'resin':

            if self.max_value_time is None:
                self.get_max_time()
            if self.max_value_time > self.start_time:
                return self.value + ((datetime.now()-self.start_time).total_seconds() // 60)// 8
            else:
                return self.current_value

    def get_max_time(self):
        
        if self.type == 'resin':
            if self.max_value_time == None:
               minutes_to_full = (160-self.value) * 8
               self.max_value_time = self.start_time + timedelta(minutes=minutes_to_full)
            
        if self.type == 'comms':
            '''
            
            code to reset comms time here

            '''
            pass

    def get_time_to_max(self):

        if self.type == 'resin':
    
            if self.max_value_time is None:
                self.get_max_time()
            
            if self.max_value_time > self.start_time:
                return (self.max_value_time-self.start_time).total_seconds() // 60
        
    @property
    def current_value(self):
        if self.type == 'resin':
            return self.get_resin_value()
        else:
            return self.value








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
                    if k != 'reminder_setup':
                        return_dict[k] = self.__dict__[k]

        return return_dict



test = Reminder('resin', datetime.now(), None, '123891273981237', 159)

while True:
    k = input('for checking resin, type i: ')
    if k == 'i':
        print('current resin value is ', test.current_value)