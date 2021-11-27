from typing import Optional
import nextcord
from nextcord.ext.commands import Context
from nextcord.ui import Select,View,Button,button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu, Member
from nextcord.errors import NotFound




class QuestDropDown(Select):
    def __init__(self, embeds_dict: dict,ctx : Context):
        '''
        initializes Build Option dropdown
        '''
        self.select_options = []
        self.embeds = embeds_dict
        for option in embeds_dict:
            self.select_options.append(SelectOption(label=option))
        self.ctx = ctx

        super().__init__(placeholder='Please select an option!',min_values=1,max_values=1,options=self.select_options)

    async def callback(self, interaction: Interaction):

        if interaction.user == self.ctx.author:
            await interaction.response.edit_message(embed=self.embeds[self.values[0]])




    
        
class QuestView(View):
    def __init__(self, ctx: Context, embeds_dict: dict, *, timeout: Optional[float] = 60):
        self.options = []        
        self.dropdown = QuestDropDown(embeds_dict,ctx)
        self.ctx = ctx
        super().__init__(timeout=timeout)
        self.add_item(self.dropdown)
    

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.ctx.author
    
    async def on_timeout(self):
        self.stop()
        
class AllView(View):
    def __init__(self, ctx: Context, embeds: list, *, timeout: Optional[float] = 60):
        self.options = []        
        self.embeds = embeds
        self.count = len(embeds)-1
        self.page = 0
        self.ctx = ctx
        super().__init__(timeout=timeout)
    

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.ctx.author
    
    @button(label='Next Page', style=nextcord.ButtonStyle.primary)
    async def next(self, button: Button,interaction: Interaction):        
        if self.page < self.count:
            self.page += 1
            await interaction.response.edit_message(embed=self.embeds[self.page])

    @button(label='Previous Page', style=nextcord.ButtonStyle.primary)
    async def previous(self, button: Button,interaction: Interaction):
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.page])

    

    async def on_timeout(self):
        self.stop()
        