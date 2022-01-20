from json import dump, load
from os import getcwd
from os.path import exists
from typing import *
from nextcord import File, Embed

class Fishing:
    def __init__(self):
        self.file = getcwd() + '/assets/fishing.json'
        self.base_path = getcwd() + '/assets/fishing_points'
        self.base_url = 'https://raw.githubusercontent.com/reko-beep/paimon-bot/main/assets/fishing_points/{city}/{file}?raw=true'
        self.data = {}
        self.load()

    def load(self):

        if exists(self.file):

            with open(self.file, 'r') as f:
                self.data = load(f)
    

    def remove_seps(self, fish_name: str):

        seps = ['-','/','!','_',':', ';', '[', ']']

        for s in seps:

            fish_name = fish_name.replace(s, ' ',99)
        
        return fish_name

    def search_fish(self, fish_name: str) -> List[Dict]:

        search_list = []
        name = ''
        if bool(self.data):

            for city in self.data:

                for loc in self.data[city]:

                    fishes = [self.remove_seps(l['name']) for l in loc['fishes']]

                    for fish in fishes:
                        if fish_name.lower() in fish.lower():
                            name = fish

                            search_list.append({
                                **{'city': city}, **loc
                            })
        
        return search_list, name



    def get_path(self, loc_dict: dict):

        if 'file' in loc_dict:

            filename = loc_dict['file']

            city = loc_dict['city']

            #return self.base_path + '/' + city + '/' + filename

            return self.base_url.format(city=city, file=filename)

    def create_embeds(self, search_fish: str):
        
        list_locs, name_fish = self.search_fish(search_fish)


        embeds = []

        for item in list_locs:

            #file = self.get_path(item)
            #name = file.split('/')[-1]
            embed = Embed(title= f"{name_fish} | {item.get('city')}",
                            description=f"**{item.get('location')}**\n{item.get('description','could not find any description!')}",
                            color=0xf5e0d0) 
            embed.set_image(url= self.get_path(item))
            #embed.set_image(url=f'attachment://{name}')
            #sent_file = File(file,filename=name)

            #embeds.append({'embed': embed, 'file': sent_file})
            embeds.append(embed)
        
        return embeds



            




test = Fishing()
lists = test.search_fish('dawn')

print([test.get_path(list_f) for list_f in lists])




                    

        