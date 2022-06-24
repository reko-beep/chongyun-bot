
from os import listdir, remove
from os.path import join, isfile, islink, getsize
from pydoc import describe
from warnings import warn
from nextcord import Embed, Message, Member
from nextcord.ext.commands import Cog, Context
from nextcord.ext import commands
from asyncio import sleep
from core.bot import DevBot
from base.paginator import PaginatorList, SwitchPaginator, ApproveForm
import nextcord
import requests

from dev_log import logc
GUILD_IDS = 889090539620814848
class AdminCog(Cog):
    def __init__(self, bot: DevBot):
        self.bot = bot
        self.resm = self.bot.resource_manager
        self.inf = self.bot.inf
        self.coop = self.bot.coop


    @commands.Cog.listener()
    async def on_message(self, message: Message):

        '''

        no text channel in leaks

        '''

        if message.channel.id == self.bot.b_config.get('leak_channel',-1):
    
            checks = ('http' in message.content or 'https' in message.content or len(message.embeds) != 0 or len(message.attachments) != 0 or message.webhook_id or '>>' in message.content.lower())
            if checks: 
                pass
            else:
                await message.delete()


        if message.channel.id == self.bot.b_config.get('art_channel'):
            
            if '/artworks/' in message.content and 'pixiv.net' in message.content and 'http' in message.content or 'https' in message.content:

                links = message.content.split('\n')
                print(links)
                async with message.channel.typing():
                    for link in links:
                        id_ = link.split('/')[-1]
                        data = self.bot.admin.get_original_pixiv_image(link)
                        if data is not None:
                            file = data['file']
                            embed = Embed(title=data['title'], description=f"by **{data['username']}**", url=link, color=self.resm.get_color_from_image(self.bot.user.avatar.url))
                            embed.set_image(url='attachment://image.png')
                            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
                            embed.set_footer(text='requested by '+str(message.author))
                            await message.channel.send(embed=embed, file=file)
                            await sleep(3)
                            print('request to download response', file.status_code)

                await message.delete()

    @commands.command(aliases=['pixc'])
    async def pixivclear(self, ctx):

        if self.bot.admin.check_admin(ctx):

            path = self.bot.resource_manager.path.format(path='pixiv/')
            files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
            for f in files:
                remove(f)
            embed = Embed(title='All pixiv files removed!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Pixiv Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)  


    @commands.command(aliases=['danb'], description='shows local saved image if no argument provided else danb (search, page)')
    async def danbooru(self, ctx, *arg):

        if len(arg) > 1:
            s = ' '.join(arg)
        else:
            s = ''.join(arg)
        search = s
        page = 1
        sfw_filter = True
        if ',' in s:
            page = s.split(',')[1].strip()
            search = s.split(",")[0].strip()

        if ctx.channel.is_nsfw():
            sfw_filter = False
        print(page, search, sfw_filter)
        if search != '':
            embeds = self.bot.admin.danbooru_embeds(ctx.author, search, page, sfw_filter)
        else:
            embeds = self.bot.admin.danbooru_local(ctx.author)
        if embeds is not None:                
            msg = await ctx.send(embed=embeds[0])
            view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
            await msg.edit(view=view)
        else:
            color = self.resm.get_color_from_image(ctx.author.avatar.url)
            embed = Embed(title='Danbooru error', description=f'Nothing found!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        

    @commands.command(aliases=['danbc'])
    async def danbooruclear(self, ctx):

        if self.bot.admin.check_admin(ctx):

            path = self.bot.resource_manager.path.format(path='danbooru/')
            files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
            for f in files:
                remove(f)
            embed = Embed(title='All danbooru files removed!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Danbooru  Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)  


    @commands.command(aliases=['pix'], description='shows local saved image if no argument provided else pix (pixiv link or search)')
    async def pixiv(self, ctx, *arg):
        s = ''.join(arg)
        size = 0
        footer = "Pixiv"
        page = 1
        if ',' in s:
            page = int(s.split(',')[1].strip())
            s = s.split(',')[0]
        if s == '':
            data = self.bot.admin.get_pixiv_local()            
            base_path = self.bot.resource_manager.path.format(path='pixiv/')
            ids = [f for f in listdir(base_path) if isfile(join(base_path, f))]
            
            for f in listdir(base_path):
                if isfile(join(base_path, f)):
                    if not islink(join(base_path, f)):
                            size += getsize(join(base_path, f)) >> 20
            footer = f"Pixiv local files - files {len(ids)} - size {size} MB"
        else:
            data = self.bot.admin.pixiv_search(s, ctx.channel, page)
        if data is not None:
            if len(data) > 0:                
                
                embeds = self.bot.admin.pixiv_embeds(data, footer)
                msg = await ctx.send(embed=embeds[0])
                view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
                await msg.edit(view=view)
            else:
                color = self.resm.get_color_from_image(ctx.author.avatar.url)
                embed = Embed(title='Pixiv error', description=f'Nothing found!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

                await ctx.send(embed=embed)
        else:
            color = self.resm.get_color_from_image(ctx.author.avatar.url)
            embed = Embed(title='Pixiv error', description=f'Nothing found!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
    
    @commands.command(aliases=['sauce'], description='sauce (image upload or link)')
    async def saucenao(self, ctx: Context, url: str=''):
        attachment = url
        if url == '':
            if len(ctx.message.attachments) > 0:
                attachment = ctx.message.attachments[0].url
        
        
        if attachment == '':
            color = self.resm.get_color_from_image(ctx.author.avatar.url)
            embed = Embed(title='Saucenao error', description=f'No Image provided\n**either provide link to image or upload image with command*', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        else:

            embeds = self.bot.admin.saucenao_embed(attachment)
            if embeds is not None:
                msg = await ctx.send(embed=embeds[0])
                view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
                await msg.edit(view=view)
            else:
                color = self.resm.get_color_from_image(ctx.author.avatar.url)
                embed = Embed(title='Saucenao error', description=f'Failed to get source', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

                await ctx.send(embed=embed)



    @commands.command(aliases=['zc'], description='zc search,page')
    async def zerochan(self, ctx, *arg):
        if len(arg) > 1:
            s = ' '.join(arg)
        else:
            s = ''.join(arg)
        search = s
        page = 1
        if ',' in s:
            page = s.split(',')[1].strip()
            search = s.split(",")[0].strip()
        print(s, page, search)
        data = self.bot.admin.zerochan_search(search, page)
        if data is not None:
            if len(data) > 0:                
             
                embeds = self.bot.admin.zerochan_embeds(ctx.author, search, data)
                msg = await ctx.send(embed=embeds[0])
                view = PaginatorList(user=ctx.author, message=msg, embeds=embeds, bot=self.bot)
                await msg.edit(view=view)
            else:
                color = self.resm.get_color_from_image(ctx.author.avatar.url)
                embed = Embed(title='Zerochan error', description=f'Nothing found!', color=color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

                await ctx.send(embed=embed)
        else:
            color = self.resm.get_color_from_image(ctx.author.avatar.url)
            embed = Embed(title='Zerochan error', description=f'Nothing found!', color=color)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await self.bot.admin.member_role_check(member)
    
    @nextcord.slash_command(name='af', guild_ids=[GUILD_IDS], description='Opens up a approval form')
    async def approvalform(self, interaction : nextcord.Interaction):
        await interaction.response.send_modal(ApproveForm(self.bot, interaction.user))

    @commands.command(aliases=['approve'], description='approve (member)')
    async def approvemember(self, ctx, member: Member):
        check = await self.bot.admin.approve_member(ctx, member)
        if check is True:
            embed = Embed(title='Member approved', color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Member Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(description='toggles scrutiny')
    async def scrutiny(self, ctx):
        check = self.bot.admin.check_admin(ctx)
        member = ctx.author
        if check is True:
            self.bot.admin.scrutiny = not self.bot.admin.scrutiny
            self.bot.b_config['scrutiny'] = self.bot.admin.scrutiny
            self.bot.save_config()
            embed = Embed(title='Scrutiny', color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
            embed.add_field(name='Status', value=str(self.bot.admin.scrutiny))
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title='Scrutiny Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['ac'])
    async def announcecode(self, ctx: Context, code:str):

        if self.bot.admin.check_admin(ctx):
            embed, file = self.bot.admin.create_code_embed(code)

            await ctx.send(embed=embed, file=file)
        else:
            
            embed = Embed(title='Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(ctx.author.avatar.url))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(AdminCog(bot))


def teardown(bot):
    bot.remove_cog("AdminCog")