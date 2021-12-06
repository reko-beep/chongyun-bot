from nextcord.ext import commands
from nextcord import Embed, File,Member
from nextcord.gateway import DiscordWebSocket
from nextcord.ui import View
from nextcord.utils import get

from base.wishhistory import GenshinGacha

from core.paimon import Paimon
from util.logging import logc



gacha_client = GenshinGacha()

class WishHistory(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        self.name = 'Genshin Wish history'
        self.description = 'Fetches your wish history from Mihoyo grasp, calculate pity for you!'
        pass
    
    @commands.command(aliases=['wh'],description='wh (wishhistory url)\nFetches wish history for user\nProvide the link to output_log.txt file or the wish history link from game!')
    async def wishhistory(self,ctx, authkey_url : str):
        if authkey_url != '':
            message = await ctx.send('Huff.. Huff.. I am working!')
            check = await gacha_client.process_authkey(authkey_url,ctx.author,message,True)
            if check is not None:
                await message.edit('Huff all done!\n Give me dumplings now! :PaimonExcited: ')
            else:
                await message.edit('Sorry no wish history link found! ')

        else:
            description = 'Please give a valid feedback url!'

            embed = Embed(title=f'Error',
                            description=description,
                            color=0xf5e0d0) 

            embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

            embed.set_image(url=self.pmon.user.avatar.url)
            await ctx.send(embed=embed)


    @commands.command(aliases=['ws'],description='ws (uid) (banner_code)\nShows wish history for provided arguments\n if no banner code is provided, prints all the available banner codes!')
    async def wishshow(self, ctx, uid: str='', banner_code : str=''):
        banners = {'301': 'Character Banner', '302': 'Weapon Banner', '200': 'Permanent Banner', '100': 'Beginner Banner','400': 'Character Event Wish 2'}
        if uid != '':
            if banner_code in banners:
                file, name = await gacha_client.fetch_image(uid,banner_code)
                logc(f'found file for banner {name}')
                if file is not None and name is not None:

                    embed = Embed(title=f'Wish history for {banners[banner_code]}',
                                color=0xf5e0d0) 

                    embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

                    embed.set_image(url=f'attachment://{name}')
                    await ctx.send(embed=embed,file=file)

                else:
                    description = 'You have not made your wish history fetch yet!'

                    embed = Embed(title=f'Error',description=description,
                                color=0xf5e0d0) 

                    embed.set_author(name=ctx.author.display_name,
                                            icon_url=ctx.author.avatar.url)

                    embed.set_thumbnail(url=self.pmon.user.avatar.url)
                    await ctx.send(embed=embed)

            else:

                '''
                prints available options
                '''

                description ='\n'.join([f'{banner}. **{banners[banner]}**' for banner in banners])

                embed = Embed(title=f'Error',description=description,
                             color=0xf5e0d0) 

                embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url=self.pmon.user.avatar.url)
                embed.set_footer(text='Please write a banner code from above')
                await ctx.send(embed=embed)
        else:

            description = 'Please write a UID'

            embed = Embed(title=f'Error',description=description,
                            color=0xf5e0d0) 

            embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

            embed.set_thumbnail(url=self.pmon.user.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['wishirs'],description='Mod only command\n resaves all images according to template!')
    async def wishimagesave(self,ctx):
        roles = [r.id for r in ctx.author.roles]
        check_role = (len(set([self.pmon.p_bot_config['mod_role']]).intersection(roles)) != 0)

        if check_role:
            gacha_client.resave_images()
            description = 'Done resaving images!'

            embed = Embed(title=f'Success',description=description,
                            color=0xf5e0d0) 

            embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

            embed.set_thumbnail(url=self.pmon.user.avatar.url)
            await ctx.send(embed=embed)
        else:
            description = 'You must have Mod role to use this command!'

            embed = Embed(title=f'Error',description=description,
                            color=0xf5e0d0) 

            embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

            embed.set_thumbnail(url=self.pmon.user.avatar.url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(WishHistory(bot))


def teardown(bot):
    bot.remove_cog("WishHistory")