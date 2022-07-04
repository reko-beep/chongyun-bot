from pydoc import describe
from warnings import warn
from nextcord import Embed, Message, Member
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
import random



from base.resource_manager import ResourceManager
from base.information import Information
from base.paginator import LibenBox, PaginatorList, SwitchPaginator
from base.coop import CoopManager
 
from dev_log import logc
class CoopCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf
        self.coop = self.bot.coop
        self.wc = self.bot.wishclient


    @commands.Cog.listener()
    async def on_message(self, message: Message):
        
        if message.guild is not None:
            self.bot.admin.load_roles_channels(message.guild)    
        if message.channel.id == self.bot.b_config.get("uid_channel"):
            if message.author.id != self.bot.user.id:
                if message.content.isdigit():
                    if message.content[0] in ['8', '7','6']:
                        self.coop.set_uid(message.author, int(message.content))
                        embed = Embed(title='UID Linked', description=f'**UID:** {message.content}\n**Region:** {self.coop.get_server_region(uid=int(message.content))}\n\n*use !cpp to see coop profile\nuse !cpinfo add|remove|set domains|leylines|rank|wl|color|image|character (value) (value) to modify your profile*', color=0xc3dde4)
                        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
                        embed.set_thumbnail(url=message.author.display_avatar.url)
                        await message.channel.send(embed=embed)
                        await message.delete()
                    else:
                        await message.delete()
                else:
                        await message.delete()
        
        if message.channel.id == self.bot.b_config.get("coop_channel") and message.author != self.bot.user:
            roles_check = len(set(self.bot.b_config.get('coop_roles')).intersection([r.id for r in message.role_mentions])) != 0

                
            if roles_check:
                warn_check = self.coop.warn_system(message.author, message)
                if warn_check in ['BANNED', 'WARNED']:
                    c = self.resm.get_color_from_image(message.author.display_avatar.url)
                    embed = Embed(title='Co-op abuse', description=f"You are tagging too quick!\n You have been {warn_check.lower()}", color=c)
                    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    await message.channel.send(embed=embed)
                
                logc('Co-op Warn system', '[', message.author.id,']', warn_check)
                if warn_check == None and warn_check not in ['BANNED', 'WARNED']:
                    digits = [int(s) for s in message.content.split() if s.isdigit()]                        
                    digits = digits[0] if len(digits) > 0 else 3
                    if digits > 3:
                        digits = 3
                        
                    region = self.coop.get_region_from_carry_role(str(message.role_mentions[0].name))
                    data = self.coop.get_data_from_carry_role(message.author, str(message.role_mentions[0].name))
                    if data is not None:
                        
                        if region in data['profiles']:
                            uid = data['profiles'][region].get('uid', 'Not Linked yet!')
                            text = f'Region for which help is needed: **{region.upper()}**\n**UID:**\n{uid}'
                        else:
                            text = f'Region for which help is needed: **{region.upper()}**\n**UID:**\nNot linked yet!'
                    else:
                        text = f'Region for which help is needed: **{region.upper()}**\n**UID:**\nNot linked yet!'

                    c = self.resm.get_color_from_image(message.author.display_avatar.url)
                    embed = Embed(title='Co-op Request', description=f"{text}\n\n*You are eligible to give {digits} co-op points\n after you have received help!*", color=c)
                    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
                    embed.set_thumbnail(url=message.author.display_avatar.url)                    
                    self.coop.add_to_give_points(message.author, digits)
                    await message.channel.send(embed=embed)
                else:
                    await message.delete()

    @commands.command(aliases=['col'])
    async def intcolor(self,ctx, hex:str):
        base = 16
        if hex.startswith('#'):
            hex = hex.replace('#','',1)

        if hex.startswith('0x'):
            base = 10
            hex.replace('0x','',1)
        
        await ctx.send(f"INT Color: {int(hex, base)}")


    @commands.command(aliases=['colbrs'], description='colbrs resets co-op leaderboard')
    async def coopleaderboardreset(self, ctx):
        if self.bot.admin.check_admin(ctx):

            check = self.coop.reset_coop_points()
            if check:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op', description=f'Coop leaderboard reset!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)
        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'Not enough perms!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['counban'], description='cogunban (user) unbans user from coop warn system')
    async def coopunban(self, ctx, user:Member=None):

        if self.bot.admin.check_admin(ctx):
            if user is not None:
                check = self.coop.unban_from_coop(user)
                if check:
                    color = self.resm.get_color_from_image(user.display_avatar.url)
                    embed = Embed(title='Co-op', description=f'User has been unbanned from co-op system!', color=color)
                    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                    await ctx.send(embed=embed)
                else:
                    if check is False:
                        color = self.resm.get_color_from_image(user.display_avatar.url)
                        embed = Embed(title='Co-op error', description=f'User is not banned!', color=color)
                        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                        await ctx.send(embed=embed)
                    else:

                        color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                        embed = Embed(title='Co-op error', description=f'Failed to unban User from co-op system!', color=color)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                        await ctx.send(embed=embed)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'Please mention a user!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'Not enough perms!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)
    
    @commands.command(aliases=['coban'], description='cogban (user) bans user from coop system')
    async def coopban(self, ctx, user:Member=None):

        if self.bot.admin.check_admin(ctx):
            if user is not None:
                check = self.coop.ban_from_coop(user)
                if check:
                    color = self.resm.get_color_from_image(user.display_avatar.url)
                    embed = Embed(title='Co-op', description=f'User has been banned from co-op system!', color=color)
                    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                    await ctx.send(embed=embed)
                else:
                    if check is False:
                        color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                        embed = Embed(title='Co-op error', description=f'User is already banned!', color=color)
                        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                        await ctx.send(embed=embed)
                    else:

                        color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                        embed = Embed(title='Co-op error', description=f'Failed to ban User from co-op system!', color=color)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                        await ctx.send(embed=embed)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'Please mention a user!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'Not enough perms!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)
    
    @commands.command(aliases=['coregp'], description='coregp (user) removes user  eligible points')
    async def coopremoveeligiblepoints(self, ctx, user:Member=None):

        if self.bot.admin.check_admin(ctx):
            if user is not None:
                check = self.coop.remove_eligible_point(user, True)
                if check:
                    color = self.resm.get_color_from_image(user.display_avatar.url)
                    embed = Embed(title='Co-op', description=f'User all eligible points that he can give others are removed!', color=color)
                    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                    await ctx.send(embed=embed)
                else:
                   
                    color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                    embed = Embed(title='Co-op error', description=f'User have zero eligible points!', color=color)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                    await ctx.send(embed=embed)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'Please mention a user!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'Not enough perms!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['cogp','cogivepoint'], description='cogp (member)\n gives co-op point to the user')
    async def coopgivepoint(self, ctx, member:Member=None):

        if member is not None:
            if member is not ctx.author:
                point_success = self.coop.add_coop_point(ctx.author, member, 1)
                if point_success is True:

                    color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                    embed = Embed(title='Co-op Point', description=f'You have given **{member.display_name}** a coop point!', color=color)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                    await ctx.send(embed=embed)
                else:
                    color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                    embed = Embed(title='Co-op error', description=f'You have given **{member.display_name}** a coop point already \n or you have not tagged carry roles!', color=color)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                    await ctx.send(embed=embed)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'You have not mentioned a user!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'You have not mentioned a user!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['gchar', 'gchars'], description='gchar (region)\n shows characters owned from genshin api')
    async def genshincharacter(self, ctx, region: str, member:Member=None):
        if member is None:
            member = ctx.author

        uid = self.coop.get_member_uid(member, region)
        if uid is not None:
            data = self.coop.get_user_data(uid, 'chars')
            if data is not None:
                embeds = self.coop.create_char_embeds(data)
                msg = await ctx.send(embed=embeds['characters'][0])
                view = SwitchPaginator(ctx.author, embeds, msg)
                await msg.edit(view=view)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'You have not made your data public from hoyolab1!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'You have not linked the uid yet for that region!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['gstat', 'gstats'], description='gstat (region)\n shows stats from genshin api')
    async def genshinstatistics(self, ctx, region: str, member:Member=None):
        if member is None:
            member = ctx.author

        uid = self.coop.get_member_uid(member, region)
        if uid is not None:
            data = self.coop.get_user_data(uid, 'stats')
            print(data)
            if data is not None:
                embeds = self.coop.create_stat_embeds(member, data)
                msg = await ctx.send(embed=embeds[0])
                view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
                await msg.edit(view=view)
            else:
                color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
                embed = Embed(title='Co-op error', description=f'You have not made your data public from hoyolab!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'You have not linked the uid yet for that region!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases=['colb'], description='colb \n shows co-op leader board')
    async def coopleaderboard(self, ctx):

        embeds = self.coop.coop_leaderboard(self.bot, ctx.guild)
        msg = await ctx.send( "Co-op leaderboard", embed=embeds[0])
        view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
        await msg.edit(view=view)


    @commands.command(aliases=['cop','copoint'], description='cpp (discord member)\nShows the co-op profile of the user')
    async def cooppoint(self, ctx, member: Member=None):

        user = member if member is not None else ctx.author

        data = self.coop.prettify_data(user)

        if len(data) > 1:
            description = self.coop.get_description(user) if self.coop.get_description(user) is not None else 'Not yet setup'
           
            base_color = self.coop.get_color(user) if self.coop.get_color(user) is not None else 0x707dfa
            embed = Embed(title='Co-op Profile', description = description, color=base_color)            
            embed.add_field(name='Co-op Points', value=data['Co-op Points'], inline=True)
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            thumbnail = self.coop.get_character(user)            
            if thumbnail is not None and thumbnail != '':
                print(thumbnail)
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.display_avatar.url)
            
            await ctx.send(embed=embed)

        else:
            description = self.coop.get_description(user) if self.coop.get_description(user) is not None else 'Not yet setup'
           
            base_color = self.coop.get_color(user) if self.coop.get_color(user) is not None else 0x707dfa
            embed = Embed(title='Co-op Profile', description = description, color=base_color)            
            embed.add_field(name='Co-op Points', value=data['Co-op Points'], inline=True)
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            thumbnail = self.coop.get_character(user)
            
            if thumbnail is not None and thumbnail != '':
                print(thumbnail)
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.display_avatar.url)
            
            await ctx.send(embed=embed)



    @commands.command(aliases=['cpp','coprofile'], description='cpp (discord member)\nShows the co-op profile of the user')
    async def coopprofile(self, ctx, member: Member=None):

        user = member if member is not None else ctx.author

        data = self.coop.prettify_data(user)

        if len(data) > 1:
            description = self.coop.get_description(user) if self.coop.get_description(user) is not None else 'Not yet setup'
           
            base_color = self.coop.get_color(user) if self.coop.get_color(user) is not None else 0x707dfa
            embed = Embed(title='Co-op Profile', description = description, color=base_color)
            for key in data:
                if key != 'Info':
                    embed.add_field(name=key, value=data[key], inline=True)
            if 'Info' in data:
                embed.set_footer(text=data['Info'])
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            thumbnail = self.coop.get_character(user)
            print(thumbnail)
            if thumbnail is not None and thumbnail != '':
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.display_avatar.url)
            
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
                if key != 'Info':
                    embed.add_field(name=key, value=data[key], inline=True)
            if 'Info' in data:
                embed.set_footer(text=data['Info'])
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            thumbnail = self.coop.get_character(user)
            if thumbnail is not None and thumbnail != '':
                embed.set_thumbnail(url=thumbnail)
            else:
                embed.set_thumbnail(url=user.display_avatar.url)
            
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
            print(args)
                        
            if len(args) > 3:   
                if args[1].strip() == 'description':   
                    print(args[0], args[1], ''.join(args[2:]))                 
                    check = self.coop.parse_arg(ctx.author, args[0], args[1], ' '.join(args[2:]))   
                else:          
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

    @commands.command(aliases=['glink'], description='glink (uid) adds a mentioned value to the coop')
    async def genshinlink(self,ctx,  uid):
        if uid.isdigit():
            check = self.coop.parse_arg(ctx.author, 'add', 'uid', uid)
            region = self.coop.get_server_region(uid=uid)
            if check:
                embed = Embed(title='Co-op profile updated!', description=f'Added {region.upper()} UID *{uid}* to coop profile!', color=0x707dfa)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Co-op Error!', description=f'Write a uid!', color=0x707dfa)
            await ctx.send(embed=embed)

    @commands.command(aliases=['gar'], description='gar (region) (ar) adds a rank for a specified region to the coop')
    async def genshinrank(self,ctx,  region, rank):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:
            if region.lower() in ['eu','asia', 'na']:
                check = self.coop.parse_arg(ctx.author, 'add', 'rank', region, rank)
                if check:
                    embed = Embed(title='Co-op profile updated!', description=f'Added World Level{rank} for region {region.upper()} to coop profile!', color=0x707dfa)
                    await ctx.send(embed=embed)
            else:
                embed = Embed(title='Co-op Error!', description=f'Not a valid region!', color=0x707dfa)
                await ctx.send(embed=embed)

        else:
            embed = Embed(title='Co-op Error!', description=f'You have not linked the uid yet!', color=0x707dfa)
            await ctx.send(embed=embed)

    @commands.command(aliases=['gwl'], description='gwl (region) (wl) adds a wl for a specified region to the coop')
    async def genshinworldlevel(self,ctx,  region, world_level):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:
            if region.lower() in ['eu','asia', 'na']:
                if world_level.isdigit():
                    if  0 < int(world_level) < 9:
                        check = self.coop.parse_arg(ctx.author, 'add', 'wl', region, world_level)
                        if check:
                            embed = Embed(title='Co-op profile updated!', description=f'Added AR {world_level} for region {region.upper()} to coop profile!', color=0x707dfa)
                            await ctx.send(embed=embed)
                    else:
                        embed = Embed(title='Co-op Error!', description=f'Allowed world levels 1-8!', color=0x707dfa)
                        await ctx.send(embed=embed)
                else:
                    embed = Embed(title='Co-op Error!', description=f'Not a number!', color=0x707dfa)
                    await ctx.send(embed=embed)

            else:
                embed = Embed(title='Co-op Error!', description=f'Not a valid region!', color=0x707dfa)
                await ctx.send(embed=embed)

        else:
            embed = Embed(title='Co-op Error!', description=f'You have not linked the uid yet!', color=0x707dfa)
            await ctx.send(embed=embed)


    @commands.command(aliases=['gserv'], description='gserv (member)')
    async def genshinserver(self,ctx,  member: Member=None, region:str=''):
        regions = ['ASIA','EU', 'NA']
        
        if member is None:
            member = ctx.author
        
        data = self.coop.prettify_data(member)
        print(data)
        embed = Embed(title='Genshin Impact Accounts', color=self.resm.get_color_from_image(member.display_avatar.url))
        
        if 'Accounts' in data:

            embed = Embed(title='Genshin Impact Accounts', description=data['Accounts'], color=self.resm.get_color_from_image(member.display_avatar.url))
            
 
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        for r in regions:            
            if region == '':
                if r in data:
                    embed.add_field(name=r.upper(), value=data[r])
            else:
                if r.lower() in region:
                    if r in data:
                        embed.add_field(name=r.upper(), value=data[r])



        await ctx.send(embed=embed)

    @commands.command(aliases=['lbt'])
    async def libentoggle(self, ctx):

        if self.bot.admin.check_admin(ctx):

            self.bot.coop.liben.enabled = not self.bot.coop.liben.enabled
            self.bot.b_config['liben'] = self.bot.coop.liben.enabled
            self.bot.save_config()

            embed = Embed(title=f'Liben Module Enabled - {self.bot.coop.liben.enabled}', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
        
        else:

            embed = Embed(title=f'Not enough perms', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['lb'])
    async def liben(self, ctx, region:str, box:str):

        if self.coop.liben.enabled:

            boxes = self.coop.liben.get_boxes(ctx.author, region, box)

            if boxes is None:

                embed = Embed(title=f'No boxes found!', description=f'**Box**: {box.title()}\n**Region:** {region.title()}\n\n**Boxes allowed:** *cryo,anemo,geo,electro,hydro,pyro*', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
                embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)

            else:

                box = random.choice(boxes)
                embed = self.coop.liben.get_random_box_embed(ctx.guild, box)
                msg = await ctx.send(embed=embed)
                view = LibenBox(bot=self.bot, user=ctx.author, msg=msg, box=box)
                await msg.edit(view=view)
        else:
            embed = Embed(title=f'Error!', description=f'Libenbox commands are disabled', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['lbadd'])
    async def libenadd(self, ctx, uid: str, box:str):

        if self.coop.liben.enabled:
            box_check = self.coop.liben.add_box(ctx.author, uid, box)

            if box_check:
                

                embed = Embed(title=f'Box added!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=embed)

            else:

                embed = Embed(title=f'Error!', description=f'Either uid is invalid or boxes are not allowed\n**Boxes allowed:** *cryo,anemo,geo,electro,hydro,pyro*', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
        else:
           
            embed = Embed(title=f'Error!', description=f'Libenbox commands are disabled', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
        

    @commands.command(aliases=['lbrem'])
    async def libenremove(self, ctx):

        if self.coop.liben.enabled:
            box_check = self.coop.liben.remove_box(ctx.author)

            if box_check:
                

                embed = Embed(title=f'Box removed!', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=embed)

            else:

                embed = Embed(title=f'Error!', description=f'You dont ahve a box listed', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title=f'Error!', description=f'Libenbox commands are disabled', color=self.bot.resource_manager.get_color_from_image(self.bot.user.display_avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)


    @commands.command(aliases=['wi','wishimport'], description='wi (authkey| link to paimon moe excel file) (region)\nregion is not required if you are using authkey')
    async def wishesimport(self, ctx, authkey, region:str=''):
        if 'paimon.moe' in authkey or authkey.split('.')[-1] in ['xlsx','xls']:
            if region != '':
                uid = self.coop.get_member_uid(ctx.author, region)
                print(uid)
                if uid is not None:
                    wishes = self.wc.save_wishes(authkey, uid)
                    if wishes is not None:
                        embed = Embed(title='Wishes', description=f'Your wishes are being processed for pity|\ncheck back in a min', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)                        
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(title='Error', description=f'The paimon moe excel file is not correct!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                        await ctx.send(embed=embed)
                else:
                    embed = Embed(title='Error', description=f'You have not linked ur uid with discord account!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                    await ctx.send(embed=embed)
            else:
                embed = Embed(title='Error', description=f'You have not provided the region\nregion is necessary for paimon moe import!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=embed)
        else:
            uid = self.coop.get_member_uid(ctx.author, region)           
            if uid is not None:
                wishes = self.wc.save_wishes(authkey, uid)
                if wishes is not None:
                    embed = Embed(title='Wishes', description=f'Your wishes are being processed for pity|\ncheck back in a min', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)                        
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(title='Error', description=f'The authkey link is not correct \ outdated!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                    self.wc.process_wishes(uid)
                    await ctx.send(embed=embed)
            else:
                embed = Embed(title='Error', description=f'You have not provided the region\nregion is necessary for paimon moe import!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=embed)

    
    @commands.command(aliases=['wish'], description='wish (region) (banner_type) \n banner types can be characters, weapons, standard, novice')
    async def wishes(self, ctx, region, banner):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:
            stats = self.wc.get_wish_stats(uid, banner)
            if stats is not None:
                embeds = self.wc.wish_embeds(stats, ctx.author)

                if embeds is not None:
                    message : Message = await ctx.send(embed=embeds[0])
                    view = PaginatorList(user=ctx.author, message=message, embeds=embeds, bot=self.bot)
                    await message.edit(embed=embeds[0],view=view)
                else:
                    embed = Embed(title='Error', description=f'Error occurred!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                    self.wc.process_wishes(uid)
                    await ctx.send(embed=embed)

            else:
                embed = Embed(title='Error', description=f'Either your wishes are not processed yet or you have not imported wishes', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                self.wc.process_wishes(uid)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Error', description=f'You have not linked ur uid to discord account!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            self.wc.process_wishes(uid)
            await ctx.send(embed=embed)

    @commands.command(aliases=['wishr'], description='wishr (region)')
    async def wishesremove(self, ctx, region):
        uid = self.coop.get_member_uid(ctx.author, region)
        if uid is not None:
            check = self.wc.wishes_clear(uid)
            if check:
                embed = Embed(title='Wishes', description=f'Your wishes data is removed', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)                        
                await ctx.send(embed=embed)
        else:
            embed = Embed(title='Error', description=f'You have not linked ur uid to discord account!', color=self.bot.resource_manager.get_color_from_image(ctx.author.display_avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            self.wc.process_wishes(uid)
            await ctx.send(embed=embed)


    @commands.command(aliases=['copannounce'], description='makes a coop announcement', brief='makes a coop result announcement')
    async def coopannounce(self, ctx):
        if self.bot.admin.check_admin(ctx):
            await self.coop.coop_announce(ctx, ctx.guild)
        else:
            color = self.resm.get_color_from_image(ctx.author.display_avatar.url)
            embed = Embed(title='Co-op error', description=f'Not enough perms!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CoopCog(bot))


def teardown(bot):
    bot.remove_cog("CoopCog")



