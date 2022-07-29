
from warnings import warn
from nextcord import Embed, Message, Member, Guild
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
from nextcord.ui import View
from core.bot import DevBot
from base.paginator import PaginatorList, SwitchPaginator
from base.reminder import Reminder
from base.commstime import get_resettimes
import random

import requests

from dev_log import logc

class ReminderCommands(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.coop = self.bot.coop
        self.rc = self.bot.remind_client
        self.name = 'Reminder'
        self.description = 'Reminder modules helps you setup reminder for commissions and resin'


    @commands.Cog.listener()
    async def on_message(self, message):

        self.rc.load_reminders()

    @commands.command(aliases=['resin', 'rr'], description='resin (region) (resin) (remind_value)\nsets up a reminder for when resin hits the remind value or its fulled\nremind_value is optional', brief='sets up a resin reminder')
    async def resinreminder(self, ctx, region: str, resin: int, remind_value:int=-1):

        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:

            reminder = self.rc.add_reminder(ctx.guild, 'resin', ctx.author, region, uid, resin, remind_value)
            if isinstance(reminder, Reminder):

                embed = reminder.create_status_embed()
                await ctx.send(embed=embed)
            
            else:

                embed = Embed(title='Reminder Error', description=f'Error creating a reminder for Resin!', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

        else:
    
                embed = Embed(title='Reminder Error', description=f'You have linked the uid for that region', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

    
    @commands.command(aliases=['resinremove', 'rrmv'], description='rem (region)\nremoves the resin reminder for that region', brief='removes the resin reminder')
    async def removeresinreminder(self, ctx, region: str):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:

            reminder = self.rc.remove_reminder('resin', ctx.author, region)
            if reminder is False:
                embed = Embed(title='Reminder Error', description=f'You have not setup a resin reminder yet!', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 
            if reminder is True:
                embed = Embed(title='Reminder removed', description=f'Your resin reminder has been removed!', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

        else:
        
                embed = Embed(title='Reminder Error', description=f'You have linked the uid for that region', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

    @commands.command(aliases=['comr'], description='comr (region)\n sets up comms reminder that reminds you every 4 hr to do comms', brief='sets up a commission reminder')
    async def commissionsreminder(self, ctx, region: str):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:

            reminder = self.rc.add_reminder(ctx.guild, 'comms', ctx.author, region, uid, 0)
            if isinstance(reminder, Reminder):
    
                embed = reminder.create_status_embed()
                await ctx.send(embed=embed)
            
            else:

                embed = Embed(title='Reminder Error', description=f'Error creating a reminder for commissions !', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

        else:
    
                embed = Embed(title='Reminder Error', description=f'You have linked the uid for that region', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

        

    @commands.command(aliases=['comrr'], description='comrr (region)\n removes the comms reminder for that region', brief='removes commission reminder')   
    async def removecommissionsreminder(self, ctx, region: str):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:

            reminder = self.rc.remove_reminder('comms', ctx.author, region)
            if reminder is False:
                embed = Embed(title='Reminder Error', description=f'You have not setup a resin reminder yet!', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 
            if reminder is True:
                embed = Embed(title='Reminder removed', description=f'Your resin reminder has been removed!', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 

        else:
        
                embed = Embed(title='Reminder Error', description=f'You have linked the uid for that region', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
                await ctx.send(embed=embed) 
        
    

    @commands.command(aliases=['rems'], description='rems (type)\nshows all your resin reminders if no type is specified\ntype can be resin, comms', brief='shows all your resin reminders')
    async def reminders(self, ctx, type:str=''):

        embeds = self.rc.get_reminders(ctx.author, type)
        print(embeds)
        if embeds is not None:
            msg = await ctx.send('Your reminders', embed=embeds[0])
            list_ = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)            
            await msg.edit(view=list_)
        else:
            embed = Embed(title='Reminder Error', description=f'You have not setup a reminder yet', color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
            await ctx.send(embed=embed) 

    @commands.command(aliases=['comrst'], description='comrst\n show commission reset times for regions', brief='shows commission reset times')
    async def commissionresettime(self, ctx):

        img_ = random.choice(self.rc.wallpapers)
        desc_ = ''
        dt = get_resettimes(1,'', True)
        for reg in dt:
            if dt[reg] is not None:
                desc_ += f"{reg.upper()} resets <t:{int(dt[reg].timestamp())}:R>\n"
            else:
                desc_ += f"{reg.upper()} resetted today\n"

        desc_ += f'\n[download image in thumbnail]({img_})'
        embed = Embed(title='Commission reset times', description=desc_, color=self.resm.get_color_from_image(ctx.author.display_avatar.url))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=img_)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ReminderCommands(bot))


def teardown(bot):
    bot.remove_cog("ReminderCommands")
