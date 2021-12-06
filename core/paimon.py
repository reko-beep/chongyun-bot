import json

from nextcord.ext.commands import Bot


from nextcord.ext import commands
from nextcord.flags import Intents


from util.logging import logc


class Paimon(Bot):

    # use p_ prefix for attributes specific to paimon
    # to prevent collision form  Bot's attributes.
    # have any better idea?

    def __init__(self, config_file: str =None):
        """configures paimon (client) and initialize."""
        
        self.p_bot_config = {}
        self.p_core_extensions = [
            "extensions.core.extman"
        ]

        self.p_load_config(config_file)
        logc("using following config:", self.p_bot_config)

        # configure discord client.
        super().__init__(
            command_prefix=self.p_bot_config['prefix'],
            intents=Intents.all(),
            help_command=None,
        )


    def p_load_config(self, config_file: str):
        """loads config file from disk"""
        # TODO: add yaml support.
        try:
            with open(config_file, 'r') as f:
                self.p_bot_config = json.load(f)
        except (FileNotFoundError, TypeError):
            logc("Error: Config file cannot be located...")
            raise
        except Exception:
            logc('Error: Config file structure is invalid...')
            raise
    
    def p_save_config(self, config_file: str):
        """loads config file from disk"""
        # TODO: add yaml support.
        try:
            with open(config_file, 'w') as f:
                json.dump(self.p_bot_config,f,indent=1)
        except (FileNotFoundError, TypeError):
            logc("Error: Config file cannot be located...")
            raise
        except Exception:
            logc('Error: Config file structure is invalid...')
            raise

    def p_load_core_extensions(self):
        """load core extension: these extensions cannot be dynamically managed"""
        for ext in self.p_core_extensions:
            logc("loading core extension:", ext)
            self.load_extension(ext)


        

    def p_start(self):
        """start the bot and discord client"""   

        @self.event
        async def on_ready():
            """runs when bot is logged in and ready"""
           
            logc("Authentication Successful...")
            self.p_load_core_extensions()

        @self.listen('on_message')
        async def on_message(message):
            """unimplemented"""
            pass

        logc('Starting Bot Client...')
        self.run(self.p_bot_config['token'])
          



    def get_config(self):
        if self.p_bot_config is not None:
            return self.p_bot_config
    
