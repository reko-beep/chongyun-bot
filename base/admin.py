from json import load, dump
from nextcord import Member, Embed
from nextcord.utils import get

from nextcord.ext.commands import Context
class Administrator:
    def __init__(self, bot):
        self.bot  = bot
        self.approve_role = None
        self.member_role = None
        self.approve_channel = None
        self.scrutiny = self.bot.b_config.get("scrutiny")
    

    def check_admin(self, ctx: Context):

        r = [i.id for i in ctx.author.roles]
        return len(set(r).intersection(self.bot.b_config.get("admin_roles"))) != 0

    def load_roles_channels(self, guild):
        if self.member_role is None:
                self.member_role = get(guild.roles, id=self.bot.b_config.get("member_role"))
        if self.approve_role is None:
                self.approve_role = get(guild.roles, id=self.bot.b_config.get("approve_role"))
        if self.approve_channel is None:
            self.approve_channel = get(guild.channels, id=self.bot.b_config.get('approve_channel'))
        print("roles loaded", self.approve_role, self.member_role)
        print("channels loaded", self.approve_channel)


    async def send_approve_message(self, member:Member):

        embed = Embed(title='Please answer these questions!', description='1. Where are you from?\n2.Where did you get the invite from?\n\n*our mods will approve as soon as possible*', color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        if self.approve_channel is not None:
            await self.approve_channel.send(member.mention, embed=embed)


    async def approve_member(self, ctx: Context, member: Member):

        if self.check_admin(ctx):
            if self.member_role is None:
                self.member_role = ctx.guild.get_role(self.bot.b_config.get("member_role"))
            await member.edit(roles=[self.member_role])
            return True

    async def member_role_check(self, member: Member):
        if self.scrutiny:     
            if self.approve_role is None:       
                await member.edit(roles=[self.approve_role])
                await self.send_approve_message(member)
        else:
            if self.member_role is None:   
                await member.edit(roles=[self.member_role])


        

