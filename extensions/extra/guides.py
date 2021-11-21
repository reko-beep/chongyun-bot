
from nextcord.ext import commands
from nextcord import Embed, File
from nextcord.ui import View

from base.guides import GenshinGuides
from extensions.views.guides import BuildOptions,AscensionOptions,NavigatableView

from core.paimon import Paimon


class Guides(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.guides_handler = GenshinGuides(pmon)



    @commands.command(aliases=['builds','b'])
    async def build(self,ctx, arg: str= ''):
        if arg != '':
            embeds, files = self.guides_handler.create_embeds('b',arg)

            if embeds and files:
                for index in range(len(embeds)):
                    await ctx.send(embed=embeds[index],file=files[index])
            else:
                embed =  Embed(title=f'Error!',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
                embed.set_thumbnail(url=f'attachment://sorry.png')
                file = File(f'{self.guides_handler.path}/paimon/sorry.png',filename='sorry.png')
                await ctx.send(embed=embed,file=file)
        else:
            view_object = NavigatableView(ctx.author)
            view_object.add_item(BuildOptions(self.pmon,self.guides_handler,ctx.author))
            await ctx.send('Please select a character from below?',view=view_object)

    @commands.command(aliases=['builds','b'])
    async def build(self,ctx, arg: str= ''):
        if arg != '':
            embeds, files = self.guides_handler.create_embeds('b',arg)

            if embeds and files:
                for index in range(len(embeds)):
                    await ctx.send(embed=embeds[index],file=files[index])
            else:
                embed =  Embed(title=f'Error!',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
                embed.set_thumbnail(url=f'attachment://sorry.png')
                file = File(f'{self.guides_handler.path}/paimon/sorry.png',filename='sorry.png')
                await ctx.send(embed=embed,file=file)
        else:
            view_object = NavigatableView(ctx.author)
            view_object.add_item(AscensionOptions(self.pmon,self.guides_handler,ctx.author))
            await ctx.send('Please select a character from below?',view=view_object)
  
  

def setup(bot):
    bot.add_cog(Guides(bot))


def teardown(bot):
    bot.remove_cog("Guides")