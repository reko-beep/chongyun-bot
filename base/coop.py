from json import load, dump
from base.resource_manager import ResourceManager

from nextcord import Member

from os.path import exists

class CoopManager:
    def __init__(self, res: ResourceManager):
        self.res = res
        self.coop_path = self.res.db.format(path='coop.json')
        self.coop_data = {}
        self.domains = {
            "boss": [
                'childe',
                'azdaha',   
                'signora',             
                'dvalin',
                'shogun'
            ],
            "mastery": [
                'liyue',
                'mondstadt',
                'inazuma'
            ],
            "forgery": [
                'liyue',
                'mondstadt'
                'inazuma'
            ],
            "blessings": [
                'liyue',
                'mondstadt',
                'inazuma'
            ]
        }
        self.domains_map = {
            "Trounce Domains": [
                'Enter the Golden House',
                'Beneath the Dragon-Queller',
                'Narukami Island: Tenshukaku',
                'Confront Stormterror',
                'End of the Oneiric Euthymia'                
            ],
            "Domains of Mastery": [
                "Taishan Mansion",
                "Forsaken Rift",
                "Violet Court"
            ],
            "Domains of Forgery": [
                "Hidden Palace of Lianshan Formula",
                "Cecilia Garden",
                "Court of Flowing Sand"
            ],
            "Domains of Blessing": [
                "Domain of Guyun\nRidge Watch\nHidden Palace of Zhour Formula\nThe Lost Valley\nClear Pool and Mountain Cavern",
                "Midsummer Courtyard\nValley of Rememberance\nPeak of Vindagnyr",
                "Momiji-Dyed Court\nSlumbering Court\n"
            ]
        }
        self.leylines = [
            'wealth',
            'revelation'
        ]
        self.leylines_map = [
            'Blossoms of Wealth',
            'Blossoms of Revelation'
        ]
        self.__load()


    def __load(self):
        if exists(self.coop_path):
            with open(self.coop_path, 'r') as f:
                self.coop_data = load(f)

    def __save(self):
        
        with open(self.coop_path, 'w') as f:
            dump(self.coop_data, f, indent=1)


    def generate_profile(self, discord_member: Member):

        discord_id = str(discord_member.id)

        if discord_id in self.coop_data:
            self.coop_data[discord_id] = {
                'profiles': {},
                'leylines' : [],
                'domains' : [],
                'points' : 0,
                'points_to_give' : 0
            }
        
        else:
            self.coop_data[discord_id] = {
                'profiles': {},
                'world_level': 0,
                'leylines' : [],
                'domains' : [],
                'points' : 0,
                'points_to_give' : 0
            }
    
    def get_server_region(self, **kwargs):
        from_uid = kwargs.get("uid", -1)
        region_str = kwargs.get("region", '').lower()
        if from_uid != -1:
            uid = from_uid
            if type(from_uid) == int:
                uid = str(from_uid)
            
            if uid[0] == '8':
                return 'asia'
            if uid[0] == '7':
                return 'eu'
            if uid[0] == '6':
                return 'na'
            
        if region_str != '':
            allowed :list = 'asia:asia:eu:europe:na:northamerica'.split(":")
            try:
                index = allowed.index(region_str)
            except ValueError:
                pass
            else:
                if index // 2 != 0:
                    return allowed[index-1]
                else:
                    return allowed[index]

    def get_domains_map(self, type_key: str , sub_key:str):

        if type_key in self.domains:
            try:
                index = self.domains[type_key].index(sub_key)
            except ValueError:
                pass
            else:
                main_index = list(self.domains.keys()).index(type_key)
                map_key = list(self.domains_map.keys())[main_index]
                return f'{map_key}, {self.domains_map[map_key][index]}'

    
    def get_leylines_map(self, key: str):

        if key in self.leylines:
            try:
                index = self.leylines.index(key)
            except ValueError:
                pass
            else:                
                map_key = self.leylines_map[index]
                return f'{map_key}'




    def set_rank(self, discord_member: Member, server_region:str, rank:int):

        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)

        region_check = self.get_server_region(region=server_region)
        if region_check is not None:
            if region_check in self.coop_data[discord_id]['profiles']:
                self.coop_data[discord_id]['profiles'][region_check]['rank'] = rank 
            else:
                self.coop_data[discord_id]['profiles'][region_check] = {}
                self.coop_data[discord_id]['profiles'][region_check]['rank'] =  rank
            self.__save()
            return True
            
            
    
    def set_wordlevel(self, discord_member: Member, server_region:str, world_level:int):
        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)

        region_check = self.get_server_region(region=server_region)
        if region_check is not None:
            if region_check in self.coop_data[discord_id]['profiles']:
                self.coop_data[discord_id]['profiles'][region_check]['world_level'] = world_level
            else:
                self.coop_data[discord_id]['profiles'][region_check] = {}
                self.coop_data[discord_id]['profiles'][region_check]['world_level'] =  world_level
            self.__save()
            return True

    def set_uid(self, discord_member: Member,  uid:int):
        discord_id = str(discord_member.id)
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)

        region = self.get_server_region(uid=uid)
        if region is not None:
            if region in self.coop_data[discord_id]['profiles']:
                self.coop_data[discord_id]['profiles'][region]['uid'] = uid
            else:
                self.coop_data[discord_id]['profiles'][region] = {}
                self.coop_data[discord_id]['profiles'][region]['uid'] = uid
            self.__save()
            return True   
        
    def add_domain(self, discord_member: Member, domain_type:str, sub_key : str):
        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        
        check = self.get_domains_map(domain_type, sub_key)
        if check is not None:
            self.coop_data[discord_id]['domains'].append({domain_type: sub_key})
            self.__save()
            return True
    
    def remove_domain(self, discord_member: Member, domain_type:str, sub_key:str):
        discord_id = str(discord_member.id)

        if discord_id in self.coop_data:

            try:
                index = self.coop_data[discord_id]['domains'].index({domain_type: sub_key})
            except ValueError:
                pass
            else:
                self.coop_data[discord_id]['domains'].pop(index)
                self.__save()
                return True
    
    def add_leyline(self, discord_member: Member, key : str):
        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        
        check = self.get_leylines_map(key)
        if check is not None:
            self.coop_data[discord_id]['leylines'].append(key)
            self.__save()
            return True
    
    def remove_leyline(self, discord_member: Member, key:str):
        discord_id = str(discord_member.id)

        if discord_id in self.coop_data:

            try:
                index = self.coop_data[discord_id]['leylines'].index(key)
            except ValueError:
                pass
            else:
                self.coop_data[discord_id]['leylines'].pop(index)
                self.__save()
                return True

    def add_eligible_point(self, discord_member: Member):
        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        
        self.coop_data[discord_id]['points_to_give'] += 1
        self.__save()
        return True
    
    def remove_eligible_point(self, discord_member: Member, all:bool = False):
        discord_id = str(discord_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        
        if self.coop_data[discord_id]['points_to_give'] > 0:
            if all:
                self.coop_data[discord_id]['points_to_give'] = 0
                self.__save()
                return True
            else:
                self.coop_data[discord_id]['points_to_give'] -= 1
                self.__save()
                return True
    
    def add_point(self, discord_member: Member, give_to_member:Member):
        discord_id = str(discord_member.id)
        receiver_id = str(give_to_member.id)

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        if receiver_id not in self.coop_data:
            self.generate_profile(give_to_member)
        
        if self.ban_check(discord_member) is None:
            if self.coop_data[discord_id]['points_to_give'] > 0:
                self.coop_data[discord_id]['points_to_give'] -= 1
                self.coop_data[receiver_id]['points'] += 1
                self.__save()
                return True

    def ban_check(self, discord_member: Member):
        if 'banned' in self.coop_data:
            return str(discord_member.id) in self.coop_data['banned']

    def ban_from_coop(self, discord_member: Member):
        if 'banned' in self.coop_data:
            if str(discord_member.id) not in self.coop_data['banned']:
                self.coop_data['banned'].append(str(discord_member.id))
                self.__save()
                return True
            return False
        else:
            self.coop_data['banned'] = [str(discord_member.id)]
            self.__save()
            return True
    
    def reset_coop_points(self):
        for discord_id in self.coop_data:
            if discord_id != 'banned':
                self.coop_data[discord_id]['points'] = 0
                self.coop_data[discord_id]['points_to_give'] = 0
        self.__save() 
        return True
    
    def prettify_data(self, discord_member: Member):
        discord_id = str(discord_member.id)

        data = {

        }

        if discord_id in self.coop_data:

            d_ = self.coop_data[discord_id]

            profiles = d_['profiles']
            data['profiles'] = ''
            if len(profiles) > 0:                
                data['profiles'] += '**Accounts:**\n'
                for prof in profiles:
                    data['profiles'] += f"**{prof.upper()}**\n__UID__: {profiles[prof].get('uid','Not setup yet')}\n__World Level__: {profiles[prof].get('world_level','Not setup yet')}\n__AR__: {profiles[prof].get('rank','Not setup yet')}\n"

            else:
                data['profiles'] = '**Accounts:**\nNone linked!'
            
            domains = d_['domains']
            if len(domains) > 0:
                data['domains'] = '**Domains:**\n'
                for dom in domains:
                    dom_type = list(dom.keys())[0]
                    dom_key = dom[dom_type]

                    domain_name = self.get_domains_map(dom_type, dom_key)
                    if domain_name is not None:
                        data['domains'] += f"**{domain_name.split(',')[0]}**: *{domain_name.split(',')[1].strip()}, {dom_key.title().strip()}*\n"
            else:
                data['domains'] = '**Domains:**\nNot setup yet!'
            
            leylines = d_['leylines']
            if len(leylines) > 0:
                data['leylines'] = '**Leylines:**\n'
                for ley in leylines:
                    leyline_name = self.get_leylines_map(ley)
                    if leyline_name is not None:
                        data['leylines'] += f"*{leyline_name}*\n"
            else:
                data['leylines'] = '**Leylines:**\nNot setup yet!'
            
            data['points'] = f"**Co op Points:** {d_['points']}\n*{d_['points_to_give']} can be given to other players*"

        return data

    def parse_arg(self, discord_member: Member, opr: str, type_: str, name:str='', value:str = ''):
        funcs = {
            'add': {
                'domains' : self.add_domain,
                'leylines': self.add_leyline,
                'wl': self.set_wordlevel,
                'rank': self.set_rank,
                'uid': self.set_uid
            },
            'remove': {
                'domains': self.remove_domain,
                'leylines': self.remove_leyline                
            }
        }

        if opr in list(funcs.keys()):
            if type_ in list(funcs[opr].keys()):
                print('args', opr, type_, name, value)
                if type_ in ['leylines', 'uid']:
                    check = funcs[opr][type_](discord_member, name)          
                else:
                    check = funcs[opr][type_](discord_member,name,  value)
                print(check)
                if check is not None:
                    return True

                # returns available parameters    
                if name in list(self.__dict__[type_].keys()):
                    if type(self.__dict__[type_][name]) == list:
                        return self.__dict__[type_][name]
                    else:
                        return list(self.__dict__[type_][name].keys())
                else:
                    if type(self.__dict__[type_]) == list:
                        return self.__dict__[type_]
                    else:
                        return list(self.__dict__[type_].keys())

            else:
                print(funcs[opr].keys())
                return list(funcs[opr].keys())
        else:
            print(funcs.keys())
            return list(funcs.keys())
                    

rm = ResourceManager()
test = CoopManager(rm)

print(test.get_server_region(uid=8126127612))