'''

EMBEDS PATTERN

must be in list

[embed1, embed2, embed3]

'''


from nextcord.ui import View, Button, button, Select
from nextcord import Member, Interaction, Message, Embed, ButtonStyle, SelectOption
from core.bot import DevBot

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

class DropdownList(Select):
    def __init__(self, bot , list_: list, func_, user : Member,page: int= 1):
       
        self.bot : DevBot = bot
        self.func = None
        self.func_str = func_

        if hasattr(self.bot.inf, func_):
            self.func = self.bot.inf.__getattribute__(func_)

        self.option_to_add = list_
        self.page = page
        self.user = user
       

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()

        for num in range(1, len(self.option_to_add)+1, 1):
            if ((self.page*22) - 22) < num < self.page*22:
                self.append_option(SelectOption(label=self.option_to_add[num]))    
        
        if self.page < divmod(len(self.option_to_add),22)[0]:
            self.append_option(SelectOption(label='Next'))

        
        if self.page > 1:
            self.append_option(SelectOption(label='Previous'))
        

       
       
            



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.user:

            if self.values[0] == 'Previous':             
                self.view.clear_items()
                self.view.add_item(DropdownList(self.bot,self.option_to_add, self.func_str,self.user,self.page-1))   
                await interaction.message.edit(interaction.message.content,view=self.view)

            else:

                if self.values[0] == 'Next':         
                    self.view.clear_items()
                    self.view.add_item(DropdownList(self.bot,self.option_to_add, self.func_str,self.user,self.page+1))   
                    await interaction.message.edit(interaction.message.content,view=self.view)      

                else: 
                    if self.func is not None:
                        embeds = self.func(self.values[0], [], False)
                        embed_view = PaginatorList(user=self.user, message=interaction.message, embeds=embeds)
                        await interaction.message.edit(self.values[0] + 'selected',embed=embeds[0], view=embed_view) 