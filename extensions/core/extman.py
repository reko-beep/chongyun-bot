import os

from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot
from util.logging import logc




class ExtensionManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ext_path = "extensions.extra."

        self.loadext_all()


    
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


    def loadext_all(self):
        """finds modules from disk and loads them"""

        ## find all modules.

        extensions_dir = "extensions/extra" # folder containing all modules.         
        extensions = []


        for ext in os.listdir(extensions_dir):

            rootpkg = extensions_dir.replace('/', '.')
            # consider root module as extension.
            if ext.endswith('.py'):
                extpath =  ".".join([rootpkg, ext[:-3]])
                extensions.append(extpath)

            # consider root package with __init__.py as extension. 
            test_path = os.path.join(extensions_dir, ext, '__init__.py')
            if os.path.exists(test_path):
                extpath =  ".".join([rootpkg, ext])
                
                extensions.append(extpath)

        for ext in extensions:
            self.client.load_extension(ext)
            logc('loaded extension:',  ext)






def setup(bot: Bot):
    bot.add_cog(ExtensionManager(bot))


def teardown(bot: Bot):
    bot.remove_cog(ExtensionManager(bot))
