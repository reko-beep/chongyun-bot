from nextcord.ext import commands

from util.logging import logc

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")



def setup(client):
    client.add_cog(Ping(client))


def teardown(client):
    client.remove_cog(Ping(client))
