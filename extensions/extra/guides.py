
from nextcord.ext import commands
from nextcord import Embed, File

from base.guides import GenshinGuides


from core.paimon import Paimon


class Guides(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.guides_handler = GenshinGuides(pmon)



    @commands.command(aliases=['builds','b'])
    async def build(self,ctx, arg):
        embeds, files = self.guides_handler.create_embeds('b',arg)

        if embeds and files:
            for index in range(len(embeds)):
                await ctx.send(embed=embeds[index],file=files[index])
        else:
            embed =  Embed(title=f'Error!',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
            embed.set_thumbnail(url=f'attachment://sorry.png')
            file = File(f'{self.guides_handler.path}/paimon/sorry.png',filename='sorry.png')
            await ctx.send(embed=embed,file=file)

    @commands.command(aliases=['ascensions','b'])
    async def ascension(self,ctx, arg):
    
        embeds, files = self.guides_handler.create_embeds('as',arg)

        if embeds and files:
            for index in range(len(embeds)):
                await ctx.send(embed=embeds[index],file=files[index])
        else:
            embed =  Embed(title=f'Error!',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
            embed.set_thumbnail(url=f'attachment://sorry.png')
            file = File(f'{self.guides_handler.path}/paimon/sorry.png',filename='sorry.png')
            await ctx.send(embed=embed,file=file)

def setup(bot):
    bot.add_cog(Guides(bot))


def teardown(bot):
    bot.remove_cog("Guides")