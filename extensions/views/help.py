from typing import Optional
from nextcord import Embed
from nextcord.ext.commands import Context
from nextcord.ui import Select,View
from nextcord import SelectOption, Interaction, Member
from nextcord.errors import NotFound

from os import getcwd
from json import load
from core.paimon import Paimon



class NavigatableView(View):
    def __init__(self, user : Member, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.user = user
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.user

    async def on_timeout(self) -> None:
        self.stop()

with open(f'{getcwd()}/assets/GenshinHelp/help.json','r') as f:
    data = load(f)


def create_embed(dict_ , member: Member):
    if 'commands' in dict_:
        commands = dict_['commands']
    name = dict_['name']
    description = dict_['description']
    embed = Embed(title=f'{name} Commands',description=description,color=0xf5e0d0)  
    for command in commands:
        aliases = f"Aliases: ``{','.join(command['aliases'])} ``"
        description = command['description']
        embed.add_field(name=f"{command['name']}", value=f"{aliases}\n__**{description}**__")
    embed.set_author(name=member.display_name,icon_url=member.avatar.url)
    embed.set_thumbnail(url='https://i.imgur.com/qb0Zjiv.gif')
    return embed






class HelpList(Select):
    def __init__(self,pmon: Paimon, user : Member,page: int= 1):
        '''
        initializes Ascension Option dropdown
        '''

        self.pmon = pmon
        self.option_list = list(data.keys())
        self.page = page
        self.user = user
       

        super().__init__(placeholder='Choose a option',min_values=1,max_values=1)
        self.populate_items()

    def populate_items(self):

        '''
        populates item depending on page
        '''

        self.options.clear()
        limit = (self.page)*21
        if limit > len(self.option_list)-1:
            limit = len(self.option_list)
        else:
            self.append_option(SelectOption(label='Next'))

        first = limit-21
        if first > 0:
            self.append_option(SelectOption(label='Previous'))
            pass
        else:
            first = 0   
        for option in self.option_list[first:limit]:
            self.append_option(SelectOption(label=option))    



    async def callback(self, interaction: Interaction):
        '''
            previous, next and build interactions
        '''
        if interaction.user == self.user:

            if self.values[0] == 'Previous':             
                view = NavigatableView(self.user)
                view.add_item(HelpList(self.pmon,self.option_type,self.user,self.page-1))   
                await interaction.message.edit('Please select a option from below?',view=view)

            else:

                if self.values[0] == 'Next':         
                    view = NavigatableView(self.user)
                    view.add_item(HelpList(self.pmon,self.option_type,self.user,self.page+1))   
                    await interaction.message.edit('Please select a option from below?',view=view)      
                else:                     
                    view = NavigatableView(self.user)
                    embed = create_embed(data[self.values[0]], self.user)
                    await interaction.message.edit('Select a module from below!',embed=embed,view=self.view)
                        
                     

