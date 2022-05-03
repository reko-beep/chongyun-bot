from posixpath import split
from nextcord import Embed, File, Guild
from base.bookmark import Bookmarer
from base.resource_manager import ResourceManager
from json import load, dump
from discord.utils import get
from dev_log import logc
from random import choice, random
from os import getcwd
from PIL import Image, ImageFont, ImageDraw
class Information():    
    def __init__(self, res: ResourceManager, bot):
        self.res_handler = res
        self.bot = bot
        self.bot_guild = None
        self.emojis = None
        self.teamcomps = {

        }
        self.bookmark = Bookmarer(bot)
        
        self.load_comps()
    
    def load_comps(self):
        path = self.res_handler.db.format(path='teamcomp.json')
        with open(path, 'r') as f:
            self.teamcomps = load(f)

    def save_comps(self):
        path = self.res_handler.db.format(path='teamcomp.json')
        with open(path, 'w') as f:
            dump(self.teamcomps, f, indent=1)

    def create_na_embed(self, character: str, desc_str: str, color_ : int, title: str, thumbnail_url: str):

        embed = Embed(title=f'{title}',description=desc_str, color=color_)
        embed.set_author(name=character, icon_url=thumbnail_url)
        embed.set_thumbnail(url=thumbnail_url)

    
        embed.set_footer(text=f' {character} ∎ {title}') 
        return embed

    def create_character_embeds(self,guild: Guild, character_name: str, options: list= [],  specific:bool = False,  split_search:bool=True ):
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
        character = self.res_handler.search(character_name, self.res_handler.characters , split_search)
        data = self.res_handler.get_character_full_details(character_name, split_search)
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
                                usr = get(guild.members, id=owner_)
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
            ind = index_
            if len(self.teamcomps['data'])-1 >= ind:
                self.teamcomps['data'].pop(ind)
                print(self.teamcomps['data'])
                self.save_comps()
                return True

    def comp_index(self, comp_title):
        comps = self.teamcomps['data']
        for comp in comps:
            if '-' in comp['title'].strip():
                if comp['title'].split('-')[1].strip().isdigit():
                    title = comp['title'].split('-')[0].strip()         
                else:
                    title = comp['title'].strip()        
            else:
                title = comp['title'].strip()              
            if comp_title.strip().lower() == title.lower():
                return comps.index(comp)

    def comp_exists(self, comp_title):
        comps = self.teamcomps['data']
        exist = None
        index = None
        for comp in comps:
            if '-' in comp['title'].strip():
                print(comp['title'].split('-')[-1], comp['title'].split('-')[-1].strip().isdigit())
                if comp['title'].split('-')[-1].strip().isdigit():
                    title = comp['title'].replace(comp['title'].split('-')[-1], '', 1).strip()                    
                    index = int(comp['title'].split('-')[-1].strip())
                    print('number found', index)
                else:
                    title = comp['title'].strip()
                    index = 0                
            else:
                title = comp['title'].strip()
                index = 0
            if comp_title.strip().lower() == title.lower():
                exist = True
        return exist, index 

    def create_comp_embed(self, comp: dict, guild):
        title = comp['title']
        chars = []
        for char in comp['chars']:
            c = list(char.keys())[0]
            chars.append(c.title())
        owner_ = comp.get('owner', None)
        usr = None
        if owner_ is not None:
            usr = get(guild.members, id=owner_)
        desc = '\n'.join(chars)
        embed = Embed(title=f'Team Comps - {title}', description=f"**Contributed by:** {usr}\n{comp['description']}\n**Characters used in Team Composition**:\n{desc}")
        
        url_ = self.res_handler.convert_to_url(self.res_handler.genpath('images/teamcomps', comp['file']), True)
        embed.set_image(url=url_)
        embed.set_footer(text=f'{title} Team Comp')
        return embed



    def create_comp(self, comp_name, comp_chars, comp_notes, owner):
        
        exists, number = self.comp_exists(comp_name)
        if exists == number == None:
            pass
        else:
            if number is not None:
                comp_name += f"- {number + 1}"
        print(number, comp_name)
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
   
        file = self.create_teamcomp_image(comp_name, chars)
        self.teamcomps['data'].append({
            'title': comp_name,
            'chars': chars,
            'description': comp_notes,
            'owner': owner.id,
            'file': file


        })
        self.save_comps()
        return True, {
            'title': comp_name,
            'chars': chars,
            'description': comp_notes,
            'owner': owner.id,
            'file': file


        }


    def random_bg(self):

        bgs = self.res_handler.goto("images/bgs").get("files")

        return self.res_handler.genpath('images/bgs', choice(bgs))

    def create_teamcomp_image(self,comp_title, chars):
        main_bg = Image.open(self.random_bg(),'r').convert('RGBA')
        font_path = self.res_handler.genpath('misc', 'font.otf')
        title = comp_title
        test_font = ImageFont.truetype(font_path,size=105)
        ImageDraw.Draw(main_bg).text((main_bg.size[0]-test_font.getsize(title)[0]-30, 10), title,fill=(255,255,255,255), font=test_font)
        chars = chars
        start_w = main_bg.size[0] - (301*4)

        role_font = ImageFont.truetype(font_path,size=30)
        for char in chars:
            char_key = list(char.keys())[0]
            role = char[char_key]
            char_image = self.res_handler.search(char_key, self.res_handler.goto("images/thumbnails").get('files'))

            
            
            if char_image is not None:
                char_image = self.res_handler.genpath('images/thumbnails', char_image)
                img = Image.open(char_image,'r').convert('RGBA')
                main_bg.paste(img, (start_w, main_bg.size[1]-256), img)
                ImageDraw.Draw(main_bg).text((start_w+(role_font.getsize(role)[0]//2)+ 10, main_bg.size[1]-256-40), role, fill=(255,255,255,255), font=role_font)
                start_w += 301
        
        file_name = comp_title.replace(' ','_',99999).replace('-','',99)+'.png'
        path = self.res_handler.genpath('images/teamcomps' ,file_name)
        main_bg.save(path,format='PNG')
        return file_name

    def create_weapon_embeds(self,guild: Guild, weapon_name: str, options: list = [], specific:bool=False, split_search:bool=True):

        data = self.res_handler.get_weapon_details(weapon_name, split_search)
        weapon = self.res_handler.search(weapon_name, self.res_handler.weapons, split_search)
        embeds = []
        if data is not None:

            options_allowed = ['main','refinement', 'ascension', 'ascension_image']
            specific_data = options_allowed

            if specific:
                specific_data = set(options_allowed).intersection(options)

            rarity = data.get("rarity",3) * '⭐'
            image = choice(data.get("image"))
            color = self.res_handler.get_color_from_image(image)
            type = data.get('type', 'N/A')
            obtain = '\n'.join(data.get("obtain", ['']))
            series = data.get('series', 'N/A')
            main_desc = f"{choice(data.get('description', ['']))}"

            if 'main' in specific_data:
            
                
                embed = Embed(title='Basic Information', description=f"{main_desc}\n**Rarity:** {rarity}", color=color)
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
                print(refinements, weapon_name)
                refinements.pop("text")

                for refinement in refinements:
                    refine_text = text

                    for val in refinements[refinement]:
                        refine_text = refine_text.replace(val, f'**{refinements[refinement][val]}**', 1)

                    embed = Embed(title=f'Refinement Level {refinement}', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*", color=color)
                    embed.add_field(name='Refinement stats', value=refine_text)
                    
                    
                    embed.set_author(name=weapon, icon_url=image)
                                
                    embed.set_thumbnail(url=image)
                    embed.set_footer(text=f' {weapon} ∎ Refinement Level {refinement} ')
                    embeds.append(embed)
            
            if 'ascension' in specific_data:

                embed = Embed(title=f'Ascension Materials', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*", color=color)
               
                
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
                    url = self.res_handler.convert_to_url(self.res_handler.genpath('images/weapons', data['file'].replace(' ','%20',99)), True)
                    embed = Embed(title=f'Ascension Materials', description=f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*", color=color)

                    
                    
                    embed.set_author(name=weapon, icon_url=image)
                                
                    embed.set_thumbnail(url=image)
                    embed.set_image(url=url)
                    embed.set_footer(text=f' {weapon} ∎ Ascension Materials')
                    embeds.append(embed)
                else:
                    embeds.append(self.create_na_embed(
                        weapon,
                        f"{main_desc}\n**Rarity:** {rarity}\n**Type:** *{type}*",
                        color,
                        f'Ascension Materials',
                        image
                    ))

        return embeds



    def create_artifact_embeds(self, guild:Guild, artifact_name:str, options:list=[], specific:bool=False, split_search:bool=False):

        data = self.res_handler.get_artifact_details(artifact_name, split_search)
        artifact = self.res_handler.search(artifact_name, list(self.res_handler.artifacts.keys()), split_search)
        embeds = []
        if data is not None:

            options_allowed = ['main','refinement', 'ascension', 'ascension_image']
            specific_data = options_allowed

            if specific:
                specific_data = set(options_allowed).intersection(options)
            

            bonus_check = len(data['bonus']) > 0
            rarity_check = len(data['rarity']) > 1

            rarity_text = ''
            if rarity_check:
                rarity_text = f"**Rarity:** {data['rarity'][0]} - {data['rarity'][-1]} ⭐'s"
            else:
                rarity_text = f"**Rarity:**  {data['rarity'][0]} ⭐"
            
            desc_text = ""
            pieces = data['pieces']
            for i in pieces:
                desc_text += f" **{i['name']} ∎ {i['type']}** \n *{i['description'].strip()}* \n"
            desc_text += rarity_text
            color = self.res_handler.get_color_from_image(data['pieces'][0]['img'])

            embed_main = Embed(title='Basic Information', description=desc_text, color=color)
          
            embed_main.set_author(name=artifact, icon_url=data['pieces'][0]['img'])                                
            embed_main.set_thumbnail(url=data['pieces'][0]['img'])
            
            embed_main.set_footer(text=f' {artifact} ∎ Basic Information')
            embeds.append(embed_main)

            embed = Embed(title='Bonuses and Obtain', description=f"{data['pieces'][0]['description']}\n{rarity_text}", color=color)
            
            for o in data['obtain']:
                obtain_text = ''
                for source in data['obtain'][o]:
                    obtain_text += '🔸'
                    obtain_text += '\n 🔸'.join(data['obtain'][o][source])
                    obtain_text += '\n'
                embed.add_field(name=f"{o}-star source", value=obtain_text)
            
            b_text = ''
            if bonus_check:
                for b in data['bonus']:
                    b_text += f" 🔸{b}-piece Bonus \n*{data['bonus'][b]}*\n\n"
                
                embed.add_field(name='Bonus', value=b_text)
            if data['file'] is not None:
                url_ = self.res_handler.convert_to_url(self.res_handler.genpath('images/artifacts', data['file']), True).replace(' ','%20', 99)
                print(url_)
                embed.set_image(url=url_)
            embed.set_author(name=artifact, icon_url=data['pieces'][0]['img'])                                
            embed.set_thumbnail(url=data['pieces'][0]['img'])
            
            embed.set_footer(text=f' {artifact} ∎ Bonuses and Obtain')
            embeds.append(embed)
            return embeds

    def create_abyss_embeds(self, floor_str: str):

        args = {'floor': '', 'chamber': '', 'half':''}
        if '-' in floor_str:
            keys = list(args.keys())
            for i in range(len(floor_str.split('-'))):
                args[keys[i]] = floor_str.split("-")[i]
        else:
            args['floor'] = floor_str

        floor_ = 'floor_{floor}'.format(floor=args['floor'])

        embeds = []
        desc = ''
        
        path = self.res_handler.genpath('data', self.res_handler.search('abyss',self.res_handler.goto('data').get('files')))
        path_fix = getcwd()+"/assets/images/abyss/{floor}/{chamber}/{half}.png"
        with open(path, 'r') as f:
            abyss = load(f)
        color = self.res_handler.get_color_from_image(self.bot.user.avatar.url)
        data = abyss[floor_]
        leyline_text = ['None'] if data.get('Ley Line Disorder', 'None') == 'None' else data['Ley Line Disorder']['text']
        t = '🔸'
        t += '\n🔸'.join(leyline_text)
        desc += f"**Ley Line Disorder:**\n{t}\n"
        t = '🔸'
        ae_text = ['None'] if data.get('Additional Effects', 'None') == 'None' else data['Additional Effects']['text']
        t += '\n 🔸'.join(ae_text)
        desc += f"**Additional Effects:**\n{t}\n"
        main = Embed(title=f"Floor {args['floor']}", description=desc, color=color)
        main.set_author(name='Abyss Moon Spiral', icon_url=self.bot.user.avatar.url)                                
        main.set_thumbnail(url=self.bot.user.avatar.url)
        
        main.set_footer(text=f' Abyss Moon Spiral ∎ Basic Information')
        embeds.append(main)

        '''
        chamber keys
        if specific only those keys
        '''
        chamber_keys = [chamb for chamb in data if 'chamber' in chamb.lower()]
        if args['chamber'] != '':
            chamber_keys = []
            for c in range(int(args['chamber'])):
                if f'chamber {c+1}' in [l.lower() for l in data.keys()]:
                    chamber_keys.append(f'chamber {c+1}'.title())
        

        for chamber in chamber_keys:
            c_data = data[chamber]
            if args['half'] == '1' or args['half'] == '':
                desc_ = f"**Enemy Level:** {c_data['Enemy Level']}\n**Challenge Target:**\n{c_data['Challenge Target']}"
                path = self.res_handler.convert_to_url(path_fix.format(floor=floor_, chamber=chamber.lower().replace(" ",'_',99).strip(), half='first_half'), True)
                e_embed = Embed(title=f"Floor {args['floor']} ∎ {chamber} - First Half", description=desc_, color=color)
                enem_text = '\n'.join([f"🔸 {i['amount']} {i['name']}" for i in c_data['First Half']['enemies']])
                e_embed.add_field(name='Enemies', value=enem_text)

                e_embed.set_image(url=path)
                e_embed.set_author(name='Abyss Moon Spiral', icon_url=self.bot.user.avatar.url)                                
                e_embed.set_thumbnail(url=self.bot.user.avatar.url)
                
                e_embed.set_footer(text=f" Abyss Moon Spiral ∎ Floor {args['floor']}  ∎ {chamber} - First Half")
                embeds.append(e_embed)

            
            if args['half'] == '2' or args['half'] == '':
                path = self.res_handler.convert_to_url(path_fix.format(floor=floor_, chamber=chamber.lower().replace(" ",'_',99).strip(), half='second_half'), True)
                e_embed = Embed(title=f"Floor {args['floor']} ∎ {chamber} - Second Half", description=desc_, color=color)
                enem_text = '\n'.join([f"🔸 {i['amount']} {i['name']}" for i in c_data['Second Half']['enemies']])
                e_embed.add_field(name='Enemies', value=enem_text)
                e_embed.set_image(url=path)
                e_embed.set_author(name='Abyss Moon Spiral', icon_url=self.bot.user.avatar.url)                                
                e_embed.set_thumbnail(url=self.bot.user.avatar.url)
                
                e_embed.set_footer(text=f"Abyss Moon Spiral ∎ Floor {args['floor']}  ∎ {chamber} - Second Half")
                embeds.append(e_embed)
        return embeds


    def create_furnishing_embeds(self, character_name:str):
        data = self.res_handler.get_furnishing_details(character_name)
        char = self.res_handler.search(character_name, list(self.res_handler.characters.keys()))
        data_char = self.res_handler.get_character_full_details(character_name)
        images_dict = {k.split('/')[-1].split('.')[0].split('_')[-1].lower(): k for k in data_char['image']}

        embeds = []
        if data is not None:
            for furn in data:
                print(furn)
                embed = Embed(title=f"Furnishing set -  {furn['title']}", description=furn['description'], color=self.res_handler.get_color_from_image(images_dict['thumb']))
                embed.set_author(name=char, icon_url=images_dict['thumb'])
                embed.set_thumbnail(url=images_dict['thumb'])
                for k in furn:
                    v = 'N/A'
                    if k not in ['file', 'description','gift_sets', 'link', 'img', 'title']:
                        if type(furn[k]) == list:
                            v = '🔸'
                            v += '\n 🔸'.join(furn[k])
                        else:
                            v = furn[k]                  
                       
                        if k != 'chars':
                            embed.add_field(name=k.replace('_', ' ',99).title(), value=v)
                        else:
                            embed.add_field(name='Characters', value=v)
                embed.set_image(url=furn['img'])
                embed.set_footer(text=f"{char} - furnishing set")
                embeds.append(embed)
                for f in furn['file']:
                    path = self.res_handler.convert_to_url(self.res_handler.genpath('images/furnishing', f), True)
                    print(path)
                    f_embed = Embed(title=f"Furnishing set -  {furn['title']}", description=furn['description']+'\n\n*Gift items overview*', color=self.res_handler.get_color_from_image(images_dict['thumb']))
                    v = 'N/A'
                    for gf in  furn['gift_sets']:
                        v += f"🔸 {gf['amount']} {gf['title']}\n"
                    f_embed.add_field(name='Gift sets', value=v)
                    f_embed.set_author(name=char, icon_url=images_dict['thumb'])
                    f_embed.set_thumbnail(url=images_dict['thumb'])
                    f_embed.set_image(url=path)
                    f_embed.set_footer(text=f"{char} - Furnishing set - {furn['title']}")
                    embeds.append(f_embed)

        return embeds

        
    def create_domains_embeds(self, day:str, region:str, type_:str):
        embeds = []
        if day == 'sunday':
            color = self.res_handler.get_color_from_image(self.bot.user.avatar.url)
            embed = Embed(title='All Domains', color=color)
            embed.add_field(name='Day', value='Sunday')
            embed.add_field(name='Item Series', value='All series of items availabe')
            
            embed.set_image(url=url_)

            embeds.append(embed)
          
        else:

            data = self.res_handler.get_domain(day, region, type_)

            for domain in data:
                color = self.res_handler.get_color_from_image(domain['domain_image'])
                embed = Embed(title=domain['domain_name'], description=domain['domain_description']+f"\n**Type:** *{domain['type']}*\n**Required AR:** *{domain['required_ar']}*\n**Recommended Part Level:** *{domain['required_plevel']}*", color=color)
                embed.add_field(name='Days', value=domain['day'])
                embed.add_field(name='Item Series', value=domain['item_series'])
                
                embed.set_thumbnail(url=domain['domain_image'])
                items = '🔸' + '\n🔸'.join(domain['items'])
                embed.add_field(name='Items', value=items)
                fors = '🔸' + '\n🔸'.join(domain['farmed_for'])
                embed.add_field(name='Farmed for', value=fors)
                url_ = self.res_handler.convert_to_url(domain['file'], True)
                embed.set_image(url=url_)

                embeds.append(embed)

        return embeds

