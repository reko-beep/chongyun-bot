from nextcord import Embed, File
from base.resource_manager import ResourceManager
from json import load, dump
from discord.utils import get
from dev_log import logc
from random import choice
class Information():    
    def __init__(self, res: ResourceManager, bot):
        self.res_handler = res
        self.bot = bot
        self.bot_guild = None
        self.emojis = None
        self.teamcomps = {

        }
        self.load_comps()
    
    def load_comps(self):
        path = self.res_handler.db.format(path='teamcomp.json')
        with open(path, 'r') as f:
            self.teamcomps = load(f)

    def save_comps(self):
        path = self.res_handler.db.format(path='teamcomp.json')
        with open(path, 'w') as f:
            dump(self.teamcomps, f)

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

    def delete_comp(self, index_):
            ind = self.teamcomps['data'].index(index_)
            if len(self.teamcomps['data'])-1 >= ind:
                self.teamcomps['data'].pop(ind)
                print(self.teamcomps['data'])
                self.save_comps()
                return True

    def comp_index(self, comp_title):
        comps = self.teamcomps['data']
        for comp in comps:
            if '-' in comp['title'].strip():
                title = comp['title'].split('-')[0].strip()                
            else:
                title = comp['title'].strip()              
            if comp_title.strip().lower() == title.lower():
                return comps.index(comp)

    def comp_exists(self, comp_title):
        comps = self.teamcomps['data']
        for comp in comps:
            if '-' in comp['title'].strip():
                title = comp['title'].split('-')[0].strip()
                index = int(comp['title'].split('-')[1].strip())
            else:
                title = comp['title'].strip()
                index = 0
            if comp_title.strip().lower() == title.lower():
                return True, index
        return None, None

    def create_comp(self, comp_name, comp_chars, comp_notes, owner):
        
        exists, number = self.comp_exists(comp_name)
        if exists == number:
            pass
        else:
            comp_name += f"- {number + 1}"
        base_char =  comp_chars.split(',')
        chars = []
        for base in base_char:
            if ':' in base:
                if len(base.split(":")) > 1:
                    key = base.split(':')[0].strip().lower()
                    value = base.split(':')[1].strip().lower()
                    chars.append({key:value})
                    
                else:
                    return None, None
            else:
                return None, None
   

        self.teamcomps['data'].append({
            'title': comp_name,
            'chars': chars,
            'description': comp_notes,
            'owner': owner.id


        })
        self.save_comps()
        return True, {
            'title': comp_name,
            'chars': chars,
            'description': comp_notes,
            'owner': owner.id


        }


    def create_weapon_embeds(self, weapon_name: str, options: list = [], specific:bool=False):

        data = self.res_handler.get_weapon_details(weapon_name)
        weapon = self.res_handler.search(weapon_name, self.res_handler.weapons)
        embeds = []
        if data is not None:

            options_allowed = ['main','refinement', 'ascension', 'ascension_image']
            specific_data = options_allowed

            if specific:
                specific_data = set(options_allowed).intersection(options)

            rarity = data.get("rarity",3) * '⭐'
            image = choice(data.get("image"))
            type = data.get('type', 'N/A')
            obtain = '\n'.join(data.get("obtain", ['']))
            series = data.get('series', 'N/A')
            main_desc = f"{choice(data.get('description', ['']))}"

            if 'main' in specific_data:
            
                
                embed = Embed(title='Basic Information', description=f"{main_desc}\n**Rarity:** {rarity}")
                embed.add_field(name='Type', value=type)
                embed.add_field(name='Obtain', value=obtain)
                embed.add_field(name='Series', value=series)

                stats = data['stats']
                
                base_atk = stats.get('Base ATK(Lv. 1 - 90)', 'N/A')
                second_stat = stats.get('2nd StatType', 'N/A')
                second_stat_perc = stats.get('2nd Stat(Lv. 1 - 90)', 'N/A')
                embed.add_field(name='Stats', value=f"Base Attack [Lv.1-90]: *{base_atk}*\n2nd Stat: *{second_stat}*\n2nd Stat Percentage: *{second_stat_perc}*")

                embed.set_author(name=weapon, icon_url=image)
                            
                embed.set_thumbnail(url=image)
                embed.set_footer(text=f' {weapon} ∎ Basic Information ')
                embeds.append(embed)

            if 'refinement' in specific_data:

                refinements = data['refinement']
                text = refinements['text']

                refinements.pop("text")

                for refinement in refinements:
                    refine_text = text

                    for val in refinements[refinement]:
                        refine_text = refine_text.replace(val, f'**{refinements[refinement][val]}**', 1)

                    embed = Embed(title=f'Refinement Level {refinement}', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*")
                    embed.add_field(name='Refinement stats', value=refine_text)
                    
                    
                    embed.set_author(name=weapon, icon_url=image)
                                
                    embed.set_thumbnail(url=image)
                    embed.set_footer(text=f' {weapon} ∎ Refinement Level {refinement} ')
                    embeds.append(embed)
            
            if 'ascension' in specific_data:

                embed = Embed(title=f'Ascension Materials', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*")
               
                
                embed.set_author(name=weapon, icon_url=image)
                            
                embed.set_thumbnail(url=image)
                embed.set_footer(text=f' {weapon} ∎ Ascension Materials')
                
                
                ascension = data['ascension']
                for level in ascension:

                    materials = ascension[level]
                    ascension_text = ''

                    for mat in materials:

                        ascension_text += f"{mat['name']}: *{mat['amount']}*\n"
                    embed.add_field(name=f'Ascension Level {level}', value=ascension_text)
                embeds.append(embed)
            print(specific_data)
            if 'ascension_image' in specific_data:
                print(data['file'])
                if data['file'] is not None:
                    url = self.res_handler.convert_to_url(self.res_handler.genpath('images/weapons', data['file']), True)
                    embed = Embed(title=f'Ascension Materials', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*")

                    
                    
                    embed.set_author(name=weapon, icon_url=image)
                                
                    embed.set_thumbnail(url=image)
                    embed.set_image(url=url)
                    embed.set_footer(text=f' {weapon} ∎ Ascension Materials')
                    embeds.append(embed)
                else:
                    embeds.append(self.create_na_embed(
                        weapon,
                        f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*",
                        0x5283ff,
                        f'Ascension Materials',
                        image
                    ))

        return embeds







