from pydoc import describe
from warnings import warn
from nextcord import Embed, Message, Member
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands

from core.bot import DevBot
from base.paginator import PaginatorList, SwitchPaginator

 
from dev_log import logc

class AdminCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf
        self.coop = self.bot.coop


    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        self.bot.admin.member_role_check(member)
    
    @commands.command(aliases=['approve'], description='approve (member)')
    async def approvemember(self, ctx, member: Member):
        check = self.bot.admin.approve_member(ctx, member)
        if check is True:
            embed = Embed(title='Member approved', color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Member Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(AdminCog(bot))


def teardown(bot):
    bot.remove_cog("AdminCog")