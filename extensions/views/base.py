from typing import Optional
import nextcord
from nextcord import member, Interaction
from nextcord.embeds import Embed
from nextcord.ext.commands import Context
from nextcord.mentions import AllowedMentions
from nextcord.ui import Select,View,Button,button
from nextcord.errors import NotFound
from nextcord.ui.select import select
from nextcord.utils import get


from core.paimon import Paimon





class EmbedView(View):
    def __init__(self, pmon: Paimon, ctx: Context, embeds_list: list, index: int):        
        self.pmon = pmon
        self.index = index       
        self.user = ctx.author
        self.embeds = embeds_list
        self.file = False        
        if type(self.embeds[0]) == dict:
            self.file = True

        super().__init__(timeout=60)

    

    @button(label='Previous',style=nextcord.ButtonStyle.blurple)
    async def previous(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.index > 0:
                self.index -= 1                            
                await interaction.message.edit(embed=self.embeds[self.index])

    @button(label='Next',style=nextcord.ButtonStyle.blurple)
    async def next(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.index < len(self.embeds)-1:
                self.index += 1                                 
                await interaction.message.edit(embed=self.embeds[self.index])

    