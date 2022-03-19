from base.resource_manager import ResourceManager
from core.bot import DevBot
from base.resource_manager import ResourceManager

rm = ResourceManager()
bot = DevBot('!',rm, True)



bot.b_run()