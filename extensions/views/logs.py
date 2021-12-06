from typing import Optional
import nextcord
from nextcord.ext.commands import Context
from nextcord.mentions import AllowedMentions
from nextcord.ui import Select,View,Button,button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu, Member
from nextcord.errors import NotFound
from extensions.views.information import NavigatableView
from core.paimon import Paimon



class ExtInformationDropDown(Select):
    def __init__(self, embeds_dict: dict,user : Member, page:int = 1):
        '''
        initializes Information dropdown
        '''
        self.embeds = embeds_dict
        self.page = page
        self.option_list = list(self.embeds.keys())
        self.user = user
        
        super().__init__(placeholder='Please select an option!',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):
        '''
        populates item depending on page
        '''

        self.options = []
        limit = (self.page)*21
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)-1
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-21
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0     
        for page_op in self.option_list[first:limit]:
            self.append_option(SelectOption(label=page_op))    

    async def callback(self, interaction: Interaction):
        if interaction.user == self.user:
            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(ExtInformationDropDown(self.embeds,self.user,self.page-1))   
                await interaction.message.edit('Please select a page from below?',view=view)
            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(ExtInformationDropDown(self.embeds,self.user,self.page+1))   
                    await interaction.message.edit('Please select a page from below?',view=view)     
                else:
                    if interaction.user == self.user:
                        await interaction.response.edit_message(embed=self.embeds[self.values[0]])