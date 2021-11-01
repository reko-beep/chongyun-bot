
from nextcord.ext import commands,tasks
from nextcord import Embed
from core.paimon import Paimon

from os import listdir,getcwd,remove
from os.path import isfile, join,exists

from json import dump,load
import genshinstats as gs

class GenshinDB():
    def __init__(self, pmon: Paimon):
        self.path = getcwd()
        self.file = 'genshin.json'
        self.data = {}
        self.allowed = ['eu','na','asia']        
        self.ltoken = pmon.p_bot_config['ltoken']
        self.ltuid = pmon.p_bot_config['luid']
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



    def get_uid(self,discord_id: str,server_region: str):
        '''
        This gets the uid for discord user with id discord_id and region server_region
        Returns:
            uid: str
        '''
        check = self.if_multiple(discord_id)
        print(check)    
        if server_region in self.data[discord_id]['servers']:
            print(self.data[discord_id]['servers'][server_region])
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

    def prettify_linked_message(self, server_region: str, uid: int):
        '''

        Generates a prettified linked message!

        '''

        # Allowed servers format
        
        allowed_format = "asia:eu:europe:na:northamerica".split(':')
        server_index = -1
        try:
            server_index = allowed_format.index(server_region)
        except:
            return None
        else:
            if server_index > 0 and server_index % 2 == 0:
                server_index -= 1

            return f'Region {allowed_format[server_index]} | UID {uid} linked!'
            

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
            print(seperated_line,_iterable)
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
        
    
    def get_genshinstats(self,data):  
        '''
            Gets only stats portion of data fetched from get_uiddata
            returns:
                stats dict, icon url
        '''      
        if len(data) > 1:
            stats_temp = data['stats']
            stats = {}
            for i in stats:
                if i != 'icon':
                    stats[i.replace('_'," ",99).title()] = stats_temp[i]
            return stats,data['characters'][0]['icon']
    
    def get_genshincharacters(self, data):
        '''
            Gets only stats portion of data fetched from get_uiddata
            Returns:
                characters: list
                weapons: list

        '''        
        characters_ = []
        weapons_ = []
       
        if len(data) > 1:
            if 'characters' in data:
                for item in data['characters']:
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
                

    def create_stats_embed(self, uid_data:dict):
        if len(uid_data) > 1:
            '''
            Creates statss embed.

            returns:
                embed: Embed
            '''

            stats,icon = self.get_genshinstats(uid_data)

            embed = Embed(title=f'Genshin Impact Profile stats',description="",color=0xf5e0d0)
            for i in stats:
                embed.add_field(name=f'{i}',value=f'{stats[i]}',inline=True)
            embed.set_thumbnail(url=icon)

            return embed

    def create_characters_embed(self,uid_data:dict):
        '''
        Creates characters embed.

        returns:
            embeds: list
            emojis: list
        '''
        
        embeds = {}

        if len(uid_data) > 1:

            characters_,weapons = self.get_genshincharacters(uid_data)
           
            for no in range(0,len(characters_),1):

                characters_[no].pop('name')
                weapons[no].pop('name')
                          
                embed_char = Embed(title=f"{characters_[no]['name']}",color=0xf5e0d0)
                for i in characters_[no]:

                    # omits image,icon
                    #   artifacts contains nested dict
                    #   constellation contains nested dict
                    #   outfits contains nested dict

                    if i != 'icon'and i != 'artifacts' and i != 'image' and i != 'constellations' and i != 'outfits':
                        print(f'{i} added')
                        embed_char.add_field(name=f"{i.replace('_',' ',99).title()}",value=characters_[no][i],inline=True)
                embed_char.set_thumbnail(url=f"{characters_[no]['icon']}")
                embed_char.set_image(url=f"{characters_[no]['image']}")

                embed_weapon = Embed(title=f"{characters_[no]['name']} {weapons[no]['name']}",color=0xf5e0d0)            
                for i in weapons[no]:
                    if i != 'icon':
                        embed_weapon.add_field(name=f"{i.replace('_',' ',99).title()}",value=weapons[no][i],inline=True)               
                embed_weapon.set_thumbnail(url=f"{weapons[no]['icon']}")

                embeds[str(no)] = {'character': embed_char,'weapon': embed_weapon}

        if len(embeds) > 1:
            emojis = ['⬅️','➡️','⚔️']
        else:
            emojis = ['⚔️']
        return embeds,emojis
        


        





        
