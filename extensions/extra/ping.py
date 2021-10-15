from nextcord.ext import commands

from util.logging import logc

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")



def setup(bot):
    bot.add_cog(Ping(bot))


def teardown(bot):
    bot.remove_cog(Ping(bot))
