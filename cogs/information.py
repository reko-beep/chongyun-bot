from pydoc import describe
from unicodedata import category
from nextcord import Embed, Message, Member, NotFound, Reaction
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
from nextcord.ui import View

from core.bot import DevBot

from base.resource_manager import ResourceManager
from base.information import Information
from base.paginator import BookmarkList, PaginatorList, DropdownList

class InformationCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf

    @commands.command(aliases=['char','character'], description='char (character name)\nshows the full info from database for a character')
    async def characterinfo(self, ctx : Context, *arg:str):


        char = ''.join(arg)

        if char != '':

            embeds = self.inf.create_character_embeds(ctx.guild, char, [],False, True)

            message : Message = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
            await message.edit(embed=embeds[0],view=view)
        else:
             
            chars = list(self.bot.resource_manager.characters.keys())
            view = View()
            view.add_item(DropdownList(self.bot, chars, 'create_character_embeds', ctx.author, 1))
            await ctx.send('All Characters list', view=view)
     
    @commands.command(aliases=['dom'], description='dom (day) (region) (type)\nshows the full info from database for a character')
    async def domain(self, ctx : Context, day:str='', region:str='', type:str=''):

        if day == '':
            embed = Embed(title='Info Error', description=f'Provide at least day for domains!', color=self.resm.get_color_from_image(ctx.author.avatar.url))
            await ctx.send(embed=embed)      
        else:
            embeds = self.inf.create_domains_embeds(day, region, type)     
            if len(embeds) > 0:  
                message : Message = await ctx.send(embed=embeds[0])
                view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
                await message.edit(embed=embeds[0],view=view)
            else:
                embed = Embed(title='Info Error', description=f'No domains found!', color=self.resm.get_color_from_image(ctx.author.avatar.url))
                await ctx.send(embed=embed)     

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user):
        print(reaction.emoji)
        if reaction.emoji == '🔖':
            msg = reaction.message
            member = user.id
            category = msg.channel.name
            check = self.inf.bookmark.add_bookmark(user, msg, category)
            if check:
                embed = Embed(title='Bookmark added!', description=msg.content+'\n'+f"**Category:**\n{category}", color=self.resm.get_color_from_image(user.avatar.url))
                embed.set_author(name=user.display_name, icon_url=user.avatar.url)
                await msg.channel.send(embed=embed)


    @commands.command(aliases=['bkc'], description='bkc (bookmark number) (category)')
    async def bookmarksetcategory(self, ctx, index: str, *cat):
        cat = ''.join(cat)
        if index.isdigit():
            index = int(index)

            check = self.inf.bookmark.set_bookmark_category(ctx.author, index, cat)
            if check:
                
                embed = Embed(title='Bookmark category changed!', description=self.inf.bookmark.bm_data[str(ctx.author.id)][index]['content']+'\n'+f"**Category:**\n{cat}", color=self.resm.get_color_from_image(ctx.author.avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

        else:
            embed = Embed(title='Bookmark error!', description="Please write bookmark number!", color=self.resm.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
    
     

    @commands.command(aliases=['wep','weapon'], description='char (character name)\nshows the full info from database for a character')
    async def weaponinfo(self, ctx : Context, *arg:str):

        wep = ' '.join(arg)
        print(wep)
        if wep != '':
            embeds = self.inf.create_weapon_embeds(ctx.guild, wep.lower(), [],False)
            print(embeds)
            message : Message = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
            await message.edit(embed=embeds[0],view=view)
        else:
            weps = list(self.bot.resource_manager.weapons.keys())
            view = View()
            view.add_item(DropdownList(self.bot, weps, 'create_weapon_embeds', ctx.author, 1))
            await ctx.send('All Weapons list', view=view)

    @commands.command(aliases=['arti','artifact'], description='arti (artifact name)\nshows the full info from database for a artifact')
    async def artifactinfo(self, ctx : Context, *arg:str):

        wep = ' '.join(arg)
        print(wep)
        if wep != '':
            embeds = self.inf.create_artifact_embeds(ctx.guild, wep.lower(), [],False)
            print(embeds)
            message : Message = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
            await message.edit(embed=embeds[0],view=view)
        else:
            weps = list(self.bot.resource_manager.artifacts.keys())
            view = View()
            view.add_item(DropdownList(self.bot, weps, 'create_artifact_embeds', ctx.author, 1))
            await ctx.send('All Artifacts list', view=view)   


    @commands.command(aliases=['af','abyssf'], description='af (floor)\nshows the builds for a character')
    async def  abyss(self, ctx : Context, floor: str):

        
        print(floor)
        embeds = self.inf.create_abyss_embeds(floor)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
        await message.edit(embed=embeds[0],view=view)


    @commands.command(aliases=['furn'], description='furn (character)\nshows the furnishing sets for a character')
    async def  furnishing(self, ctx : Context, character: str):

        
        embeds = self.inf.create_furnishing_embeds(character)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
        await message.edit(embed=embeds[0],view=view)

    @commands.command(aliases=['ctc', 'createtc'], description='ctc (title) (chars) (description)')
    async def  createteamcomp(self, ctx, title, chars, description):
        roles = [r.id for r in ctx.author.roles]
        check_roles = self.bot.b_config.get('teamcomp_role')

        if len(set(roles).intersection(check_roles) != 0):

            check, dict_ = self.inf.create_comp(title, chars, description, ctx.author)

            if check is not None:
                embed = self.inf.create_comp_embed(dict_)
                embed.color = self.resm.get_color_from_image(ctx.author.avatar.url)
                embed.set_author(name=ctx.author.display_name, url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            
            else:
                embed = Embed(title='Comp Error', description=f'Either the characters are not in correct format, or few arguments passed!', color=self.resm.get_color_from_image(ctx.author.avatar.url))
                await ctx.send(embed=embed)        
        else:
            embed = Embed(title='Comp Error', description=f'You are not allowed to create comps!', color=self.resm.get_color_from_image(ctx.author.avatar.url))
            await ctx.send(embed=embed)        


    @commands.command(aliases=['bkadd'], description='bkadd (messageid) (category)')
    async def bookmarkadd(self, ctx: Context, message: str, category: str=''):   
        
        channel = ctx.channel

        message_id = None
        if message.isdigit():
            message_id = int(message)
        channel_id = None
        if message.startswith('https://') and message.split("/")[-2].isdigit():
            channel_id = int(message.split("/")[-2])
            message_id = int(message.split("/")[-1])

        if channel_id is not None:
            try:
                channel =  await ctx.guild.fetch_channel(channel_id)
            except NotFound:
                embed = Embed(title='Bookmark Error', description=f'Either use the command in channel where message is or use message link', color=self.resm.get_color_from_image(ctx.author.avatar.url))
                await ctx.send(embed=embed)         

        

        try:
            message = await channel.fetch_message(message_id)
        except NotFound:
            embed = Embed(title='Bookmark Error', description=f'Message cannot be fetched\nTry using message link\n**Category:**\n{category}', color=self.resm.get_color_from_image(ctx.author.avatar.url))
            await ctx.send(embed=embed)
        else:
            check = self.inf.bookmark.add_bookmark(ctx.author, message, category)
            if check:
                embed = Embed(title='Bookmark', description=f'bookmark added\n**Category:**\n{category}', color=self.resm.get_color_from_image(ctx.author.avatar.url))
                await ctx.send(embed=embed)

    @commands.command(aliases=['bks'], description='bkadd (user) (category)')
    async def bookmarks(self, ctx, author: Member=None, category:str = ''):
        member = ctx.author if author is None else author
        check = self.inf.bookmark.get_bookmarks(member, category)

        if len(check) == 0:
            embed = Embed(title='Bookmark', description=f'User has not bookmarks added', color=self.resm.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = self.inf.bookmark.create_bookmark_embed(member, check[0])
            msg = await ctx.send(embed=embed)
            view = BookmarkList(user=ctx.author, bookmark_user=member, message=msg, embeds=check, bot=self.bot)
            await msg.edit(view=view)

    @commands.command(aliases=['b','builds'], description='b (character name)\nshows the builds for a character')
    async def build(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(ctx.guild, char, ['builds'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
        await message.edit(embed=embeds[0],view=view)
    
    @commands.command(aliases=['as','ascensions'], description='as (character name)\nshows the ascension materials for a character')
    async def ascension(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(ctx.guild, char, ['ascension_imgs'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
        await message.edit(embed=embeds[0],view=view)

    @commands.command(aliases=['tc','teamcomps'], description='tc (character name)\nshows the teamcomps for a character')
    async def teamcomp(self, ctx : Context, *arg:str):

        char = ''.join(arg)

        embeds = self.inf.create_character_embeds(ctx.guild, char, ['teamcomps'],True, True)

        message : Message = await ctx.send(embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
        await message.edit(embed=embeds[0],view=view)



def setup(bot):
    bot.add_cog(InformationCog(bot))


def teardown(bot):
    bot.remove_cog("InformationCog")
