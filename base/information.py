from nextcord import Embed, File
from base.resource_manager import ResourceManager
from json import load, dump


class Information():    
    def __init__(self, res: ResourceManager):
        self.res_handler = res


    def create_character_embeds(self, character_name: str, options: list= [], specific:bool = False, url: bool= False):
        '''        
        create character embeds for character_name
        from specified options
        '''

        embeds = []

        character = self.res_handler.search(character_name, self.res_handler.characters)
        data = self.res_handler.get_character_full_details(character_name, url)
        if data is not None:
            options_allowed = ['main','constellations','talents','builds', 'ascension_imgs']
            # check if provided options are
            specific_data = options_allowed
            if specific:
                check = (len(set(options).intersection(options_allowed)) != 0)
                if check:

                    specific_data =  list(set(options).intersection(options_allowed))
            
            images_dict = {k.split('/')[-1].split('.')[0].split('_')[-1].lower(): k for k in data['image']}
            print(images_dict)
            if 'image' in specific_data:
                specific_data.pop('image')

            # keys setup for embeds

            #
            #   MAIN
            #

            if 'main' in specific_data:
                main_keys = ['sex','element','rarity','birthday','region','weapon','parents','obtain', 'constellation']
                embed = Embed(title=f'Basic Information', description=f"{data.get('description','')}")
                for i in main_keys:
                    if i in data:
                        v = '\n'.join(data[i]) if type(data[i]) == list else data[i]
                        embed.add_field(name=i.title(), value=v, inline=True)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Main Information')
                embeds.append(embed)

            if 'constellations' in specific_data:

                c_data = data['constellations']
                c_desc = ''
                for const in c_data:

                    level = const
                    const_data = c_data[const]
                    c_desc += f"**{const_data['name']}** ∎ **Level {level}**\n*{const_data['effect']}*\n\n"

                embed = Embed(title=f'Constellations',description=c_desc)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))

                folder_name = self.res_handler.genpath('images/characters',self.res_handler.search(character, self.res_handler.goto('images/characters').get('folders')))
                image_url = self.res_handler.convert_to_url(f'{folder_name}/constellations.png', True)
                print(image_url)
                embed.set_image(url=image_url)
                embed.set_footer(text=f' {character} ∎ Constellations')   
                embeds.append(embed)
        
        if 'talents' in specific_data:
    
                t_data = data['talents']
                t_desc = ''
                for t in t_data:

                    t_desc += f"**{t['name']}**\n*{t['type']}*\n\n"

                embed = Embed(title=f'Talents',description=t_desc)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))

                folder_name = self.res_handler.genpath('images/characters',self.res_handler.search(character, self.res_handler.goto('images/characters').get('folders')))
                image_url = self.res_handler.convert_to_url(f'{folder_name}/talents.png', True)
                print(image_url)
                embed.set_image(url=image_url)
                embed.set_footer(text=f' {character} ∎ Talents') 
                embeds.append(embed)  

        if 'builds' in specific_data:
            for b in data['builds']:
                embed = Embed(title='Builds',description=f"\n**Build Type:**\n{b.split('/')[-1].split('.')[0].replace('_',' ', 99).title()}")
                embed.set_image(url=self.res_handler.convert_to_url(b,True))
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Builds ')   

                embeds.append(embed)
        
        if 'ascension_imgs' in specific_data:
            for a in data['ascension_imgs']:
                embed = Embed(title='Ascension and Talent Mats')
                embed.set_image(url=self.res_handler.convert_to_url(a,True))
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Ascension ')   

                embeds.append(embed)
        return embeds