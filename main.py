
from base.image_generator import ImageGenerator
from base.resource_manager import ResourceManager

from core.bot import DevBot
from os import getcwd
from json import load, dump

rm = ResourceManager()
im = ImageGenerator(rm)
bot = DevBot('!',rm, True)

bot.b_run()



