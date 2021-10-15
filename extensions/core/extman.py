from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from util.logging import logc




class ExtensionManager(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.ext_path = "extensions.extra."

    
    @commands.command()
    async def loadext(self, ctx, arg):
        # todo: check if that file exists 
        # todo: add error handling.
        logc("loading extension", arg)
        self.bot.load_extension(self.ext_path + arg)

    @commands.command()
    async def uloadext(self, ctx, arg):
        logc("unloading extension", arg)
        self.bot.unload_extension(self.ext_path + arg)
    
    async def rloadext(self, ctx, arg):
        logc("reloading extension", arg)
        self.bot.reload_extension(self.ext_path + arg)





def setup(bot: Bot):
    bot.add_cog(ExtensionManager(bot))


def teardown(bot: Bot):
    bot.remove_cog(ExtensionManager(bot))
