
from base.image_generator import ImageGenerator
from base.resource_manager import ResourceManager

from core.bot import DevBot

from json import load

rm = ResourceManager()
im = ImageGenerator()

bot = DevBot('!',rm, True)
bot.b_run()
