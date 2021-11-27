import os

from nextcord.ext import commands

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.paimon import Paimon

from util.logging import logc


class ExtensionManager(commands.Cog):
    def __init__(self, pmon):
        self.pmon = pmon
        self.ext_path = "extensions.extra."

        self.loadext_all()

    
    @commands.command()
    async def loadext(self, ctx, arg):
        # todo: check if that file exists 
        # todo: add error handling.
        logc("loading extension", arg)
        self.pmon.load_extension(self.ext_path + arg)


    @commands.command()
    async def uloadext(self, ctx, arg):
        logc("unloading extension", arg)
        self.pmon.unload_extension(self.ext_path + arg)

    @commands.command(aliases=['rr'])
    async def rloadext(self, ctx, arg):
        logc("reloading extension", arg)
        self.pmon.reload_extension(self.ext_path + arg)


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

            # consider folder type module (with __init__.py) as extension. 
            test_path = os.path.join(extensions_dir, ext, '__init__.py')
            if os.path.exists(test_path):
                extpath =  ".".join([rootpkg, ext])
                
                extensions.append(extpath)

        for ext in extensions:
            print(ext)
            self.pmon.load_extension(ext)
            logc('loaded extension:',  ext)



def setup(pmon: Paimon):
    pmon.add_cog(ExtensionManager(pmon))


    # extension file watcher: reloads when extra extension modules are modified
    class ExtensionFileChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            super().on_modified(event)
            if not event.is_directory:
                _, filename = os.path.split(event.src_path)
                module_name = filename[:-3]
                logc("reloading ", module_name)
                pmon.reload_extension('extensions.extra.' + module_name)

    event_handler = ExtensionFileChangeHandler()
    observer = Observer()

    watch_path = os.path.join('extensions', 'extra')
    observer.schedule(event_handler, watch_path)
    observer.start()



def teardown(pmon: Paimon):
    pmon.remove_cog("ExtensionManager")
