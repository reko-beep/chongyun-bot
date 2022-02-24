
from typing import Optional
from nextcord.member import Member
from nextcord.message import Message
from nextcord.ui import Select,View,Button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu, ButtonStyle

from nextcord.errors import NotFound

from core.paimon import Paimon
from base.information import GenshinInformation

from asyncio.exceptions import TimeoutError

class TeampComps(Select):
    def __init__(self,pmon: Paimon,info_handler: GenshinInformation,comps_list: list, user : Member,page: int= 1):
        '''
        initializes Build Option dropdown
        '''

        self.pmon = pmon
        self.info_handler = info_handler
        self.page = page
        self.user = user
        self.comps_list = [c for c in comps_list if c is not None]
        print(self.comps_list)

        super().__init__(placeholder='Choose a team comp',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):
        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*24
        if limit > len(self.comps_list)-1:
            limit = len(self.comps_list)
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-24
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0     
        for comp in self.comps_list[first:limit]:
            print(comp['title'], self.comps_list.index(comp))
            self.append_option(SelectOption(label=comp['title'], value=self.comps_list.index(comp)))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        button_ = False
        if interaction.user == self.user:
            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(TeampComps(self.pmon,self.info_handler,self.comps_list,self.user,self.page-1))   
                await interaction.message.edit('Please select a team comp from below?',view=view)
            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(TeampComps(self.pmon,self.info_handler,self.comps_list,self.user,self.page+1))   
                    await interaction.message.edit('Please select a team comp from below?',view=view)                            
                else:  
                    print(self.comps_list[int(self.values[0])])
                    embed,file = self.info_handler.create_embed_comp(self.comps_list[int(self.values[0])])
                    view_ = None
                    comp_role = self.info_handler.get_comprole()
                    role_check = (len(set([comp_role.id]).intersection([r.id for r in self.user.roles])) !=0)
                    if self.comps_list[int(self.values[0])].get('owner', None) is not None:
                        if self.comps_list[int(self.values[0])].get('owner', None) == self.user.id:
                            view_ = NavigatableView(self.user)
                            view_.add_item(DeleteButton(self.info_handler, self.user, self.comps_list[int(self.values[0])]))
                            button_ = True
                        else:
                            if role_check:
                                view_ = NavigatableView(self.user)
                                view_.add_item(DeleteButton(self.info_handler, self.user, self.comps_list[int(self.values[0])]))
                                button_ = True

                    if interaction.response.is_done():
                        await interaction.response.edit_message(content=f"{self.comps_list[int(self.values[0])]['title']}")
                        message = await interaction.original_message()  
                        if button_ and view_ is not None:
                            await message.edit(embed=embed,file=file,view=view_)
                        else:
                            await message.edit(embed=embed,file=file)

                    else:
                        await interaction.response.send_message(content=f"{self.comps_list[int(self.values[0])]['title']}")
                        message = await interaction.original_message()  
                        await message.edit(embed=embed,file=file)
                        if button_ and view_ is not None:
                            await message.edit(embed=embed,file=file,view=view_)
                        else:
                            await message.edit(embed=embed,file=file)


class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool: 
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()

class DeleteButton(Button):
    def __init__(self, inf_handler: GenshinInformation, user,  comp_dict):
        self.comp_index = comp_dict
        self.author_ = user
        self.inf_handler = inf_handler
        super().__init__(style=ButtonStyle.red, label='Delete')
    

    async def callback(self, interaction: Interaction):

        if interaction.user == self.author_:
            self.inf_handler.delete_comp(self.comp_index)
            self.disabled = True
            embed = interaction.message.embeds[0].set_footer(text='This team comp is now deleted!')
            file = interaction.message.attachments
            await interaction.message.edit(embed=embed,attachments=file,view=self.view)