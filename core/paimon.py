import json


from nextcord.ext import commands
from nextcord.flags import Intents


from util.logging import logc


class Paimon:
    def __init__(self):
       
        self.bot_config = {}
        self.client = None
        self.core_extensions = [
            "extensions.core.extman"
        ]


    def __load_config(self, config_file: str):
        """loads config file from disk"""

        # todo: add yaml support.
        try:
            with open(config_file, 'r') as f:
                self.bot_config = json.load(f)
        except FileNotFoundError:
            logc("Config file cannot be located...")
            raise
        except Exception:
            logc('Config file structure is invalid...')
            raise


    def load_core_extensions(self):
        """load core extension: these extensions cannot be dynamically managed"""
        for ext in self.core_extensions:
            logc("loading core extension:", ext)
            self.client.load_extension(ext)


    def configure(self, config_file: str):
        """configure bot and initialize discord client"""

        self.__load_config(config_file)
        logc("using following config:")
        logc(self.bot_config)

        # initialize discord client.
        self.client = commands.Bot(
            command_prefix=self.bot_config['prefix'],
            intents=Intents.all(),
            help_command=None
        )

        return self
        

    def start(self):
        """start the bot and discord client"""   

        @self.client.event
        async def on_ready():
            """runs when bot is logged in and ready"""

            logc("Authentication Successful...")
            self.load_core_extensions()

        logc('Starting Bot Client...')
        self.client.run(self.bot_config['token'])
          

    def get_client(self):
        if self.client != None:
            return self.client


    def get_config(self):
        if self.bot_config != None:
            return self.bot_config

    
