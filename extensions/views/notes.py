from typing import Optional
import nextcord
from nextcord import member
from nextcord.embeds import Embed
from nextcord.ext.commands import Context
from nextcord.mentions import AllowedMentions
from nextcord.ui import Select,View,Button,button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu, Member
from nextcord.errors import NotFound
from nextcord.ui.select import select
from nextcord.utils import get
from base.information import GenshinInformation

from core.paimon import Paimon

from base.notes import GuidesNotes




class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()

class AllList(Select):
    def __init__(self,pmon: Paimon, notes_handler: GuidesNotes,type: str, member: Member, character : str='',  user : str='', index: int = -1 ,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        

        self.pmon = pmon
        self.notes_handler = notes_handler
        self.option_type = type
        self.character = character
        self.page = page
        self.user = user
        self.member = member
        self.done = False
        self.select_index = ['characters','users','notes']
        if self.option_type == 'characters':
            self.option_list = self.notes_handler.get_available_characternotes()
        if self.option_type == 'users':
            self.option_list = self.notes_handler.get_available_usernotes(self.character)
        if self.option_type == 'notes':
            self.option_list = self.notes_handler.get_available_notes(self.character, self.user)
        self.index = index
        self.guild = self.pmon.guilds[0]
        
        

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''
        if len(self.option_list) == 0:
            self.append_option(SelectOption(label='Nothing Found'))
        else:

            if self.option_type == 'characters':
                self.options.clear()
                limit = (self.page)*24
                if limit > len(self.option_list):
                    limit = len(self.option_list)                
                else:
                    self.append_option(SelectOption(label='Next'))

                first = limit-24
                if first > 0:
                    self.append_option(SelectOption(label='Previous'))
                    pass
                else:
                    first = 0  
                if limit == 0:
                    for option in self.option_list:
                        
                        self.append_option(SelectOption(label=option))  
                else:
                    for option in self.option_list[first:limit]:
                        
                        self.append_option(SelectOption(label=option))  
            if self.option_type == 'notes':
                self.options.clear()
                limit = (self.page)*24
                if limit > len(self.option_list):
                    limit = len(self.option_list)
                else:
                    self.append_option(SelectOption(label='Next'))

                first = limit-24
                if first > 0:
                    self.append_option(SelectOption(label='Previous'))
                    pass
                else:
                    first = 0               
                if limit == 0:
                    for option in self.option_list:
                        index_ = self.notes_handler.get_note_index(self.character,self.user,option)
                    self.append_option(SelectOption(label=option[:75],value=index_))    
                else:     
                    for option in self.option_list[first:limit]:
                        index_ = self.notes_handler.get_note_index(self.character,self.user,option)
                        self.append_option(SelectOption(label=option[:75],value=index_))                  
            if self.option_type == 'users':
                self.options.clear()
                limit = (self.page)*24
                if limit > len(self.option_list):
                    limit = len(self.option_list)
                else:
                    self.append_option(SelectOption(label='Next'))

                first = limit-24
                if first > 0:
                    self.append_option(SelectOption(label='Previous'))
                    pass
                else:
                    first = 0    
                
                if limit == 0:           
                    for option in self.option_list:
                        index_ = option
                        user_ = get(self.guild.members,id=int(index_))
                        self.append_option(SelectOption(label=user_.display_name,value=index_))  
                else:
                    for option in self.option_list[first:limit]:
                        index_ = option
                        user_ = get(self.guild.members,id=int(index_))
                        self.append_option(SelectOption(label=user_.display_name,value=index_))  
                

    def next_select(self, option: str):
        index_ = 0
        try:
            index_ = self.select_index.index(option)
            if index_ < len(self.select_index):
                index_ += 1
            else:
                index_ = 0
        except ValueError:
            index_ = 0
        return index_


    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.member:
            if self.values[0] == 'Previous':             
                view = NavigatableView(self.member)
                view.add_item(AllList(self.pmon,self.notes_handler,self.option_type,self.member,self.character,self.user,self.index,self.page-1))   
                await interaction.message.edit(content='Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.member)
                    view.add_item(AllList(self.pmon,self.notes_handler,self.option_type,self.member,self.character,self.user,self.index,self.page+1))   
                    await interaction.message.edit(content='Please select a option from below?',view=view)      

                else: 

                    if self.option_type == 'characters':
                        self.option_type = self.select_index[self.next_select(self.option_type)]                        
                        view = NavigatableView(self.member)
                        view.add_item(AllList(self.pmon,self.notes_handler,self.option_type,self.member,self.values[0],self.user,self.index,1))   
                        await interaction.message.edit(content='Please select a user from below?',view=view) 
                        self.done = True  
                    if self.option_type == 'users' and self.done == False:
                        self.option_type = self.select_index[self.next_select(self.option_type)]
                        view = NavigatableView(self.member)
                        view.add_item(AllList(self.pmon,self.notes_handler,self.option_type,self.member,self.character,self.values[0],self.index,1))   
                        await interaction.message.edit(content='Please select a note from below?',view=view)  
                        self.done = True 
                    if self.option_type == 'notes'and self.done == False:
                        embed = self.notes_handler.create_note_embed(self.character,self.user,int(self.values[0]))
                        view = NoteView(self.pmon,self.notes_handler,self.member,self.character,self.user,int(self.values[0]))
                        await interaction.message.edit(content='Note',embed=embed,view=view)   
                        self.done = True



class NoteView(View):
    def __init__(self, pmon: Paimon, notes_handler: GuidesNotes, user : Member, character_name: str, creator_id: str, index: int):
        '''
        initializes Note View
        '''
        self.pmon = pmon
        self.index = index       
        self.user = user
        self.creator_id = creator_id
        self.character = character_name
        self.notes_handler = notes_handler

        super().__init__(timeout=60)

  

    @button(label='Delete',style=nextcord.ButtonStyle.red)
    async def delete(self, button: Button,interaction: Interaction):
        if interaction.user.id == int(self.creator_id):
            embed = self.notes_handler.delete_note_embed(self.character,self.creator_id,self.index)
            self.notes_handler.remove_note(self.character,self.creator_id,self.index)
            button.disabled = True
            await interaction.response.edit_message(content='Note removed!',embed=embed,view=self)
            self.stop()
        else:
            await interaction.response.send_message(content='You didnot add this note!',ephemeral=True)
            
        

class NoteAdd(Select):
    def __init__(self,pmon: Paimon, notes_handler: GuidesNotes, member: Member,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        self.pmon = pmon     
        self.page = page
        self.notes_handler = notes_handler
        self.member = member
        
        self.option_list = self.pmon.p_bot_config['characters']     
        self.guild = self.pmon.guilds[0]
        
        

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''
        
        self.options.clear()
        limit = (self.page)*24
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)-1
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-24
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
        if interaction.user == self.member:
            if self.values[0] == 'Previous':             
                view = NavigatableView(self.member)
                view.add_item(NoteAdd(self.pmon,self.member,self.page-1))   
                await interaction.response.edit_message(content='Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.member)
                    view.add_item(NoteAdd(self.pmon,self.member,self.page+1))   
                    await interaction.response.edit_message(content='Please select a option from below?',view=view)      

                else: 
                    user = self.member.id
                    self.disabled = True
                    await interaction.response.edit_message(content=f'Please write the note below for {self.values[0]}',view=self.view)   
                    
                    try:
                        def check(message):
                            return message.channel.id == interaction.message.channel.id and message.author == self.member
                        msg = await self.pmon.wait_for('message',
                                            check=check,
                                            timeout=60)
                    except TimeoutError:
                        self.disabled = True
                    else:
                        embed = Embed(title=f'{self.member.display_name} note written for {self.values[0]} added!',description=msg.content, color=0xf5e0d0)
                        embed.set_author(name=self.member.display_name,
                                        icon_url=self.member.avatar.url)
                        embed.set_thumbnail(url='https://i.imgur.com/YlujvnT.gif')
                        note_ = self.notes_handler.add_note(self.values[0],str(user),msg.content)
                        await msg.delete()
                        await interaction.message.channel.send(content='Added!',embed=embed)
                   

