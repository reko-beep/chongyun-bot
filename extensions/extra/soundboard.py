import os
import random
import json

from nextcord import Embed, FFmpegPCMAudio
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

        with open('assets/SoundBoard/genshinimpactfandom_voicelines_data.json', encoding="utf-8") as f:
            self.voicelines = json.load(f)
        self.other_sounds = os.listdir('assets/SoundBoard/sounds')

       
        

     
    @commands.command(aliases=['sb'])
    async def soundboard(self, ctx, given_chara=None, given_voice_type=None, given_lang='Japanese'):

        # TODO: handle characters/voices with spaces correctly.
        #       maybe make (,) an optional delimiter when spaces are present

        # invoked without arguments, display availabe sounds.
        if (given_chara and given_chara) is None:
            msg = await self.handle_other_sounds(ctx)
            return

        # get language dictkey
        for lang in self.voicelines.keys():
            if given_lang.lower() in lang.lower():
                break

        # get character name dictkey
        for chara in self.voicelines[lang].keys():
            if given_chara.lower() in chara.lower():
                break
        if chara is None:
            await ctx.send("that character does not exist.")
            return

        # get voice_type dictkey
        for voice_type in self.voicelines[lang][chara].keys():
            if given_voice_type.lower() in voice_type.lower():
                break
        if voice_type is None:
            await ctx.send("that voice type does not exist.")
            return

        url = list(random.choice(self.voicelines[lang][chara][voice_type]).values())[0]
        logc("evaluated url", url)
        await self.play_audio(ctx, url)  

    
            


    async def handle_other_sounds(self, ctx):
        """display embed menu for other sounds and handle playback"""

        sounds =  self.other_sounds         
        desc = ''
        choices = [] 
        for i, sound in enumerate(sounds):
            name = sound[:-4]
            desc += f'**{i} : {name}**\n'
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
                await self.play_audio(ctx, f'assets/SoundBoard/sounds/{sounds[choice]}')
                
        return msg


    
    async def play_audio(self, ctx: Context, sound):
  
        src = FFmpegPCMAudio(sound, executable='bin/ffmpeg')

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
