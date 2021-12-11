
from typing import Optional
from nextcord.member import Member
from nextcord.message import Message
from nextcord.ui import Select,View,Button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu

from nextcord.errors import NotFound

from core.paimon import Paimon
from base.domains import Domains

from asyncio.exceptions import TimeoutError



class DomainView(Select):
    def __init__(self,pmon: Paimon,domain_handler: Domains,user : Member, day, page: int= 1):
        '''
        initializes Build Option dropdown
        '''

        self.pmon = pmon
        self.domain_handler = domain_handler
        self.dict_ = self.domain_handler.map_area_type_to_domain_details(day)
        self.option_list = list(self.dict_.keys())
        self.page = page
        self.user = user

        super().__init__(placeholder='Choose a character',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):
        '''
        populates item depending on page
        '''

        self.options.clear()
        
        for option_ in self.option_list:
            self.append_option(SelectOption(label=option_))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''

        if interaction.user == self.user:            
            if interaction.response.is_done():
                await interaction.response.edit_message(content=f'Domain schedule')
                message = await interaction.original_message()  
                await message.edit(embed=self.dict_[self.values[0]]['embed'],file=self.dict_[self.values[0]]['image'])
            else:
                await interaction.response.send_message(content=f'Domain schedule')
                message = await interaction.original_message()  
                await message.edit(embed=self.dict_[self.values[0]]['embed'],file=self.dict_[self.values[0]]['image'])

class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()
