import os
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json

class GenshinGuides:
    def __init__(self):
        self.path = f'{os.getcwd()}/guides/'
        self.characters = []
        self.case = self._caseinsensitive()
        self._load_characters()
        
    def _load_characters(self):
        if os.path.exists('characters.json'):
            with open('characters.json','r') as f:
                self.characters = json.load(f)['characters']

    def _caseinsensitive(self):
        temp_ = {}
        for i in self.characters:
            temp_[i.lower()] = i
        return temp_

    def _search(self,name):

        for i in self.case:
            if name.lower() == i:
                return self.case[i]

    def get_supported_option(self,option):
        options_ = ['ast:ascension_talents','bd:builds']
        for i in options_:
            check_ = i.split(":")
            if option in check_:
                return check_[1]
        return None

    def get_build_type(self,filename: str):
        """

        Prettifying build_files name!
        
        _ -> spaces
        dps -> DPS

        """

        text = ''
        if "_" in filename:
            for i in filename.split('.')[0].split("_"):
                if text == '':
                    text += f'{i.capitalize()} '
                else:
                    if 'dps' in i:
                        text += 'DPS'
                    else:
                        text += f'{i.capitalize()}'
        else:
            text = filename.split('.')[0].capitalize()
        return text

        




    def get_files(self,character_name :str,guide: str):
        """
        Searches files in guides/name -> character
        """
        search_results = self._search(character_name)

        #searches the provided name in characters database

        print(f'Character Name {search_results}')
        if os.path.exists(f'{self.path}/{search_results}/'):
            print(f"Path Exists:  {self.path}/{search_results}/")
            option_ = self.get_supported_option(guide)
            print(f'Option selected: {option_}')
            if option_ != None:
                if os.path.exists(f'{self.path}/{search_results}/{option_}'):
                    print(f"Path Exists:  {self.path}/{search_results}/{option_}")
                    files = [f for f in listdir(f'{self.path}/{search_results}/{option_}') if isfile(join(f'{self.path}/{search_results}/{option_}', f))]
                    print(files)
                    return files,f'{self.path}/{search_results}/{option_}'
            else:
                return None,None
        else:
            return None,None

    def create_embeds(self,name,option_):
        files,path = self.get_files(name,option_)
        character = self._search(name)
        option = self.get_supported_option(option_)
        if option != None:
            option_text = ''
            if '_' in option:                
                option = option.split('_')
                for i in option:
                    if option_text == '':
                        option_text += f'{i.capitalize()} and '
                    else:
                        option_text += f'{i.capitalize()} Mats'
            else:
                option_text = option
        print(len(files) == 0)
        check = (files == path == None) and (len(files) == 0)
        print(check)
        if check != True:   
            if (len(files) != 0):         
                files_list = []
                embeds = []
                for i in files:
                    type_ = self.get_build_type(i)
                    files_list.append(discord.File(f'{path}/{i}',filename=i))                
                    embed = discord.Embed(title=f'{character} {option_text}',description=f'**{type_}**',color=0xf5e0d0)
                    embed.set_image(url=f'attachment://{i}')                               
                    print(i)
                    embeds.append(embed)
                return embeds,files_list
            else:
                embed =  discord.Embed(title=f'{character} {option_text}',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
                embed.set_thumbnail(url=f'attachment://sorry.png')
                files_list = [discord.File(f'{self.path}/paimon/sorry.png',filename='sorry.png')]                
                return [embed],files_list
        else:
            embed =  discord.Embed(title=f'{character} {option_text}',description=f'Sorry p-p-paimon could not find anything!\ncontact archons!',color=0xf5e0d0)
            embed.set_thumbnail(url=f'attachment://sorry.png')
            files_list = [discord.File(f'{self.path}/paimon/sorry.png',filename='sorry.png')]
            return [embed],files_list


