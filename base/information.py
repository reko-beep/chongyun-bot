from nextcord import Embed, File
from base.resource_manager import ResourceManager
from json import load, dump
from discord.utils import get
from dev_log import logc
class Information():    
    def __init__(self, res: ResourceManager, bot):
        self.res_handler = res
        self.bot = bot
        self.bot_guild = get(self.bot.guilds, id=945256650355392554)
        if self.bot_guild is not None:
            self.emojis = self.bot_guild.emojis
        else:
            self.emojis = None
        logc('Dev Guild', self.bot_guild,'\n','emojis loaded', len(self.emojis))

    def create_character_embeds(self, character_name: str, options: list= [], specific:bool = False, url: bool= False):
        '''        
        create character embeds for character_name
        from specified options
        '''

        embeds = []

        character = self.res_handler.search(character_name, self.res_handler.characters)
        data = self.res_handler.get_character_full_details(character_name, url)
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

            element = self.res_handler.get_element(data.get('element'))
            
            element_color = element.get('color', 9486540)
            if self.emojis is not None:
                element_emoji = get(self.emojis, name=element.lower())
                logc('Element Emoji', element_emoji)
                if element_emoji is not None:
                    element_emoji = ':'+element_emoji.name+':'
            else:
                element_emoji = ''
            logc('Final Element Emoji', element_emoji)
            if 'image' in specific_data:
                specific_data.pop('image')

            # keys setup for embeds

            #
            #   MAIN
            #
            min_desc = f"**Sex:** *{data.get('sex','N/A')}* \n**Element:** *{data.get('element','N/A')}* {element_emoji}\n**Weapon:** *{data.get('weapon','N/A')}*\n**Nation:** *{data.get('nation','N/A')}*\n**Rarity:** {data.get('rarity',3) *'⭐'}"
            if 'main' in specific_data:
                main_keys = ['sex','element','birthday','region','weapon','parents','obtain', 'constellation']
                embed = Embed(title=f'Basic Information', description=f"{data.get('description','')}\n\n**Rarity:** {data.get('rarity',3) *'⭐'}", color=element_color)
                for i in main_keys:
                    if i == 'constellation':
                        v = data[i]
                        embed.add_field(name=i.title(), value=v[-1], inline=True)
                    else:
                        if i == 'element':
                            v = data[i]+' '+element_emoji
                        else:

                            if i in data and i != 'rarity':
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

                embed = Embed(title=f'Constellations',description=c_desc, color=element_color)
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

                embed = Embed(title=f'Talents',description=t_desc, color=element_color)
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
                embed = Embed(title=f"{b.split('/')[-1].split('.')[0].replace('_',' ', 99).title()} Build",description=f"{min_desc}", color=element_color)
                embed.set_image(url=b)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Builds ')   

                embeds.append(embed)
        
        if 'ascension_imgs' in specific_data:
            for a in data['ascension_imgs']:
                embed = Embed(title='Ascension and Talent Mats',description=f"{min_desc}", color=element_color)               
                embed.set_image(url=a)
                embed.set_author(name=character, icon_url=images_dict.get('thumb'))
                embed.set_thumbnail(url=images_dict.get('thumb'))
                embed.set_footer(text=f' {character} ∎ Ascension ')   

                embeds.append(embed)
        
        if 'teamcomps' in specific_data:
            comps = data['teamcomps']
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


        return embeds

