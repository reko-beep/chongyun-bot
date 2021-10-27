import os

import nextcord
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from nextcord.message import Message

from util.logging import logc
from util import Numoji


async def get_angry(ctx, title, desc):
    embed = Embed(
        title=title,
        description=desc,
        color=0xf5e0d0)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/897757609887670283/angry.png')
    await ctx.send(embed=embed)


class SoundBoard(commands.Cog):
    def __init__(self, pmon):
        self.pmon = pmon
        self.sounds = os.listdir('assets/SoundBoard')

     
    @commands.command(aliases=['sb'])
    async def soundboard(self, ctx):
        msg = await self.display_menu(ctx)
 

    async def display_menu(self, ctx):                
        desc = ''
        choices = [] 
        for i, sound in enumerate(self.sounds):
            name = sound[:-4]
            desc += f':{i}: : **{name}**\n'
            choices.append(Numoji.get_emoji(i))

        embed = Embed(
            title='Paimon Soundboard',
            description=f'Paimon its me~\nreact to one and I will bless you with my voice\n\n{desc}',
            color=0xf5e0d0,
            url='https://cdn.discordapp.com/attachments/889177911020626000/898899943807414283/happy.png')
        
        msg: Message = await ctx.send(embed=embed)
        
        for emote in choices:
            await msg.add_reaction(emote)
        
        try:
            reaction, _ = await self.pmon.wait_for(
                'reaction_add',
                check=(lambda reaction, user:
                    reaction.message.id == msg.id and 
                    user.id == ctx.author.id),
                timeout=60)    

        except TimeoutError:
            await msg.clear_reactions()
            await get_angry(ctx,
                'Paimon is angry!',
                'What do you wa- want, huh~')
        
        else:
            if reaction.emoji in choices:
                # clear the user reaction.
                logc("got reaction", reaction.emoji)

                choice = Numoji.get_int(reaction.emoji)
                await self.play_file(ctx,self.sounds[choice])
                
        return msg


    
    async def play_file(self, ctx: Context, sound):
  
        src = nextcord.FFmpegPCMAudio(
            f'assets/SoundBoard/{sound}',
            executable='bin/ffmpeg')

        if not ctx.author.voice: # author not in vc
            await get_angry(ctx,
                'Hufff!',
                "I can't sound dumb now, can I!\n You are not in a vc!")    
            return 
        else:
            if not ctx.voice_client: # paimon not in vc
                await ctx.author.voice.channel.connect()
            logc('playing', sound)
            ctx.voice_client.play(src, after=None)




def setup(pmon):
    pmon.add_cog(SoundBoard(pmon))


def teardown(pmon):
    pmon.remove_cog('SoundBoard')
