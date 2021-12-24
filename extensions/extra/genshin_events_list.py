
import nextcord as discord
from base.events import GenshinEvents
import json
from nextcord.ext import commands, tasks
from nextcord import TextChannel
from core.paimon import Paimon
from util.logging import logc
from fetcher.events import Events
import os

gevents = GenshinEvents()

def get_event(events, id):
    for event in events:
        if event['id'] == id:
            return event

class GenshinEventsList(commands.Cog):
    def __init__(self, client: Paimon):
        self.client = client
        self.name = 'Events'
        self.description = 'Module to send the events ongoing or passed in game!'
        self.event_fetcher = Events()
        self.event_channel: TextChannel = self.client.get_channel(self.client.p_bot_config['events_channel'])

        

    @commands.command()
    async def updateevents(self, ctx):
    
        await self.event_fetcher.update_event_list(self.event_channel)

        
        



        

def setup(client: Paimon):
    client.add_cog(GenshinEventsList(client))




def teardown(client):
    client.remove_cog("GenshinEventsList")

