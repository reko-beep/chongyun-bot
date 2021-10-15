from nextcord.ext import commands

from util.logging import logc

from base.help import GenshinHelp

help_handler = GenshinHelp()

class GHelp(commands.Cog):
    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['help', 'h'])
    async def ghelp(self, ctx):    
        stop = False
        select = 0
        embeds,emojis = help_handler.create_embeds()
        count = len(embeds)
        msg = await ctx.send(embed=embeds[0])
        for i in emojis:
            await msg.add_reaction(i)
        while stop == False:
            try:
                def check(reaction,user):
                    return reaction.message.id == msg.id and user == ctx.author
                reaction, user = await self.client.wait_for('reaction_add',check=check,timeout=60)
            except TimeoutError:
                await msg.clear_reactions()
            else:                    
                if reaction.emoji in emojis:                
                    if reaction.emoji == '➡️':
                        if select < count-1:
                            select += 1
                            await msg.edit(embed=embeds[select])                           
                    if reaction.emoji == '⬅️':
                        if select >= 1:
                            select -= 1
                            await msg.edit(embed=embeds[select])


def setup(bot):
    bot.add_cog(GHelp(bot))


def teardown(bot):
    bot.remove_cog(GHelp(bot))
