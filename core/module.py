from util.logging import log

class Module:
    pass

    def __init__(self, pmon):
        self.pmon = pmon
        self.meta = {
            "status": "loaded",
        }


    

    def process_message(self, msg):
        pass


    def log(self, *msg):
        log(f'[mod: {self.__class__.__name__}]', *msg)