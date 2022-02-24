from typing import Optional
import nextcord
from nextcord.ext.commands import Context
from nextcord.mentions import AllowedMentions
from nextcord.ui import Select,View,Button,button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu, Member
from nextcord.errors import NotFound
from base.information import GenshinInformation

from core.paimon import Paimon




class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()

class AllList(Select):
    def __init__(self,pmon: Paimon, inf_handler: GenshinInformation, option: str, user : Member,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''
        self.information_handler = inf_handler
        self.pmon = pmon
        self.allowed_options = self.information_handler.get_options()
        self.option_type = option
        if self.option_type != '' and self.option_type in self.allowed_options:
            self.option_list = self.information_handler.get_names_list(option)
        else:
            self.option_list = self.information_handler.get_options()
        self.page = page
        self.user = user
       

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*22
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)-1
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-22
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
        if interaction.user == self.user:

            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(AllList(self.pmon,self.information_handler,self.option_type,self.user,self.page-1))   
                await interaction.message.edit('Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(AllList(self.pmon,self.information_handler,self.option_type,self.user,self.page+1))   
                    await interaction.message.edit('Please select a option from below?',view=view)      

                else: 
                    if self.values[0] in self.allowed_options:                    
                        view = NavigatableView(self.user)
                        view.add_item(AllList(self.pmon,self.information_handler,self.values[0],self.user))   
                        await interaction.message.edit(content=f'Please select a {self.values[0]} from below?',view=view)  
                    else:
                        view = NavigatableView(self.user)
                        if self.option_type in ['Bows','Claymores','Catalysts','Swords','Polearms']:
                            embeds = self.information_handler.create_weapon_embeds(self.option_type.lower(),self.values[0])
                            view.add_item(InformationDropDown(embeds,self.user))   
                            await interaction.message.edit(f'Please select a a option for {self.values[0]} from below?',view=view)
                            
                        if self.option_type == 'Artifacts':
                            embeds = self.information_handler.create_artifact_embeds(self.option_type.lower(),self.values[0])
                            view.add_item(InformationDropDown(embeds,self.user))   
                            await interaction.message.edit(f'Please select a option for {self.values[0]} from below?',view=view)
                            
                        if self.option_type == 'Characters':
                            embeds = self.information_handler.create_character_embeds(self.option_type.lower(),self.values[0])
                            view.add_item(InformationDropDown(embeds,self.user))   
                            await interaction.message.edit(f'Please select a option for {self.values[0]} from below?',view=view)
                            


class InformationDropDown(Select):
    def __init__(self, embeds_dict: dict,user : Member):
        '''
        initializes Information dropdown
        '''
        self.select_options = []
        self.embeds = embeds_dict
        for option in embeds_dict:
            self.select_options.append(SelectOption(label=option))
        self.user = user

        super().__init__(placeholder='Please select an option!',min_values=1,max_values=1,options=self.select_options)

    async def callback(self, interaction: Interaction):

        if interaction.user == self.user:
            await interaction.response.edit_message(embed=self.embeds[self.values[0]])
