
from datetime import datetime
from nextcord.ext.commands import Context
from nextcord.ext import commands,tasks
from nextcord import Embed, Member
from nextcord.utils import get

from core.paimon import Paimon

from os import listdir,getcwd,remove
from os.path import isfile, join,exists
from util.logging import logc
from json import dump,load
import genshinstats as gs
from base.resin import reminder_set
import re

class GenshinDB():
    def __init__(self, pmon: Paimon):
        self.path = getcwd()
        self.file = 'genshin.json'
        self.data = {}
        self.pmon = pmon
        self.allowed = ['eu','na','asia']        
        self.ltoken = pmon.p_bot_config['ltoken']
        self.ltuid = pmon.p_bot_config['ltuid']
        self.reminders = []
        self.__load()

    def __load(self):
        '''
        Loads the database
        '''
        if exists(self.file):
            with open(self.file,'r') as f:
                self.data = load(f)
    
    def __save(self):
        '''
        Saves the database
        '''
        if exists(self.file):
            remove(self.file)
        with open(self.file,'w') as f:
            dump(self.data,f,indent=1)
    
    def if_multiple(self,discord_id: str):
        '''
        Checks if a discord user with id discord_id has mutliple accounts linked.

        Returns:
            True if he has multiple accounts
            False if he has only one linked
            None if theres no entry in database
        '''
        if discord_id in self.data:
            if 'servers' in self.data[discord_id]:
                if len(self.data[discord_id]['servers']) > 1:
                    return True
                else:
                    return False
            return None
        return None

   

    def set_world_level(self, member: Member,region: str, wl: str):
        id_ = str(member.id)
        region = region.lower()
        if id_ in self.data:
            print(self.data[id_])
            if 'wl' in self.data[id_]:
                print(self.data[id_]['wl'])
                if region in self.allowed:                    
                    self.data[id_]['wl'][region] = wl
                    self.__save()
                    return True
                else:
                    self.data[id_]['wl'][region] = wl
                    self.__save()
                    return True

            else:
                if region in self.allowed:
                    self.data[id_]['wl'] = {region:  wl}
                    self.__save()
                    return True

    def get_wls(self,discord_id: str):
        '''
        All the servers discord user with id discord_id has linked in database.

        Returns:
            dict with regions and uid
            if none found, returns None
        '''
        if discord_id in self.data:
            if 'wl' in self.data[discord_id]:                
                return self.data[discord_id]['wl']
            return None
        return None






    def fetch_key(self,key, dict_, type_ = None):
        if key in dict_:
            if type_ is not None:
                if dict_[key] == type_:
                    return ','.join(dict_[key])
            else:
                return dict_[key]
        else:
            return ''

    def prettify_abyss(self,data):

        main_stats = {}
        main_stats['season'] = self.fetch_key('season',data)
        main_stats['start_time'] = self.fetch_key('season_start_time',data)
        main_stats['end_time'] = self.fetch_key('season_end_time',data)
        stats_data = self.fetch_key('stats',data)
        if stats_data != '':
            main_stats['total_battles'] = self.fetch_key('total_battles',stats_data)
            main_stats['total_wins'] = self.fetch_key('total_wins',stats_data)   
            main_stats['total_stars'] = self.fetch_key('total_stars',stats_data) 
            main_stats['max_floor'] = self.fetch_key('max_floor',stats_data) 
        character_ranks = self.fetch_key('character_ranks',data)
        most_played_characters = self.fetch_key('most_played',character_ranks)
        if bool(most_played_characters):
            list_ = [f"{char['name']} - {char['rarity']}" for char in most_played_characters]            
            played_text = '\n'.join(list_[:3])
            main_stats['most_played'] = played_text
        most_kills = self.fetch_key('most_kills',character_ranks)
        main_stats['most_kills'] = ''
        if bool(most_kills):
            list_ = [f"{char['name']} - {char['value']}" for char in most_kills]            
            kill_text = '\n'.join(list_[:3])
            main_stats['most_kills'] = kill_text
        strongest_strike = self.fetch_key('strongest_strike',character_ranks)
        if bool(strongest_strike):
            strike_text = f"{strongest_strike[0]['name']} - {strongest_strike[0]['value']}"
            main_stats['strongest_strike'] = strike_text
        most_damage_taken = self.fetch_key('most_damage_taken',character_ranks)
        if bool(most_damage_taken):
            list_ = [f"{char['name']} - {char['value']}" for char in most_damage_taken]            
            dmg_text = '\n'.join(list_[:3])
            main_stats['most_damage_taken'] = dmg_text
        most_bursts_used = self.fetch_key('most_bursts_used',character_ranks)
        if bool(most_bursts_used):
            list_ = [f"{char['name']} - {char['value']}" for char in most_bursts_used]
            
            dmg_text = '\n'.join(list_[:3])
            main_stats['most_bursts_used'] = dmg_text
        most_skills_used = self.fetch_key('most_skills_used',character_ranks)
        if bool(most_skills_used):
            list_ = [f"{char['name']} - {char['value']}" for char in most_skills_used]            
            skill_text = '\n'.join(list_[:3])
            main_stats['most_skills_used'] = skill_text
        floor_stats = {}
        floors = self.fetch_key('floors',data)
        if bool(floors):
            for floor in floors:
                floor_dict = {}
                floor_number = self.fetch_key('floor',floor)
                floor_stars = self.fetch_key('stars',floor)
                floor_maxstars = self.fetch_key('max_stars',floor)
                chambers = self.fetch_key('chambers',floor)
                if bool(chambers):
                    for chamber in chambers:
                        chamber_dict = {}
                        chamber_number = self.fetch_key('chamber',chamber)
                        chamber_stars = self.fetch_key('stars',chamber)
                        chamber_maxstars = self.fetch_key('max_stars',chamber)
                        halves = chamber['has_halves']
                        if halves:
                            battles = chamber['battles']
                            if bool(battles):
                                for battle in battles:
                                    battle_dict = {}
                                    battle_half = self.fetch_key('half',battle)
                                    characters = self.fetch_key('characters',battle)
                                    if bool(characters):
                                        text = '\n'.join([f"{char['name']} - LVL {char['level']}" for char in characters]) 
                                    battle_dict['half'] = 'First' if battle_half == 1 else 'Second'
                                    battle_dict['characters'] = text
                                    chamber_dict[f"{battle_dict['half']} Half"] = battle_dict
                        chamber_dict['stars'] = chamber_stars
                        chamber_dict['max_stars'] = chamber_maxstars
                        floor_dict[f'Chamber {chamber_number}'] = chamber_dict
                floor_dict['stars'] = floor_stars
                floor_dict['max_stars'] = floor_maxstars
                floor_stats[f"Floor - {floor_number}"] = floor_dict
        return main_stats, floor_stats


    async def add_resin_reminder(self,member: Member, region: str, resin: int, ctx: Context = None, base_loop: bool= False, base_delay: int = 0):

        check = self.get_resin_reminder(str(member.id), region)
        if check is not None:
            self.reminders.pop(self.reminders.index(check))

        reminder = await reminder_set({}, self, self.pmon, member, region, resin, ctx,base_loop, base_delay)
        self.reminders.append(reminder)
        return reminder

    async def load_resin_reminder(self):
        
        if len(self.reminders) != 0:
            return None

        files = [join(f'{getcwd()}/assets/resin/',f) for f in listdir(f'{getcwd()}/assets/resin/') if isfile(join(f'{getcwd()}/assets/resin/',f))]
        for file in files:
            with open(file,'r') as f:
                data = load(f)
            if datetime.strptime(data['full_time'],'%c') < datetime.now():
                pass
            else:
                remind = await reminder_set(data,self , self.pmon)
                self.reminders.append(remind)
        
        return True

    def get_resin_reminder(self, discord_id: str, region: str):
        if len(self.reminders) != 0:
            for remind in self.reminders:
                if remind.discord_id == discord_id and remind.region == region:
                    return remind

    def get_servers(self,discord_id: str):
        '''
        All the servers discord user with id discord_id has linked in database.

        Returns:
            dict with regions and uid
            if none found, returns None
        '''
        if discord_id in self.data:
            if 'servers' in self.data[discord_id]:                
                return self.data[discord_id]['servers']
            return None
        return None

    def get_discord_user_from_uid(self, uid :str ):
        '''
        Gets discord user from uid

        '''
        members = self.pmon.guilds[0].members

        for discord_id in self.data:
            uid_data = self.data[discord_id]['servers']
            uids = list(uid_data.values())
            if int(uid) in uids:
                server = list(uid_data.keys())[list(uid_data.values()).index(int(uid))]
                user = get(members,id=int(discord_id))
                return user, server
        return None,None
            


    def get_uid(self,discord_id: str,server_region: str):
        '''
        This gets the uid for discord user with id discord_id and region server_region
        Returns:
            uid: str
        '''
        check = self.if_multiple(discord_id)
        if discord_id in self.data: 
            if server_region in self.data[discord_id]['servers']:
                return self.data[discord_id]['servers'][server_region]
            else:
                if 'none' in self.data[discord_id]['servers']:
                    return self.data[discord_id]['servers']['none']        
        return None
    
    def save_server(self,discord_id: str,server_region: str,uid: int):
        '''
        Saves the entry for discord user with discord_id, and region server_region with uid

        Returns:            
            if linked:
                [dict containing servers of a user with discord_id, bool True]
            else:
                [empty dict, bool None]
        '''
        temp_ = {}
        if discord_id in self.data:
            if 'servers' in self.data[discord_id]:
                if server_region in self.data[discord_id]['servers']:

                    # Updates the linked server_region 
                    # in database

                    self.data[discord_id]['servers'][server_region] = uid
                else:

                    # Add if the server_region 
                    # is not linked in database                   

                    if server_region in self.allowed:
                        temp_ = self.data[discord_id]['servers']
                        temp_[server_region] = uid
                        self.data[discord_id]['servers'] = temp_
                        
            else:

                # if server key does not exist in
                # database adds the server key for user discord_id

                temp_ = self.data[discord_id]
                if server_region in self.allowed:
                    temp_['servers'] = {server_region: uid}
                    self.data[discord_id] = temp_
                print(f'server key was not found now added, {temp_}')
        else:           

            # adds the new entry for discord_id 
            # if it does not exist in database and links the account
             
            if server_region in self.allowed:
                temp_['servers'] = {server_region: uid}
                self.data[discord_id] = temp_
                   
        if discord_id in self.data:
            return self.data[discord_id],True
        else:
            return {},None



    # note: new method. because you don't need to type
    # server name. it can be figured out.
    def save_uid(self, discord_id: str, uid: int):
        '''
        Saves and detects regions from just uid
        '''

        server = str(uid)[0]

        # asia server
        if str(uid)[0] == '6':
            server = 'na'
        elif server == '7':
            server = 'eu'
        elif server == '8':
            server = 'asia'
        elif server == '9':
            server = 'tw'
        else:
            server = None

        self.save_server(discord_id, server, uid)

        self.__save()

    def get_server_region(self, uid:int):
        server = str(uid)[0]

        # asia server
        if str(uid)[0] == '6':
            server = 'na'
        elif server == '7':
            server = 'eu'
        elif server == '8':
            server = 'asia'
        elif server == '9':
            server = 'tw'
        else:
            server = None
        return server

    def prettify_linked_message(self, username: str , uid: int):
        '''

        Generates a prettified linked message!

        '''

        server = self.get_server_region(uid)

        if server:        
            return f'{username} : Region **{server.upper()}** | UID {uid} linked!'
        else:
            return f'{username} : Region **Not Found** | UID {uid} linked!'
            

    def parse_discord_message(self,discord_id: str, discord_message: str, seperator: str=':', first_part_region: bool = True):    
        '''
        Parses discord message for region and uids having seperator

        example
        if first_part_region is True:
            region [seperator] uid
        if first_part_region is False:
            uid [seperator] region

        Returns:
            linked_dict: dict containing user ids and region
            check: true or false depending on action succeeded or failed
        '''

        # Allowed servers format
        
        allowed_format = "asia:eu:europe:na:northamerica".split(':')
        region_part = 1
        if first_part_region:
            region_part = 0

        # Split discord_message 
        # into lines

        linked_dict = {}
        check = None
        lines = discord_message.splitlines()
        for line in lines:
            seperated_line = line.split(seperator)
            _iterable = (len(seperated_line) > 1)
            if _iterable:
                server_region = seperated_line[region_part].lstrip().rstrip().lower()
                uid = -1
                if seperated_line[abs(region_part-1)].lstrip().rstrip().isdigit():
                    uid = int(seperated_line[abs(region_part-1)].lstrip().rstrip())
                try:
                    server_index = allowed_format.index(server_region)
                except:                    
                    return {},None
                else:
                    if server_index > 0 and server_index % 2 == 0:
                        server_index -= 1
                    linked_dict,check = self.save_server(discord_id,allowed_format[server_index],uid)
            else:
                return {},None
                    
        self.__save()
        return linked_dict,check
            
    def get_uiddata(self,uid): 
        '''
        Fetches Genshin Profile data from hoyolab api
        if data is not public:
            returns None
        '''
        data = {}
        try:
            gs.set_cookie(ltuid=self.ltuid,ltoken=self.ltoken)
            data = {}
            if isinstance(uid,int):
                data = gs.get_all_user_data(uid)
            else:
                data = gs.get_all_user_data(uid)
            return data
        except gs.errors.DataNotPublic:
                return None
        
    
    def get_genshinstats(self,uid: int ):  
        '''
            Gets only stats portion of data fetched from get_uiddata
            returns:
                stats dict, icon url
        '''      
        try:
            gs.set_cookie(ltuid=self.ltuid,ltoken=self.ltoken)
            data = {}
            if isinstance(uid,int):
                data = gs.get_user_stats(uid)
            else:
                data = gs.get_user_stats(uid)
        except gs.errors.DataNotPublic:
                return None,None
        else:
            if len(data) > 1:
                stats_temp = data['stats']
                stats = {}
                for i in stats_temp:
                    if i != 'icon':
                        stats[i.replace('_'," ",99).title()] = stats_temp[i]
                return stats,data['characters'][0]['icon']

    def get_genshinabyss(self,uid: int ):  
        '''
            Gets only stats portion of data fetched from get_uiddata
            returns:
                stats dict, icon url
        '''      
        try:
            gs.set_cookie(ltuid=self.ltuid,ltoken=self.ltoken)
            data = {}
            if isinstance(uid,int):
                data = gs.get_spiral_abyss(uid)
            else:
                data = gs.get_spiral_abyss(uid)
        except gs.errors.DataNotPublic:
                return None,None
        else:
            if bool(data):
                return self.prettify_abyss(data)
            else:
                return None,None

    def get_genshincharacters(self, uid, character_id : int = None):
        '''
            Gets only stats portion of data fetched from get_uiddata
            Returns:
                characters: list
                weapons: list

        '''        
        characters_ = []
        weapons_ = []
        try:
            gs.set_cookie(ltuid=self.ltuid,ltoken=self.ltoken)
            data = {}
            if character_id is not None:
                data = gs.get_characters(uid,character_ids=[character_id])
            else:
                data = gs.get_characters(uid)
            
                
        except gs.errors.DataNotPublic:
                return None,None
        else:                

            for item in data:
                characters_dict = {}
                for item_key in item:  
                    if item_key == 'id':
                        id_ = item[item_key]  
                    else:
                        if item_key == 'weapon':
                            weapons_.append(item[item_key])
                        else:                       
                            characters_dict[item_key] = item[item_key]          
                characters_.append(characters_dict) 
                
            return characters_,weapons_
                

    def create_stats_embed(self, member: Member, uid: int):
        '''
        Creates statss embed.

        returns:
            embed: Embed
        '''

        stats,icon = self.get_genshinstats(uid)
        if stats is not None and icon is not None:

            embed = Embed(title=f'Genshin Impact Profile stats',description="",color=0xf5e0d0)
            embed.set_author(name=member.display_name,
                            icon_url=member.avatar.url)
            for i in stats:
                embed.add_field(name=f'{i}',value=f'{stats[i]}',inline=True)
            embed.set_thumbnail(url=icon)

            return embed

    def create_abyss_embeds(self, member: Member, uid: int):
        '''
        Creates statss embed.

        returns:
            embed: Embed
        '''
        embeds = {}
        main_stats,floor_stats = self.get_genshinabyss(uid)
        if main_stats is not None and main_stats is not None:
            description = ''
            
            main_embed = Embed(title=f'Genshin Impact Abyss Stats',color=0xf5e0d0)
            for key in main_stats:
                main_embed.add_field(name=key.replace('_',' ',99).title(),value=main_stats[key]) 
            
            main_embed.set_author(name=member.display_name,
                            icon_url=member.avatar.url)
            main_embed.set_thumbnail(url='https://static.wikia.nocookie.net/gensin-impact/images/c/ce/Enemy_Abyss_Lector_Violet_Lightning.png')
            embeds['Main Information'] = main_embed

            for floor in floor_stats:
                description = ''
                if 'stars' in floor_stats[floor]:
                    description += f"Stars: {('⭐' * int(floor_stats[floor]['stars']))}"
                if 'max_stars' in floor_stats[floor]:
                    description += f"\nMax stars {('⭐' * int(floor_stats[floor]['max_stars']))}"
                embed = Embed(title=floor,description=description,color=0xf5e0d0)
                chambers = [chamber for chamber in floor_stats[floor] if type(floor_stats[floor][chamber]) == dict]
                
                
                for chamber in chambers:
                    chamber_description = ''
                    key_name = chamber
                    if 'stars' in floor_stats[floor]:
                        chamber_description += f"Stars: {('⭐' * int(floor_stats[floor][chamber]['stars']))}"
                    if 'max_stars' in floor_stats[floor]:
                        chamber_description += f"\nMax stars {('⭐' * int(floor_stats[floor][chamber]['max_stars']))}"
                    halves = [half for half in floor_stats[floor][chamber] if type(floor_stats[floor][chamber][half]) == dict]
                    halv_description = ""
                    for halv in halves:
                        halv_name = halv
                        halv_description += f"\n**__{halv_name}__**\n{floor_stats[floor][chamber][halv]['characters']}"
                    chamber_description += f'\n{halv_description}'
                    embed.add_field(name=key_name,value=chamber_description)
                embed.set_thumbnail(url='https://static.wikia.nocookie.net/gensin-impact/images/c/ce/Enemy_Abyss_Lector_Violet_Lightning.png')
                embeds[floor] = embed
            return embeds



    def create_characters_embed(self,uid: int):
        '''
        Creates characters embed.

        returns:
            embeds: list
            emojis: list
        '''
        
        embeds = {}

        
        characters_,weapons = self.get_genshincharacters(uid)

        if characters_ is not None and weapons is not None:
        
            for no in range(0,len(characters_),1):

                            
                embed_char = Embed(title=f"Character stats",color=0xf5e0d0)
                for i in characters_[no]:

                    # omits image,icon
                    #   artifacts contains nested dict
                    #   constellation contains nested dict
                    #   outfits contains nested dict
                    
                    if i != 'name' and i != 'icon'and i != 'artifacts' and i != 'image' and i != 'constellations' and i != 'outfits':
                        embed_char.add_field(name=f"{i.replace('_',' ',99).title()}",value=characters_[no][i],inline=True)
                embed_char.set_author(name=f"{characters_[no]['name']}",icon_url=f"{characters_[no]['icon']}")
                embed_weapon = Embed(title=f"Weapon stats",color=0xf5e0d0)            
                for i in weapons[no]:
                    if i != 'name' and i != 'icon':
                        embed_weapon.add_field(name=f"{i.replace('_',' ',99).title()}",value=weapons[no][i],inline=True)  
                embed_weapon.set_author(name=f"{characters_[no]['name']} {weapons[no]['name']}",icon_url=f"{weapons[no]['icon']}")   

                embeds[str(no)] = {'character': embed_char,'weapon': embed_weapon}

        if len(embeds) > 1:
            emojis = ['⬅️','➡️','⚔️']
        else:
            emojis = ['⚔️']
        return embeds,emojis
        


        



