
from nextcord.ext import commands
from nextcord import Embed, File
from nextcord.ui import View

from base.guides import GenshinGuides
from extensions.views.guides import AddImageOption, BuildOptions,AscensionOptions,NavigatableView

from core.paimon import Paimon


class Guides(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.guides_handler = GenshinGuides(pmon)
        self.name = 'Genshin Guides'
        self.description = 'Shows ascension or build guides of characters!'



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

    @commands.command(aliases=['ascensions','as'])
    async def ascension(self,ctx, arg: str= ''):
        if arg != '':
            embeds, files = self.guides_handler.create_embeds('as',arg)

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

    @commands.command(aliases=['addg'],description='addg\nOpens an interaction to add ascension or build guide!')
    async def addguide(self,ctx, type:str= ''):
        check_roles = self.pmon.p_bot_config['mod_role']
        check = (len(set(check_roles).intersection([r.id for r in ctx.author.roles])) != 0)
        type = type.lower()
        allowed = ['as','b']
        if type in allowed:
            if check is True:           
                view_object = NavigatableView(ctx.author)
                view_object.add_item(AddImageOption(self.pmon,self.guides_handler,type,ctx.author))
                await ctx.send('Please select a character from below?',view=view_object)
            else:
                embed = Embed(title='Administration Error',description='You dont have enough privilege to add builds',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Guides Error',description='Please provide an option for below.\n**b** for build\n**as** for ascension',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['addc'],description='addc\nAdds a character!')
    async def addcharacter(self,ctx, *, character: str):
        check_roles = self.pmon.p_bot_config['mod_role']
        check = (len(set(check_roles).intersection([r.id for r in ctx.author.roles])) != 0)
        character = ''.join(character)
        
        if check is True:    

            check_c = self.guides_handler.add_character(character)
            if check_c is not None:
                embed = Embed(title='Added Character',description=f'{character.title()} added in database!',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
                await ctx.send(embed=embed)

               
            else:                
                embed = Embed(title='Guides Error',description='The character already exists!',color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
                await ctx.send(embed=embed)


               
        else:
            embed = Embed(title='Administration Error',description='You dont have enough privilege to add builds',color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/QNKWJp2.gif')
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Guides(bot))


def teardown(bot):
    bot.remove_cog("Guides")