from nextcord import Embed, File
from base.resource_manager import ResourceManager
from json import load, dump
from discord.utils import get
from dev_log import logc
class Information():    
    def __init__(self, res: ResourceManager, bot):
        self.res_handler = res
        self.bot = bot
        self.bot_guild = None
        self.emojis = None

    def create_na_embed(self, character: str, desc_str: str, color_ : int, title: str, thumbnail_url: str):

        embed = Embed(title=f'{title}',description=desc_str, color=color_)
        embed.set_author(name=character, icon_url=thumbnail_url)
        embed.set_thumbnail(url=thumbnail_url)

    
        embed.set_footer(text=f' {character} ∎ {title}') 
        return embed

    def create_character_embeds(self, character_name: str, options: list= [], specific:bool = False, url: bool= False):
        '''        
        create character embeds for character_name
        from specified options
        '''

        embeds = []
        if self.bot_guild is None:

            self.bot_guild = get(self.bot.guilds, id=945256650355392554)           
            
            if self.bot_guild is not None:
                self.emojis = self.bot_guild.emojis
            else:
                self.emojis = None
            logc('Dev Guild', self.bot_guild,'\n','emojis loaded', len(self.emojis))
        character = self.res_handler.search(character_name, self.res_handler.characters)
        data = self.res_handler.get_character_full_details(character_name, url)
        print(data)
        if data is not None:
            options_allowed = ['main','constellations','talents','builds', 'ascension_imgs', 'teamcomps']

            # check if provided options are
            specific_data = options_allowed
            if specific:
                check = (len(set(options).intersection(options_allowed)) != 0)
                if check:

                    specific_data =  list(set(options).intersection(options_allowed))
            
            images_dict = {k.split('/')[-1].split('.')[0].split('_')[-1].lower(): k for k in data['image']}
            print(images_dict)
            print(specific_data)
            element = self.res_handler.get_element(data.get('element'))
            
            element_color = element.get('color', 9486540)
            if self.emojis is not None:
                element_emoji = get(self.emojis, name=data.get('element').lower())
                element_emoji = '<:'+element_emoji.name+":"+str(element_emoji.id)+'>'
         
            if 'image' in specific_data:
                specific_data.pop('image')

            # keys setup for embeds

            #
            #   MAIN
            #
            element = 'N/A' if data.get('element','') == '' else data['element']
            weapon = 'N/A' if data.get('weapon','') == '' else data['weapon']
            nation = 'N/A' if data.get('nation','') == '' else data['nation']
            rarity = ''
            if data.get('rarity', 0) == 0:
                rarity = 'N/A'
            else:
                rarity = '⭐'*data.get('rarity')
            min_desc = f"\n**Element:** *{element}* {element_emoji}\n**Weapon:** *{weapon}*\n**Nation:** *{nation}*\n**Rarity:** {rarity}"
            if 'main' in specific_data:
                main_keys = ['sex','element','birthday','region','weapon','parents','obtain', 'constellation']
                
                embed = Embed(title=f'Basic Information', description=f"{data.get('description','N/A')}\n\n**Rarity:** {rarity}", color=element_color)
                for i in main_keys:
                    v = 'N/A'
                    if i == 'constellation':                        
                        if data.get("constellation", None) != None:
                            if type(data['constellation']) == list:
                                v = [c for c in data.get("constellation") if 'chapter' not in c.lower() and 'constellation' not in c.lower()]
                                v = 'N/A' if len(v) == 0 else v[0]                           
                        embed.add_field(name=i.title(), value=v, inline=True)
                    else:
                        if i == 'element':
                            v = 'N/A' if data.get(i,None) == None else data[i] +' '+element_emoji
                        else:
                            if i in data and i != 'rarity':
                                if data.get(i, None) != None:
                                    if type(data[i]) == list:
                                        v = '\n'.join(data[i])
                                    else:
                                        if data[i] == '':
                                            v = 'N/A'
                                        else:
                                            v = data[i]
                        embed.add_field(name=i.title(), value=v, inline=True)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Main Information')
                print(embed.to_dict())
                embeds.append(embed)

            if 'constellations' in specific_data:

                c_data = data.get('constellations', None)
                
                if c_data is not None:
                    if len(c_data) > 0:
                        c_desc = ''
                        for const in c_data:

                            level = const
                            const_data = c_data[const]
                            c_desc += f"**{const_data['name']}** ∎ **Level {level}**\n*{const_data['effect']}*\n\n"

                        embed = Embed(title=f'Constellations',description=c_desc, color=element_color)
                        embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                        embed.set_thumbnail(url=images_dict.get('thumb'))

                        folder_name = self.res_handler.genpath('images/characters',self.res_handler.search(character, self.res_handler.goto('images/characters').get('folders')))
                        image_url = self.res_handler.convert_to_url(f'{folder_name}/constellations.png', True)
                        print(image_url)
                        embed.set_image(url=image_url)
                        embed.set_footer(text=f' {character} ∎ Constellations')   
                        embeds.append(embed)
                    else:
                        embeds.append(self.create_na_embed(
                        character,
                        'No Constellation found yet!',
                        element_color,
                        'Constellations',
                        images_dict.get('thumb')
                    ))
                else:
                    embeds.append(self.create_na_embed(
                        character,
                        'No Constellation found yet!',
                        element_color,
                        'Constellations',
                        images_dict.get('thumb')
                    ))

        
            if 'talents' in specific_data:

                    t_data = data.get("talents", None)
                    
                    if t_data is not None:
                        if len(c_data) > 0:
                            t_desc = ''
                            for t in t_data:

                                t_desc += f"**{t['name']}**\n*{t['type']}*\n\n"

                            embed = Embed(title=f'Talents',description=t_desc, color=element_color)
                            embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                            embed.set_thumbnail(url=images_dict.get('thumb'))

                            folder_name = self.res_handler.genpath('images/characters',self.res_handler.search(character, self.res_handler.goto('images/characters').get('folders')))
                            image_url = self.res_handler.convert_to_url(f'{folder_name}/talents.png', True)
                            print(image_url)
                            embed.set_image(url=image_url)
                            embed.set_footer(text=f' {character} ∎ Talents') 
                            embeds.append(embed)  
                        else:
                            embeds.append(self.create_na_embed(
                            character,
                            'No talents found yet!',
                            element_color,
                            'Talents',
                            images_dict.get('thumb')
                        ))
                    else:
                        embeds.append(self.create_na_embed(
                        character,
                        'No talents found yet!',
                        element_color,
                        'Talents',
                        images_dict.get('thumb')
                    ))
            if 'builds' in specific_data:
                b_data = data.get("builds", None)
                if b_data is not None:
                    if len(b_data) > 0:
                        for b in b_data:
                            embed = Embed(title=f"{b.split('/')[-1].split('.')[0].replace('_',' ', 99).title().replace('Dps','DPS',1)} Build",description=f"{min_desc}", color=element_color)
                            embed.set_image(url=b)
                            embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                            embed.set_thumbnail(url=images_dict.get('thumb'))
                            embed.set_footer(text=f' {character} ∎ Builds ')   

                            embeds.append(embed)
                    else:
                        embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No builds available yet!*',
                            element_color,
                            'Builds',
                            images_dict.get('thumb')
                        ))
                else:
                    embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No builds available yet!*',
                            element_color,
                            'Builds',
                            images_dict.get('thumb')
                        ))
            
            if 'ascension_imgs' in specific_data:
                a_data = data.get('ascension_imgs', None)
                if a_data is not None:
                    if len(a_data) > 0:
                        for a in data['ascension_imgs']:
                            embed = Embed(title='Ascension and Talent Mats',description=f"{min_desc}", color=element_color)               
                            embed.set_image(url=a)
                            embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                            embed.set_thumbnail(url=images_dict.get('thumb'))
                            embed.set_footer(text=f' {character} ∎ Ascension ')   

                            embeds.append(embed)
                    else:
                        embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No ascension available yet!*',
                            element_color,
                            'Ascension and Talent Mats',
                            images_dict.get('thumb')
                        ))
                else:
                    embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No ascension available yet!*',
                            element_color,
                            'Ascension and Talent Mats',
                            images_dict.get('thumb')
                        ))
            
            

            if 'teamcomps' in specific_data:
                comps = data.get('teamcomps', None)
                
                if comps is not None:
                    if len(comps) > 0:
                        for comp in comps:
                            title = comp['title']
                            chars = []
                            for char in comp['chars']:
                                c = list(char.keys())[0]
                                chars.append(c.title())
                            owner_ = comp.get('owner', None)
                            usr = None
                            if owner_ is not None:
                                usr = get(self.bot.guilds[0].members, id=owner_)
                            desc = '\n'.join(chars)
                            embed = Embed(title=f'Team Comps - {title}', description=f"**Contributed by:** {usr}\n{comp['description']}\n**Characters used in Team Composition**:\n{desc}", color=element_color)
                            embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                            
                            embed.set_image(url=comp['file'])
                            embed.set_footer(text=f' {character} ∎ Team Comps ')
                            embeds.append(embed)
                    else:
                        embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No team comp available yet!*',
                            element_color,
                            'Team comps',
                            images_dict.get('thumb')
                        ))
                    
                else:
                    embeds.append(self.create_na_embed(
                            character,
                            f'{min_desc}\n\n*No team comp available yet!*',
                            element_color,
                            'Team comps',
                            images_dict.get('thumb')
                        ))
        
        print(embeds)
        return embeds

