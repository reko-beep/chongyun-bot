from calendar import c
from json import load, dump
from nextcord.ext import tasks
from nextcord import Member

class Reminders:
    def __init__(self) -> None:
        pass



class Reminder:
    def __init__(self, type_: str, discord_member: Member) -> None:
        self.type = type_
        self.member = discord_member
    
    @tasks.loop(seconds=60)
    async def reminder_setup(self):

        raise NotImplementedError
    

    def get_type_time(self):

        if self.type_ == 'resin':
            pass

        elif self.type_ == 'comms':
            pass