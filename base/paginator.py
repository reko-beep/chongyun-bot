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
    def __init__(self, *, timeout: Optional[float] = 180, user: Member, message: Message, embeds: List[Embed], bot):
        super().__init__(timeout=timeout)
        self.user = user
        self.message = message
        self.embeds = embeds
        self.page = 0
        self.bot : DevBot = bot
        self.comp_delete_button()
        

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
                self.comp_delete_button()

                await interaction.message.edit(embed=self.embeds[self.page], view=self)

    def comp_delete_button(self):
        if 'team comps' in self.embeds[self.page].title.lower():
            title = self.embeds[self.page].title.split('-')[1].strip()
            comp = self.bot.inf.comp_index(title)
            
            
            if comp is not None:
                comp_selected = self.bot.inf.teamcomps['data'][comp]
                print('selected comp', comp_selected, comp_selected['owner'])
                if comp_selected['owner'] == self.user.id:
                    self.add_item(CompDelete(self.bot, comp_selected))
                else:
                    for ui_items in self.children:                                
                        if hasattr(ui_items, 'cdict'):
                            self.remove_item(ui_items) 


    @button(label='Next',style=ButtonStyle.blurple)
    async def next(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.page < len(self.embeds)-1:
                self.page += 1       
                self.comp_delete_button()

                await interaction.message.edit(embed=self.embeds[self.page], view=self)

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
                        embeds = self.func(self.values[0], [], False, False)
                        embed_view = PaginatorList(user=self.user, message=interaction.message, embeds=embeds, bot=self.bot)
                        await interaction.message.edit(self.values[0] + 'selected',embed=embeds[0], view=embed_view) 


class CompDelete(Button):
    def __init__(self, bot, comp_dict):
        
        self.index = 0
        self.cdict = comp_dict
        self.bot : DevBot = bot
        self.owner = comp_dict['owner']
        super().__init__(style=ButtonStyle.danger, label='Delete')
      

    async def callback(self, interaction: Interaction):

        if interaction.user.id == self.owner:
            index_ = self.bot.inf.teamcomps['data'].index(self.cdict)
            self.bot.inf.delete_comp(index_ )
            self.disabled = True
            embed = interaction.message.embeds[0].set_footer(text='This team comp is now deleted!')
            file = interaction.message.attachments
            await interaction.message.edit(embed=embed,attachments=file,view=self.view)