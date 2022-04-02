from pydoc import describe
from nextcord import Embed, Message, Member
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands

from core.bot import DevBot

from base.resource_manager import ResourceManager
from base.information import Information
from base.paginator import PaginatorList
from base.coop import CoopManager
 
class CoopCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf
        self.coop = CoopManager(self.resm)

    @commands.command(aliases=['cpp','coprofile'], description='cpp (discord member)\nShows the co-op profile of the user')
    async def coopprofile(self, ctx, member: Member=None):

        user = member if member is not None else ctx.author

        data = self.coop.prettify_data(user)

        if len(data) > 1:
            description = self.coop.get_description(user) if self.coop.get_description(user) is not None else 'Not yet setup'
           
            base_color = self.coop.get_color(user) if self.coop.get_color(user) is not None else 0x707dfa
            embed = Embed(title='Co-op Profile', description = description, color=base_color)
            for key in data:
                embed.add_field(name=key, value=data[key], inline=True)
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)

            thumbnail = self.coop.get_character(user)
            print(thumbnail)
            if thumbnail is not None and thumbnail != '':
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.avatar.url)
            
            image = self.coop.get_image(user)
            print(image)
            if image is not None and image != '':
                embed.set_image(url=image)
            await ctx.send(embed=embed)

        else:
            description = self.coop.get_description(user) if self.coop.get_description(user) is not None else 'Not yet setup'
           
            base_color = self.coop.get_color(user) if self.coop.get_color(user) is not None else 0x707dfa
            embed = Embed(title='Co-op Profile', description = description, color=base_color)
            for key in data:
                embed.add_field(name=key, value=data[key], inline=True)
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)

            thumbnail = self.coop.get_character(user)
            if thumbnail is not None and thumbnail != '':
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.avatar.url)
            
            image = self.coop.get_image(user)
            if image is not None and image != '':
                embed.set_image(url=image)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['cpinfo', 'coinfo'], description='cpinfo (add|remove) (domain|leylines|wl|rank|uid) (domain type|leyline name|server region) (nation| nothing | value) adds a mentioned value to the coop')

    async def coopinfo(self,ctx,  *args):

        first_arg = ['add', 'remove', 'set']
        second_arg = ['domain', 'leylines', 'wl', 'rank', 'uid']
        max_args = 4        
        min_args = 3
        args_provided = args

        if len(args_provided) < 3:
            embed = Embed(title='Co-op error', description='Insufficient arguments provided!', color=0x707dfa)
            await ctx.send(embed=embed)

        else:
            if len(args) > 3:
                check = self.coop.parse_arg(ctx.author, args[0], args[1], args[2], args[3])
            else:
                check = self.coop.parse_arg(ctx.author, args[0], args[1], args[2])
            print(check)
            status = 'added' if args[0] == 'add' else 'remove'
            if args[0] == 'set':
                status = 'set'
            if type(check) == bool:
                embed = Embed(title='Co-op profile updated!', description=f'{status.title()} {args[2]} {args[1]} to coop profile!', color=0x707dfa)
                await ctx.send(embed=embed)
            else:
                desc = '\n'.join(check)
                embed = Embed(title='Available arguments', description=f'{desc}', color=0x707dfa)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CoopCog(bot))


def teardown(bot):
    bot.remove_cog("CoopCog")



