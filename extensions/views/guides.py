
from typing import Optional
from nextcord.member import Member
from nextcord.ui import Select,View,Button
from nextcord import SelectOption, Interaction,InteractionMessage, SelectMenu

from nextcord.errors import NotFound

from core.paimon import Paimon
from base.guides import GenshinGuides



class BuildOptions(Select):
    def __init__(self,pmon: Paimon,guide_handler: GenshinGuides,user : Member,page: int= 1):
        '''
        initializes Build Option dropdown
        '''

        self.pmon = pmon
        self.guide_handler = guide_handler
        self.page = page
        self.user = user

        super().__init__(placeholder='Choose a character',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):
        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*24
        print(len(self.pmon.p_bot_config['characters'])-1,limit)
        if limit > len(self.pmon.p_bot_config['characters'])-1:
            limit = len(self.pmon.p_bot_config['characters'])-1
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-24
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0     
        print(first)
        for character in self.pmon.p_bot_config['characters'][first:limit]:
            self.append_option(SelectOption(label=character))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''

        if interaction.user == self.user:
            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(BuildOptions(self.pmon,self.guide_handler,self.user,self.page-1))   
                await interaction.message.edit('Please select a character from below?',view=view)
            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(BuildOptions(self.pmon,self.guide_handler,self.user,self.page+1))   
                    await interaction.message.edit('Please select a character from below?',view=view)                            
                else:  

                    embeds,files = self.guide_handler.create_embeds('b',self.values[0])  
                    
                    if interaction.response.is_done():
                        await interaction.response.edit_message(content=f'Builds for {self.values[0]}')
                        message = await interaction.original_message()  
                        await message.edit(embeds=embeds,files=files)
                    else:
                        await interaction.response.send_message(content=f'Builds for {self.values[0]}')
                        message = await interaction.original_message()  
                        await message.edit(embeds=embeds,files=files)
                    
                    
           
          
class AscensionOptions(Select):
    def __init__(self,pmon: Paimon,guide_handler: GenshinGuides,user : Member,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        self.pmon = pmon
        self.guide_handler = guide_handler
        self.page = page
        self.user = user

        super().__init__(placeholder='Choose a character',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*24
        print(len(self.pmon.p_bot_config['characters'])-1,limit)
        if limit > len(self.pmon.p_bot_config['characters'])-1:
            limit = len(self.pmon.p_bot_config['characters'])-1
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-24
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0     
        print(first)
        for character in self.pmon.p_bot_config['characters'][first:limit]:
            self.append_option(SelectOption(label=character))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.user:

            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(AscensionOptions(self.pmon,self.guide_handler,self.user,self.page-1))   
                await interaction.message.edit('Please select a character from below?',view=view)

            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(AscensionOptions(self.pmon,self.guide_handler,self.user,self.page+1))   
                    await interaction.message.edit('Please select a character from below?',view=view)      

                else:  

                    embeds,files = self.guide_handler.create_embeds('as',self.values[0])  
                    
                    if interaction.response.is_done():
                        await interaction.response.edit_message(content=f'Builds for {self.values[0]}')
                        message = await interaction.original_message()  
                        await message.edit(embeds=embeds,files=files)
                    else:
                        await interaction.response.send_message(content=f'Builds for {self.values[0]}')
                        message = await interaction.original_message()  
                        await message.edit(embeds=embeds,files=files)

class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()