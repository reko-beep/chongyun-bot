'''

EMBEDS PATTERN

must be in list

[embed1, embed2, embed3]

'''


from re import A
from nextcord.ui import View, Button, button, Select, Modal, TextInput
from nextcord import Member, Interaction, Message, Embed, ButtonStyle, SelectOption
from nextcord.utils import get
from core.bot import DevBot
import random

from typing import Optional, List, Text


class PaginatorList(View):
    def __init__(self, *, timeout: Optional[float] = 180, user: Member, message: Message, embeds: List[Embed], bot):
        super().__init__(timeout=timeout)
        self.user = user
        self.message = message
        self.embeds = embeds
        self.page = 0
        self.bot : DevBot = bot
        print(self.user.display_name)
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
        print('interaction check', interaction.user.display_name, self.user.display_name)
        if interaction.user == self.user:
            if self.page > 0:
                self.page-= 1   
                self.comp_delete_button()

                await interaction.message.edit(embed=self.embeds[self.page], view=self)

    def comp_delete_button(self):
        for ui_items in self.children:                                
            if hasattr(ui_items, 'cdict'):
                self.remove_item(ui_items)
        if 'team comps' in self.embeds[self.page].title.lower():
            if '-' in self.embeds[self.page].title:
                title = '-'.join(self.embeds[self.page].title.split('-')[1:]).strip()
                comp = self.bot.inf.comp_index(title)      
                print('comp attributes', title, self.bot.inf.generate_id(title), comp)
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
                    self.add_item(CompDelete(self.bot, {'owner': -1}, label='Deleted Comp', disabled=True))
        


    @button(label='Next',style=ButtonStyle.blurple)
    
    async def next(self, button: Button,interaction: Interaction):
        
        print('interaction check', interaction.user.display_name, self.user.display_name)
        if interaction.user == self.user:
            if self.page < len(self.embeds)-1:
                self.page += 1       
                self.comp_delete_button()

                await interaction.message.edit(embed=self.embeds[self.page], view=self)


