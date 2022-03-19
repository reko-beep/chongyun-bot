from nextcord import Embed, File
from resource_manager import ResourceManager
from json import load, dump


class Information():    
    def __init__(self, res: ResourceManager):
        self.res_handler = res


    def create_character_embed(self, character_name: str, options: list= [], specific:bool = False, url: bool= False):
        '''        
        create character embeds for character_name
        from specified options
        '''

        embeds = []

        data = self.res_handler.get_character_full_details(character_name, url)
        if data is not None:
            options_allowed = list(data.keys())
            # check if provided options are
            specific_data = {k: data[k] for k in options_allowed}
            if specific:
                check = (len(set(options).intersection(options_allowed)) != 0)
                if check:

                    specific_data = {k: data[k] for k in list(set(options).intersection(options_allowed))}
            
            images_dict = {k.split('/')[-1].split('.')[0].split('_')[-1].lower(): k for k in data['image']}
            print(images_dict)
            if 'image' in specific_data:
                specific_data.pop('image')

            # keys setup for embeds

            #
            #   MAIN
            #

            main_keys = ['sex','element','rarity','birthday','region','weapon','parents','obtain', 'constellation']
            main_selected_keys = list(set(main_keys).intersection(specific_data))
            print(main_selected_keys)


