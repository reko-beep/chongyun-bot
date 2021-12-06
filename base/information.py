from json import load,dump
from os.path import exists, isfile, join
from os import listdir,mkdir, getcwd

from nextcord import Embed

class GenshinInformation:
    def __init__(self) -> None:
        self.path = f'{getcwd()}/assets/Information/'
    
    def get_options(self):
        '''
        options
        files in self.path
        '''
        options = [f.split('.')[0].title() for f in listdir(self.path) if isfile(join(self.path,f))]
        return options
    
    def get_names_list(self, option: str):
        '''
        gets items names from option -> option.json
        '''

        option = option.lower()
        if exists(self.path + "/" + option+ ".json"):
            with open(self.path + "/" + option+ ".json",'r') as f:
                names = list(load(f).keys())
                return names
        return []
    
    def get_data(self, option: str, name: str):
        '''
        gets data of an item
        '''

        if exists(self.path + "/" + option+ ".json"):
            with open(self.path + "/" + option+ ".json",'r') as f:
                data = load(f)
        if name in data:
            return data[name]

    def create_artifact_embeds(self, option: str,name: str):
        '''
        create artifacts embed
        '''
        
        data = self.get_data(option,name)
        embeds = {}
        if data is not None:
            main_embed = Embed(title=f'{name}',color=0xf5e0d0)       
            if bool(data['obtain']):
                for star in data['obtain']:
                    obtain_text = ''
                    for sources in data['obtain'][star]:
                        obtain_text += '\n'.join(data['obtain'][star][sources])
                        obtain_text += '\n'
                    main_embed.add_field(name=f'{star} stars artifact obtained from:',value=obtain_text)
            else:
                main_embed.add_field(name=f'Obtain from:',value='Sorry its no where to be found!')
            if bool(data['rarity']):
                text = f"{data['rarity'][0]} - {data['rarity'][-1]} "
                main_embed.add_field(name=f'Rarity:',value=text)
            else:
                main_embed.add_field(name=f'Rarity:',value=':(')
            if 'bonus' in data and bool(data['bonus']):
                bonuses = ['2','4']
                for bonus in bonuses:
                    if bonus in data['bonus']:
                        main_embed.add_field(name=f'{bonus} pc Bonus',value=data['bonus'][bonus])
            if bool(data['pieces']):
                for piece in data['pieces']:
                    piece_embed = Embed(title=f"{name} {piece['type']}",color=0xf5e0d0)    
                    piece_embed.add_field(name='Name',value=piece['name'])
                    if 'description' in piece:
                        piece_embed.add_field(name='Lore',value=piece['description'])   
                    piece_embed.set_thumbnail(url=piece['img'])
                    embeds[piece['type']] = piece_embed
            else:
                main_embed.add_field(name='Pieces',value='None found!')
            embeds['Main Information'] = main_embed
        return embeds
        
    def create_weapon_embeds(self, option: str,name: str):

        '''
        create weapon embeds
        '''
        def minimum_information(data, embed):
            information = ['type','obtain','rarity','series']
            for inf in information:
                if inf in data:
                    if inf == 'rarity':
                        embed.add_field(name=inf.title(),value='⭐' * int(data[inf]))
                    else:
                        embed.add_field(name=inf.title(),value=data[inf])
                else:
                    embed.add_field(name=inf.title(),value='nothing found anything in database')
                

        data = self.get_data(option,name)
        embeds = {}

        if data is not None:
            main_embed = Embed(title=f'{name}',color=0xf5e0d0)       
            minimum_information(data,main_embed)
            if 'stats' in data:
                stats = data['stats']
                for stat in stats:
                    main_embed.add_field(name=stat,value=stats[stat])
            
            if 'image' in data:
                main_embed.set_image(url=data['image'][0])
            embeds['Main Information'] = main_embed

            # refinement

            if 'refinement' in data:
                if bool(data['refinement']):
                    text = data['refinement']['text']
                    for refinement in data['refinement']:                        
                        if type(data['refinement'][refinement]) == dict:                            
                            text_modified = text
                            for values in data['refinement'][refinement]:
                                text_modified = text_modified.replace(values,data['refinement'][refinement][values],1)
                            embed = Embed(title=f'{name} Refinement level {refinement}',color=0xf5e0d0)       
                            minimum_information(data,embed)
                            embed.add_field(name='Refinement Description',value=text_modified,inline=False)
                            if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                            embeds[f'{name} Refinement level {refinement}'] = embed
            
            #ascension

            if 'ascension' in data:
                if bool(data['ascension']):
                    for level in data['ascension']:
                        items = data['ascension'][level]
                        embed = Embed(title=f'{name} Ascension level {level}',color=0xf5e0d0)
                        minimum_information(data,embed)
                        text_ = ''
                        for item in items:
                            text_ +=  f"**{item['name']}** {item['amount']}\n"
                        embed.add_field(name=f'Ascension Materials required',value=text_,inline=False)
                        if 'image' in data:
                            embed.set_thumbnail(url=data['image'][0])
                        embeds[f'{name} Ascension level {level}'] = embed
            
            return embeds

    def create_character_embeds(self,  option: str,name: str):
        '''
        create character embeds
        '''
        def minimum_information(data, embed):
            information = ['element','sex','rarity','weapon']
            for inf in information:
                if inf in data:
                    if inf == 'rarity':
                        embed.add_field(name=inf.title(),value='⭐' * int(data[inf]))
                    else:
                        embed.add_field(name=inf.title(),value=data[inf])
                else:
                    embed.add_field(name=inf.title(),value='found anything in database')
                

        data = self.get_data(option,name)
        embeds = {}
        if data is not None:
            main_embed = Embed(title=f'{name}',description=data['description'],color=0xf5e0d0)       
            minimum_information(data,main_embed)
            others = ['constellation','birthday','region','affiliation','dish','parents','obtain','releaseDate','siblings']
            for other in others:
                if other in data:
                    value_ = data[other]
                    if type(data[other]) == list:
                        value_ = '\n'.join(data[other])
                    main_embed.add_field(name=other.title(),value=value_)

            if 'image' in data:
                main_embed.set_image(url=data['image'][0])
            embeds['Main Information'] = main_embed

            # constellation

            if 'constellations' in data:
                if bool(data['constellations']):
                    constellations = data['constellations']
                    for level in constellations:                        
                        if type(constellations[level]) == dict:                            
                            
                            embed = Embed(title=f'{name} Constellation level {level}',color=0xf5e0d0)       
                            minimum_information(data,embed)
                            
                            embed.add_field(name=constellations[level]['name'],value=constellations[level]['effect'],inline=False)
                            if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                            embeds[f'{name} Constellation level {level}'] = embed
            
            #talents

            if 'talents' in data:
                talents = data['talents']                
                embed = Embed(title=f'{name} Talents',color=0xf5e0d0)       
                minimum_information(data,embed)
                for talent in talents:
                    embed.add_field(name=talent['type'],value=talent['name'],inline=False)       
                embeds[f'{name} Talents'] = embed


            #ascension

            if 'ascension' in data:
                if bool(data['ascension']):
                    for level in data['ascension']:
                        items = data['ascension'][level]
                        embed = Embed(title=f'{name} Ascension level {level}',color=0xf5e0d0)       
                        minimum_information(data,embed)
                        text_ = ''
                        for item in items:
                            text_ +=  f"**{item['name']}** {item['amount']}\n"
                        embed.add_field(name=f'Ascension Materials required',value=text_)
                        if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                        embeds[f'{name} Ascension level {level}'] = embed
            
            return embeds
                            
                    
                    

                            







