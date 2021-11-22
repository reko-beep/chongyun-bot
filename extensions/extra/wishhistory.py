from nextcord.ext import commands
from nextcord import Embed, File,Member
from nextcord.ui import View
from nextcord.utils import get

from base.wishhistory import GenshinGacha

from core.paimon import Paimon
from util.logging import logc



gacha_client = GenshinGacha()

class WishHistory(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        pass
    
    @commands.command(aliases=['wh'])
    async def wishhistory(self,ctx, authkey_url : str):
        if authkey_url != '':
            message = await ctx.send('Huff.. Huff.. I am working!')
            check = await gacha_client.process_authkey(authkey_url,ctx.author,message,True)
            if check:
                await message.edit('Huff all done!\n Give me dumplings now! :PaimonExcited: ')

        else:
            description = 'Please give a valid feedback url!'

            embed = Embed(title=f'Error',
                            description=description,
                            color=0xf5e0d0) 

            embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar.url)

            embed.set_image(url=self.pmon.user.avatar.url)
            await ctx.send(embed=embed)


    @commands.command(aliases=['ws'])
    async def wishshow(self, ctx, uid: str='', banner_code : str=''):
        banners = {'301': 'Character Banner', '302': 'Weapon Banner', '200': 'Permanent Banner', '100': 'Beginner Banner'}
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

    @commands.command(aliases=['wishirs'])
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