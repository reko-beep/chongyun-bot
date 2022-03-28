'''

EMBEDS PATTERN

must be in list

[embed1, embed2, embed3]

'''


from nextcord.ui import View, Button, button
from nextcord import Member, Interaction, Message, Embed, ButtonStyle

from typing import Optional, List


class PaginatorList(View):
    def __init__(self, *, timeout: Optional[float] = 180, user: Member, message: Message, embeds: List[Embed]):
        super().__init__(timeout=timeout)
        self.user = user
        self.message = message
        self.embeds = embeds
        self.page = 0

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        for ui_items in self.children:
            if hasattr(ui_items, 'disabled'):
                ui_items.disabled = True
        await self.message.edit(view=self)
    
    @button(label='Previous',style=ButtonStyle.blurple)
    async def previous(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.page > 0:
                self.page-= 1                            
                await interaction.message.edit(embed=self.embeds[self.page])

    @button(label='Next',style=ButtonStyle.blurple)
    async def next(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.page < len(self.embeds)-1:
                self.page += 1                                 
                await interaction.message.edit(embed=self.embeds[self.page])