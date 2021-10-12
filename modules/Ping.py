from core.module import Module



class Ping(Module):
    def __init__(self, pmon):
        """runs only once, when module is initialized."""
        super().__init__(pmon)

        # uncomment below to disable module.
        # self.meta['status'] = "unloaded"

        # add commands here.
        @self.pmon.client.command()
        async def ping(ctx):
            await ctx.send("pong!")
            # self.log("you can log stuff like this", 1,2,3)
            pass
            
   

    def process_message(self, msg):
        """process incoming message here"""
        pass