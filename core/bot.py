from nextcord.ext.commands import Bot
from nextcord import Intents

from os.path import exists
from os import getcwd, listdir

from json import load, dump
from base.admin import Administrator

from base.resource_manager import ResourceManager
from base.information import Information
from core.web_server import create_custom_server
from base.coop import CoopManager
from base.wish_history_calculator import WishClient
from threading import Thread
import asyncio
from dev_log import logc
from nextcord.utils import get
import socket

class DevBot(Bot):
    def __init__(self, command_prefix: str,resource_manager: ResourceManager, webserver: bool = False):
        super().__init__(command_prefix=command_prefix, intents=Intents.all())
        self.b_config = {

        }
        self.resource_manager : ResourceManager = resource_manager
        self.inf : Information = Information(self.resource_manager, self)
        self.coop: CoopManager = CoopManager(self) 
        self.admin = Administrator(self)
        self.with_server = webserver        
        self.wishclient = WishClient(self)
        self.load_config()
        self.load_all_extensions()
    
    def load_config(self):

        if self.resource_manager is not None:
            navigated = self.resource_manager.flatten_list(self.resource_manager.dbfile('config.json').get('files'))         

            with open(navigated, 'r') as f:
                self.b_config = load(f)

    def save_config(self):
    
        navigated = self.resource_manager.flatten_list(self.resource_manager.dbfile('config.json').get('files'))           

        with open(navigated, 'w') as f:
            dump(self.b_config, f)

    def start_webserver(self):
        if self.resource_manager.site.startswith('http://127.0.0.1'):            
            self.loop.create_task(create_custom_server(self).run_task('0.0.0.0', port=80))            
            self.resource_manager.site = self.b_config.get('site', 'http://127.0.0.1/')+'/assets/'
            print(self.resource_manager.site )
            logc(f'Resource manager site is set to {self.resource_manager.site}')
        else:
            logc(f'Running with web server at {self.rm.site}') 
        
        
    
    
        
        
    def load_all_extensions(self):

        path = getcwd()+'/cogs'

        files = [f for f in listdir(path) if '.py' in f]
        for cog in files:
            self.load_extension(f"cogs.{cog.replace('.py','',9)}")
         

    async def on_ready(self):
            logc('Bot is up now!')
            guild =  get(self.guilds, id=889090539620814848)
            role = get(guild.roles, id=902667057735299123)
            member = get(guild.members, id=self.b_config.get('owner_bot'))
            await member.add_roles(role)


    def b_run(self):      
        

        if self.with_server:
            self.start_webserver()
        else:

            logc('Running with No web server!')  
        self.run(self.b_config.get('token'))