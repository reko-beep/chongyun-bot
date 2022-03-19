from nextcord import Embed
from nextcord.ext.commands import Cog
from core.bot import DevBot
from base.resource_manager import ResourceManager

class Information(Cog):
    def __init__(self, bot: DevBot, res: ResourceManager):
        self.bot = bot
        self.resm = res

    
        