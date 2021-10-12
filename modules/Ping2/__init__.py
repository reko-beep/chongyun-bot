# when one file is too large for a module.
# a Folder with __init__.py will also act as a module with same name as Folder.

from core.module import Module

class Ping2(Module):
    def __init__(self, pmon):
        """runs only once, when module is initialized."""
        super().__init__(pmon)

        # unconmment below to disable module.
        # self.meta['status'] = "unloaded" 
    



    def process_message(self, msg):
        """process incoming message here"""
        pass