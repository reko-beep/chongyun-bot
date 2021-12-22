from json import load, dump
from nextcord import Embed, Member, SelectOption, Interaction, FFmpegPCMAudio
from nextcord.ui import  View, Select
from nextcord.ext.commands import Context
from util.logging import logc
from os import getcwd
import random
from typing import Optional
from base.ost import GenshinOST
from core.paimon import Paimon


path = f'{getcwd()}/assets/SoundBoard/voiceovers.json'

with open(path,'r') as f:
    data = load(f)

OST = GenshinOST()

async def get_angry(ctx, title, desc):
    embed = Embed(
        title=title,
        description=desc,
        color=0xf5e0d0)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/889177911020626000/897757609887670283/angry.png')
    await ctx.send(embed=embed)



def get_characters(language):
    if language in data:
        return list(data[language].keys())

def get_languages():    
    return list(data.keys())

def get_voiceovers(language, character_name):
    if language in data:
        if character_name in data[language]:            
            return list(data[language][character_name].keys())

def get_url(language, character_name, voice_over):
    if language in data:
        if character_name in data[language]:            
            return random.choice(data[language][character_name][voice_over])

async def play_audio(ctx: Context, sound):
  
        src = FFmpegPCMAudio(sound, executable='ffmpeg')

        if not ctx.author.voice: # author not in vc
            await get_angry(ctx,
                'Hufff!',
                "I can't sound dumb now, can I!\n You are not in a vc!")    
            return 
        else:
            if not ctx.voice_client: # paimon not in vc
                await ctx.author.voice.channel.connect()
            ctx.voice_client.play(src, after=None)



class VoiceOverList(Select):
    def __init__(self,pmon: Paimon, type_: str, language: str, character: str ,ctx : Context,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        self.pmon = pmon        
        self.type_ = type_
        self.language = language
        self.character = character
        if self.type_ == 'languages':
            self.option_list = get_languages()
        if self.type_ == 'characters':
            self.option_list = get_characters(self.language)
        if self.type_ == 'voiceovers':
            self.option_list = get_voiceovers(self.language, self.character)
            if len(self.option_list) == 0:
                self.option_list = ['Nothing','Found','Sorry!']
                self.type_ = 'error'
        self.page = page
        self.ctx = ctx
        
       

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*21
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-21
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0   
        for option in self.option_list[first:limit]:
            self.append_option(SelectOption(label=option))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.ctx.author:

            if self.values[0] == 'Previous':             
                print(self.type_)
                view = NavigatableView(self.ctx.author)
                view.add_item(VoiceOverList(self.pmon,self.type_,self.language,self.character,self.ctx,self.page-1))   
                await interaction.message.edit('Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next': 
                    print(self.type_, self.character)        
                    view = NavigatableView(self.ctx.author)
                    view.add_item(VoiceOverList(self.pmon,self.type_,self.language,self.character,self.ctx,self.page+1))   
                    await interaction.message.edit('Please select a option from below?',view=view)      

                else: 
                    if self.type_ == 'languages':         
                        view = NavigatableView(self.ctx.author)
                        view.add_item(VoiceOverList(self.pmon,'characters',self.values[0],self.character,self.ctx,self.page+1))   
                        await interaction.message.edit('Please select a character from below?',view=view)   
                    else:
                        if self.type_ == 'characters':         
                            view = NavigatableView(self.ctx.author)
                            view.add_item(VoiceOverList(self.pmon,'voiceovers',self.language,self.values[0],self.ctx,self.page+1))   
                            await interaction.message.edit('Please select a voice over from below?',view=view)   
                        else:

                            if self.type_ == 'voiceovers':  
                                url = get_url(self.language,self.character,self.values[0])   
                                if url is not None:          
                                    await play_audio(self.ctx,url )
                                else:
                                    await get_angry(self.ctx,'Soundboard Error','Sorry the audio does not exists')
                    
                            

class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()


class OSTList(Select):
    def __init__(self,pmon: Paimon, type_: str, album: str, track: str ,ctx : Context,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        self.pmon = pmon        
        self.type_ = type_
        self.album = album
        self.track = track
        if self.type_ == 'albums':
            self.option_list = OST.get_album_names()
        if self.type_ == 'tracks':
            self.option_list = OST.get_track_names(self.album)        
            if len(self.option_list) == 0:
                self.option_list = ['Nothing','Found','Sorry!']
                self.type_ = 'error'
        self.page = page
        self.ctx = ctx
        
       

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*21
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-21
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0   
        for option in self.option_list[first:limit]:
            self.append_option(SelectOption(label=option))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.ctx.author:

            if self.values[0] == 'Previous':             
                print(self.type_)
                view = NavigatableView(self.ctx.author)
                view.add_item(OSTList(self.pmon,self.type_,self.album,self.track,self.ctx,self.page-1))   
                await interaction.message.edit('Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next':    
                    view = NavigatableView(self.ctx.author)
                    view.add_item(OSTList(self.pmon,self.type_,self.album,self.track,self.ctx,self.page+1))   
                    await interaction.message.edit('Please select a option from below?',view=view)      

                else: 
                    if self.type_ == 'albums':         
                        view = NavigatableView(self.ctx.author)
                        view.add_item(OSTList(self.pmon,'tracks',self.values[0],self.track,self.ctx,self.page+1))   
                        await interaction.message.edit('Please select a track from below?',view=view)   
                    else:
                        if self.type_ == 'tracks':  
                            track = OST.get_track_info(self.album, self.values[0])
                            embed = OST.track_embed(self.album, track) 
                            url = track.get('audio', None)
                            await interaction.message.edit(f'**Album**: {self.album}',embed=embed)   
                            if url is not None:          
                                await play_audio(self.ctx,url )
                            else:
                                await get_angry(self.ctx,'Soundboard Error','Sorry the audio does not exists')
                    


