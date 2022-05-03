'''

EMBEDS PATTERN

must be in list

[embed1, embed2, embed3]

'''


from re import A
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
            else:
                 self.add_item(CompDelete(self.bot, comp_selected, label='Deleted Comp', disabled=True))


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
                        embeds = self.func(interaction.guild, self.values[0], [], False, False, interaction.guild)
                        embed_view = PaginatorList(user=self.user, message=interaction.message, embeds=embeds, bot=self.bot)
                        await interaction.message.edit(self.values[0] + 'selected',embed=embeds[0], view=embed_view) 


class CompDelete(Button):
    def __init__(self, bot, comp_dict, label:str='Delete', disabled:bool = False):
        
        self.index = 0
        self.cdict = comp_dict
        self.bot : DevBot = bot
        self.owner = comp_dict['owner']
        super().__init__(style=ButtonStyle.danger, label=label, disabled=disabled)
      

    async def callback(self, interaction: Interaction):

        if interaction.user.id == self.owner:
            index_ = self.bot.inf.teamcomps['data'].index(self.cdict)
            self.bot.inf.delete_comp(index_ )
            self.disabled = True
            embed = interaction.message.embeds[0].set_footer(text='This team comp is now deleted!')
            file = interaction.message.attachments
            await interaction.message.edit(embed=embed,attachments=file,view=self.view)


class SwitchPaginator(View):
    def __init__(self, user: Member, embeds: dict, message: Message):
       
        super().__init__(timeout=180.0)
        self.user = user
        self.embeds = embeds
        self.message = message
        self.index = 1

        self.main_embed = list(self.embeds.keys())[0]
        self.switcher = self.main_embed
        for button in self.embeds:
            self.add_item(SwitchButton(self, ButtonStyle.blurple, button.replace("_"," ",99).title(), False))
    
    
    @button(label='Previous',style=ButtonStyle.blurple)
    async def previous(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.index > 0:
                self.index -= 1   
                

                await interaction.message.edit(embed=self.embeds[self.switcher][self.index], view=self)

  


    @button(label='Next',style=ButtonStyle.blurple)
    async def next(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.index < len(self.embeds[self.switcher]):
                self.index += 1                   
                await interaction.message.edit(embed=self.embeds[self.switcher][self.index], view=self)


class SwitchButton(Button):
    def __init__(self, view: SwitchPaginator, button_style: ButtonStyle, label: str, disabled: bool):
        super().__init__(style=button_style, label=label,  disabled=disabled)
        self.view_ = view
    
    async def callback(self, interaction: Interaction):

        if interaction.user == self.view_.user:
            if self.view_.index > len(self.view_.embeds[self.label.lower()])-1:
                embed = self.view_.embeds[self.label.replace(" ","_",99).lower()][-1]
                self.view_.switcher = self.label.replace(" ","_",99).lower()
                await self.view_.message.edit(embed=embed,view=self.view_)
            else:
                embed = self.view_.embeds[self.label.replace(" ","_",99).lower()][self.view_.index]
                self.view_.switcher = self.label.replace(" ","_",99).lower()
                await self.view_.message.edit(embed=embed,view=self.view_)
            
            


class BookmarkList(View):
    def __init__(self, *, timeout: Optional[float] = 180, user: Member, bookmark_user: Member,  message: Message, embeds: List[Embed], bot):
        super().__init__(timeout=timeout)
        self.user = user
        self.message = message
        self.embeds = embeds
        self.bu = bookmark_user
        self.page = 0
        self.bot : DevBot = bot

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
                self.bk_button(interaction.user)
                embed = self.bot.inf.bookmark.create_bookmark_embed(self.bu, self.embeds[self.page])
                await interaction.message.edit(embed=embed, view=self)

    def bk_button(self, user):
        if user.id == self.embeds[self.page]['owner']:   
            for ui_items in self.children:
                if hasattr(ui_items, 'cdict'):
                    self.remove_item(ui_items)
            exist = self.bot.inf.bookmark.if_bookmark_exists(self.bu, self.page)
            if exist:                  
                self.add_item(BKDelete(self.bot, self.embeds[self.page], label='Delete'))
            else:
                self.add_item(BKDelete(self.bot, self.embeds[self.page], label='Deleted', disabled=True))



    @button(label='Next',style=ButtonStyle.blurple)
    async def next(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            if self.page < len(self.embeds)-1:
                self.page += 1       
                self.bk_button(interaction.user)                
                embed = self.bot.inf.bookmark.create_bookmark_embed(self.bu, self.embeds[self.page])
                await interaction.message.edit(embed=embed, view=self)


class BKDelete(Button):
    def __init__(self, bot, comp_dict, label:str='Delete', disabled:bool = False):
        
        self.index = 0
        self.cdict = comp_dict
        self.bot : DevBot = bot
        self.owner = comp_dict['owner']
        super().__init__(style=ButtonStyle.danger, label=label, disabled=disabled)
      

    async def callback(self, interaction: Interaction):

        if interaction.user.id == self.owner:
            index_ = self.cdict['index']
            self.bot.inf.bookmark.remove_bookmark(interaction.user, index_)
            self.disabled = True
            embed = interaction.message.embeds[0].set_footer(text='This bookmark is now deleted!')
            file = interaction.message.attachments
            await interaction.message.edit(embed=embed,attachments=file,view=self.view)
