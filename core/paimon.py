import os
import json

import yaml



from nextcord.ext import commands,tasks
from nextcord.flags import Intents

from util.logging import log

from core.module_manager import ModuleManager

class Paimon:
    def __init__(self):
        self.bot_config = {}
        self.client = None
        self.modules = []
        self.module_manager = ModuleManager(self)
    

    # def load_config(self, config_file: str):
    #     """load bot from a yaml file"""
    #     with open(config_file) as f:
    #         try:
    #             self.bot_config = yaml.safe_load(f)
    #         except yaml.YAMLError as e:
    #             raise IOError("can't load base config file") from e


    def load_config(self, config_file: str):
        if os.path.exists('settings.json'):
            with open('settings.json','r') as f:
                self.bot_config = json.load(f)

    def configure(self):
        """configure bot and initialize discord client"""

        if self.bot_config is None:
            raise Exception("bot_config is not populated, load a config first.")

        self.log("using following config:")
        self.log(self.bot_config)

        # initialize discord client.
        self.client = commands.Bot(
            command_prefix=self.bot_config['prefix'],
            intents=Intents.all(),
            help_command=None
        )



    def start(self):
        """start the bot and discord client"""   

        @self.client.event
        async def on_ready():
            """runs when bot is logged in and ready"""

            self.log("Authentical Successful, Bot is now up...")
            self.module_manager.start()

        self.log('Starting Client...')
        self.client.run(self.bot_config['token'])
          


    def get_client(self):
        if self.client != None:
            return self.client

    def get_config(self):
        if self.bot_config != None:
            return self.bot_config

        
    def log(self, *msg):
        log(f'[-------]', *msg)
