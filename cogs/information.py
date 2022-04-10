from nextcord import Embed, Message
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
from nextcord.ui import View

from core.bot import DevBot

from base.resource_manager import ResourceManager
from base.information import Information
from base.paginator import PaginatorList, DropdownList

class InformationCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf

    @commands.command(aliases=['char','character'], description='char (character name)\nshows the full info from database for a character')
    async def characterinfo(self, ctx : Context, *arg:str):


        char = ''.join(arg)

        if char != '':

            embeds = self.inf.create_character_embeds(char, [],False, True)

            message : Message = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
            await message.edit(embed=embeds[0],view=view)
        else:
             
            chars = list(self.bot.resource_manager.characters.keys())
            view = View()
            view.add_item(DropdownList(self.bot, chars, 'create_character_embeds', ctx.author, 1))
            await ctx.send('All Characters list', view=view)
     
    

    @commands.command(aliases=['wep','weapon'], description='char (character name)\nshows the full info from database for a character')
    async def weaponinfo(self, ctx : Context, *arg:str):

        wep = ''.join(arg)
        if wep != '':
            embeds = self.inf.create_weapon_embeds(wep, [],False)

            message : Message = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
            await message.edit(embed=embeds[0],view=view)
        else:
            weps = list(self.bot.resource_manager.weapons.keys())
            view = View()
            view.add_item(DropdownList(self.bot, weps, 'create_weapon_embeds', ctx.author, 1))
            await ctx.send('All Weapons list', view=view)
            

    
    @commands.command(aliases=['b','builds'], description='b (character name)\nshows the builds for a character')
    async def build(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(char, ['builds'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
        await message.edit(embed=embeds[0],view=view)
    
    @commands.command(aliases=['as','ascensions'], description='as (character name)\nshows the ascension materials for a character')
    async def ascension(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(char, ['ascension_imgs'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
        await message.edit(embed=embeds[0],view=view)

    @commands.command(aliases=['tc','teamcomps'], description='tc (character name)\nshows the teamcomps for a character')
    async def teamcomp(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(char, ['teamcomps'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds)
        await message.edit(embed=embeds[0],view=view)



def setup(bot):
    bot.add_cog(InformationCog(bot))


def teardown(bot):
    bot.remove_cog("InformationCog")
