import os
import importlib

from util import DummyObject
from util.logging import log


class ModuleManager:
    def __init__(self, pmon):
        self.pmon = pmon
        

    
    def start(self):
        self.populate_modules()
        self.setup_processing()

    def populate_modules(self):
        """finds modules from disk and loads them"""

        ## find all modules.

        mods_dir = "modules" # folder containing all modules.         
        modules = []

  
        for mod in os.listdir(mods_dir):
            # skip non module files
            if mod.endswith('.py'):
                module = DummyObject()
                module.meta =  {
                    "name": mod[:-3], # ex: Ping.py -> Ping
                    "location": ".".join([mods_dir, mod[:-3]]),
                    "status": "unloaded"
                }
                modules.append(module)

            # skip non module folders
            test_path = os.path.join(mods_dir, mod, '__init__.py')
            if os.path.exists(test_path):
                module = DummyObject()
                module.meta =  {
                    "name": mod,
                    "location": ".".join([mods_dir, mod]),
                    "status": "unloaded"
                }
                modules.append(module)
    
        for mod in modules:
            self.log('found module:',  mod.meta['location'])

        self.pmon.modules = modules

        ## load all modules
        for index in range(len(modules)):
            self.load_module(index)


    def load_module(self, index: int):
        mod = self.pmon.modules[index]

        mod_name = mod.meta['name']
        mod_location = mod.meta['location']
        mod_status = mod.meta['status']

        self.log("loading module: ", mod_name)

        # check if module is already loaded.
        if mod_status != "unloaded":
            return False

        # load and instantiate module.
        new_mod_class = getattr(importlib.import_module(mod_location), mod_name)
        new_mod = new_mod_class(self.pmon)

        # add meta data.
        new_mod.meta["name"] = mod_name
        new_mod.meta["location"] =  mod_location


        # check if module has problems loading
        if new_mod.meta['status'] == 'unloaded':
            self.log('module was not loaded [requirements did not meet/ manually enforced')
            return False
        
        self.pmon.modules.pop(index)
        self.pmon.modules.insert(index, new_mod)


        self.log("Done")
        return True




    def setup_processing(self):
        """process messages and other events."""
        ## setup message processing.
        @self.pmon.client.listen('on_message')
        async def message_hadler(message):
            for mod in self.pmon.modules:
                mod.process_message(message)

    def log(self, *msg):
        log('[mod-man]', *msg)
    