class DropDownView(View):
    def __init__(self, bot , list_: list, func_, user : Member,page: int= 1):
        self.bot : DevBot = bot
        self.func = None
        self.func_str = func_
        self.option_to_add = list_
        self.page = page
        self.user = user
        self.none = 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Replacement_character.svg/220px-Replacement_character.svg.png'
        self.dropdown = DropdownList(self.bot,self.option_to_add, self.func_str,self.user,self.page)
        super().__init__(timeout=90)
        self.add_item(self.dropdown)
      
    
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        for ui_items in self.children:
            if hasattr(ui_items, 'disabled'):
                ui_items.disabled = True

    @button(label="<", style=ButtonStyle.blurple, custom_id='previous', row=2)
    async def previous(self, button: Button,  interaction: Interaction):
        if self.page > 1:
            self.page -= 1            
            self.clear_dropdown()
            self.dropdown = DropdownList(self.bot, self.option_to_add, self.func_str, self.user, self.page)
            self.add_item(self.dropdown)
        
            self.buttons_disable()
            await interaction.message.edit(interaction.message.content,view=self)
    
    @button(label=">", style=ButtonStyle.blurple, custom_id='next', row=2)
    async def next(self,button: Button, interaction: Interaction):        
        if self.page < divmod(len(self.option_to_add),22)[0]:        
            self.page += 1    
            self.clear_dropdown()
            self.dropdown = DropdownList(self.bot, self.option_to_add, self.func_str, self.user, self.page)        
            self.add_item(self.dropdown)
        
            self.buttons_disable()
            await interaction.message.edit(interaction.message.content,view=self)      

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        for ui_items in self.children:
            if hasattr(ui_items, 'disabled'):
                ui_items.disabled = True


    def clear_dropdown(self):        

        self.remove_item(self.dropdown)

    def buttons_disable(self):
        for i in self.children:
            if isinstance(i, Button):
                if i.custom_id == 'next':
                    if not self.page < divmod(len(self.option_to_add),22)[0]:
                        i.disabled = True
                    else:                        
                        i.disabled = False
            if isinstance(i, Button):
                if i.custom_id == 'previous':
                    if not self.page > 1:
                        i.disabled = True    
                    else:
                        i.disabled = False
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
        self.none = 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Replacement_character.svg/220px-Replacement_character.svg.png'

        super().__init__(placeholder=f"Please select a {self.func_str.split('_')[1]}",min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        
       

        for num in range(1, len(self.option_to_add)+1, 1):
            if ((self.page*22) - 22) < num < self.page*22:                 

                self.append_option(SelectOption(label=self.option_to_add[num]))    
        
        
         

       
       
   



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        
        
        if self.func is not None:
            embeds = self.func(interaction.guild, self.values[0], [], False, False)
            embed_view = PaginatorList(user=self.user, message=interaction.message, embeds=embeds, bot=self.bot)
            await interaction.message.edit('You selected '+self.values[0],embed=embeds[0], view=embed_view) 


class CompDelete(Button):
    def __init__(self, bot, comp_dict, label:str='Delete', disabled:bool = False):
        
        self.index = 0
        self.cdict = comp_dict
        self.bot : DevBot = bot
        self.owner = comp_dict['owner']
        super().__init__(style=ButtonStyle.danger, label=label, disabled=disabled)
      

    async def callback(self, interaction: Interaction):

        if interaction.user.id == self.owner:
            index_ = self.bot.inf.comp_index(self.cdict['title'])
            if index_ is not None:
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


class LibenBox(View):
    def __init__(self, bot: DevBot, user: Member, msg:Message, box):
        super().__init__(timeout=60)

        self.box = box
        self.bot = bot
        self.user = user
        self.message = msg
    
    @button(label='Claim',style=ButtonStyle.green, emoji='✔️')
    async def claim(self, button: Button,interaction: Interaction):
        if interaction.user == self.user:
            member = get(interaction.guild.members,id=int(self.box['member']))
            if member is not None:
                check = self.bot.coop.liben.add_claimed('✅', member, self.box['region'], self.box['box'], self.user)
                if check:                    
                    embed = self.bot.coop.liben.get_random_box_embed(interaction.guild, self.box)
                    self.disable_all()
                    await interaction.message.edit(embed=embed, view=self)


    def disable_all(self):
        for i in self.children:
            if hasattr(i, 'disabled'):
                i.disabled = True

  
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        for ui_items in self.children:
            if hasattr(ui_items, 'disabled'):
                ui_items.disabled = True
        await self.message.edit(view=self)



class ApproveForm(Modal):
    def __init__(self, bot: DevBot, user: Member):
        super().__init__('Member Approval Form', timeout=90)
        self.bot = bot
        self.user = user

        self.from_where = TextInput(label='Where are you from?', placeholder='City , Country, or location!', required=True)
        self.add_item(self.from_where)

        self.invite_where = TextInput(label='Where you got the invite from?', placeholder='Disboard or friends name!', required=True)
        self.add_item(self.invite_where)

    async def callback(self, interaction: Interaction):
        embed = Embed(title=f'Approval form', color=self.bot.resource_manager.get_color_from_image(self.user.display_avatar.url))
        embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)
        w_t = 'N/A' if self.from_where.value is None else self.from_where.value
        embed.add_field(name=f"{self.user.display_name.title()} is from", value=w_t, inline=False)
        i_t = 'N/A' if self.invite_where.value is None else self.invite_where.value
        embed.add_field(name=f"{self.user.display_name.title()} got the invite from", value=i_t, inline=False)

        await interaction.response.send_message(embed=embed, view=ApprovalView(self.bot, self.user))


class ApprovalView(View):
    def __init__(self, bot : DevBot, user: Member):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @button(label='Approve',style=ButtonStyle.green, emoji='✔️')
    async def claim(self, button: Button,interaction: Interaction):
        if self.bot.admin.check_admin(interaction.user):
            print(self.user)
            check = await self.bot.admin.approve_member(interaction.user, self.user)
            print('Form', check)
            self.disable_all()
            if check is True:
                embed = Embed(title='Member approved', color=self.bot.resource_manager.get_color_from_image(self.user.display_avatar.url))
                embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)
                await interaction.response.send_message(embed=embed)
            if check is None:
                embed = Embed(title='Member Error',description='Not enough perms!', color=self.bot.resource_manager.get_color_from_image(self.user.display_avatar.url))
                embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)
                await interaction.response.send_message(embed=embed)
            if check is False:
                embed = Embed(title='Member Error',description='Member is already approved!', color=self.bot.resource_manager.get_color_from_image(self.user.display_avatar.url))
                embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)
                await interaction.response.send_message(embed=embed)

    def disable_all(self):
        for i in self.children:
            if hasattr(i, 'disabled'):
                i.disabled = True