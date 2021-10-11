import os
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json
class GenshinHelp:
    def __init__(self):
        self.embeds = {}
        self.file = 'help.json'
        self._load()
        pass
    
    def _load(self):
        if os.path.exists(self.file):
            with open(self.file,'r') as f:
                self.embeds = json.load(f)

    def create_embeds(self):
        embeds_ = []
        emojis = ['⬅️','➡️']
        for i in self.embeds:
            embed = discord.Embed.from_dict(self.embeds[i])
            embeds_.append(embed)
        return embeds_,emojis

