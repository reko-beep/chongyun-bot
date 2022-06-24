
from dis import disco
from json import load, dump
from base.liben import LibenManager
from base.resource_manager import ResourceManager
from base.utils import get_ordered_dicts, paginator
from base.calculator import StatCalculator

from nextcord import Member, Message, Embed
from nextcord.utils import get
from datetime import datetime
from os.path import exists
import genshinstats as gs

from dev_log import logc
class CoopManager:
    def __init__(self, bot):
        self.bot = bot
        self.res = bot.resource_manager
        self.coop_path = self.res.db.format(path='coop.json')
        self.coop_data = {}
        self.liben = LibenManager(self.bot)
        self.calculator = StatCalculator(bot)

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
                'mondstadt',
                'inazuma'
            ],
            "blessings": [
                'liyue',
                'mondstadt',
                'inazuma'
            ],
            "all" : [
                "all"
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
            ],
            "Domains" : [
                "All Domains"
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
        print(region_str)
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
            allowed :list = ['asia','asia','eu','europe','na','northamerica']
            
            try:
                index = allowed.index(region_str)
                print('index found', index)
            except ValueError:                
                pass
            else:              
                if index % 2 != 0:                    
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
    
    def unban_from_coop(self, discord_member: Member):
        if 'banned' in self.coop_data:
            if str(discord_member.id) in self.coop_data['banned']:
                list_ = [r for r in self.coop_data['banned'] if r!=str(discord_member.id)]            
                self.coop_data['banned'] = list_
                self.__save()
                return True            
            return False
        

    def warn_system(self, discord_member: Member, message: Message):
        if 'warns' not in self.coop_data:
            self.coop_data['warns'] = {}

        discord_id = str(discord_member.id)
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        if 'banned' not in self.coop_data:
            self.coop_data['banned'] = []
        last_message_time = None
        if discord_id in self.coop_data['warns']:
            last_message_time = self.coop_data['warns'][discord_id].get('warn_time', None)
        else:
            self.coop_data['warns'][discord_id] = {}

        if message.author.id == discord_member.id:
            message_time = message.created_at
            if last_message_time is not None:
                lmt_obj = datetime.strptime(last_message_time, '%c %z')
                if (message_time-lmt_obj).seconds < 360:
                    if 'warn_count' not in self.coop_data['warns'][discord_id]:
                        self.coop_data['warns'][discord_id]['warn_count'] = 0
                    self.coop_data['warns'][discord_id]['warn_count'] += 1

                    if int(discord_id) in self.coop_data['banned']: ## if user is already banned
                        return 'BANNED'

                    if self.coop_data['warns'][discord_id]['warn_count'] > 3:      #if warn count is greater than 3 bans the user                   
                        self.coop_data['banned'].append(discord_member.id)
                        self.coop_data['warns'][discord_id]['warn_count'] = 0
                        self.coop_data['warns'][discord_id]['warn_time'] = message_time.strftime("%c %z")
                        return 'BANNED'
                    self.coop_data['warns'][discord_id]['warn_time'] = message_time.strftime("%c %z")
                    return 'WARNED'
                self.coop_data['warns'][discord_id]['warn_time'] = message_time.strftime("%c %z")
            self.coop_data['warns'][discord_id]['warn_time'] = message_time.strftime("%c %z")

        self.__save()

    def add_to_give_points(self, discord_member: Member, points: int):

        discord_id = str(discord_member.id)
        if points > 3:
            points = 3

        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
        
        self.coop_data[discord_id]['points_to_give'] += points
        self.__save()
    
    def add_coop_point(self, giver: Member, discord_member: Member, points: int):
        giver_id = str(giver.id)
        discord_id = str(discord_member.id)

        points_can_be_given = self.coop_data[giver_id]['points_to_give']


        duplicate_check = self.duplicate_point_check(giver, discord_member)
        if duplicate_check is None:
            if points_can_be_given >= points:
                if discord_id not in self.coop_data:
                    self.generate_profile(discord_member)
                self.coop_data[discord_id]['points'] += points
                self.coop_data[giver_id]['points_to_give'] -= points 
                self.__save()
                return True
        else:
            return False

        

    def reset_coop_points(self):
        for discord_id in self.coop_data:
            if discord_id not in ['banned', 'point_check', 'warns']:
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
            if len(profiles) > 0:               
                
                for prof in profiles:
                    data[prof.upper()] = ''
                    data[prof.upper()] += f"UID: {profiles[prof].get('uid','Not setup yet')}\nWorld Level: {profiles[prof].get('world_level','Not setup yet')}\nAR: {profiles[prof].get('rank','Not setup yet')}\n"

            else:
                data['Accounts'] = 'None linked!'
            
            domains = d_['domains']
            if len(domains) > 0:
                for dom in domains:
                    dom_type = list(dom.keys())[0]
                    dom_key = dom[dom_type]

                    domain_name = self.get_domains_map(dom_type, dom_key)
                    if domain_name is not None:
                        if domain_name.split(',')[0] not in data:
                            data[domain_name.split(',')[0]] = ''
                        data[domain_name.split(',')[0]] += f"*{domain_name.split(',')[1].strip()}*, **{dom_key.title().strip()}**\n"
            else:
                data['Info'] = 'You can set domains up by `!cpinfo add domains (boss|liyue|mondstadt|inazuma|all) (blessings|mastery|forgery|all)\n'
            
            leylines = d_['leylines']
            if len(leylines) > 0:
                data['Leylines'] = ''
                for ley in leylines:
                    leyline_name = self.get_leylines_map(ley)
                    if leyline_name is not None:
                        data['Leylines'] += f"*{leyline_name}*\n"
            else:
                if 'Info' in data:
                    data['Info'] += 'You can set leylines up by `!cpinfo add leylines (wealth|revelation)\n'
                else:
                    data['Info'] = 'You can set leylines up by `!cpinfo add leylines (wealth|revelation)\n'

                
            
            data['Co-op Points'] = f"You have {d_['points']} co-op points\n*{d_['points_to_give']} co-op points can be given to other players*"

        return data

    def duplicate_point_check(self, giver: Member, discord_member: Member):
        giver_id = str(giver.id)
        receiver_id = str(discord_member.id)

        if 'point_check' not in self.coop_data:
            self.coop_data['point_check'] = {}        
        if giver_id not in self.coop_data['point_check']:
            self.coop_data['point_check'][giver_id] = {}
        
        if self.coop_data['point_check'][giver_id].get('last_id', None) != None:
            if self.coop_data['point_check'][giver_id]['last_id'] == receiver_id:
                lst_tm = datetime.strptime(self.coop_data['point_check'][giver_id]['last_time'], '%c')
                now_tm = datetime.now()
                print((now_tm-lst_tm).seconds)
                if (now_tm-lst_tm).seconds < 360:
                    return True
            else:
                self.coop_data['point_check'][giver_id]['last_id'] = receiver_id
                self.coop_data['point_check'][giver_id]['last_time'] = datetime.now().strftime('%c')
                self.__save()
        else:
            self.coop_data['point_check'][giver_id]['last_id'] = receiver_id
            self.coop_data['point_check'][giver_id]['last_time'] = datetime.now().strftime('%c')
            self.__save()
            


    def coop_leaderboard(self, bot, guild):

        coop_dict = {}
        for c in self.coop_data:
            if c not in ['banned', 'warns', 'point_check']:
                coop_dict[c] = self.coop_data[c]['points']
        
        ordered = get_ordered_dicts(coop_dict)
        embeds = paginator(bot, guild, ordered, 'Co-op leaderboard', '{key} has **{value}** co-op points!', 10)
        return embeds

    def get_region_from_carry_role(self, role_name:str):
        role_name = role_name.lower().replace("carry", "",99).strip()
        
        print('role_name provided', role_name)
        server = self.get_server_region(region=role_name)
        print('server_returned', server)
        
        return server

    def get_data_from_carry_role(self,discord_member:Member, role_name:str):

        discord_id = str(discord_member.id)

        role_name = role_name.lower().replace("carry", "",99)
        server = self.get_server_region(region=role_name)

        if discord_id in self.coop_data:
            return self.coop_data[discord_id]




        



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
            },
            'set': {
                'image': self.set_image,
                'character': self.set_character,
                'description': self.set_description,
                'color': self.set_color
            }
        }

        if opr in list(funcs.keys()):
            if type_ in list(funcs[opr].keys()):
                print('args', opr, type_, name, value)
                if type_ in ['leylines', 'uid', 'image', 'character', 'color', 'description']:
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
                    
    def set_character(self, discord_member: Member, character_str: str):
        discord_id = str(discord_member.id)
        thumbnail = self.res.genpath('images/thumbnails', self.res.search(character_str, self.res.goto('images/thumbnails').get('files')).replace(' ','%20',999))
        
        if thumbnail.split('/')[-1] == 'None':
            self.coop_data[discord_id]['thumbnail'] = ''
            return True

        
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)            
        self.coop_data[discord_id]['thumbnail'] = thumbnail
        self.__save()
        return True
    
    def get_character(self, discord_member: Member):
        discord_id = str(discord_member.id)   

        
        if discord_id  in self.coop_data:
            if self.coop_data[discord_id].get('thumbnail', None) != None:
                return self.res.convert_to_url(self.coop_data[discord_id].get('thumbnail').replace(" ",'%20',99), True)
            
    
    def set_image(self, discord_member: Member, url: str):
        discord_id = str(discord_member.id)
        url_check = url.startswith('http') and url.split('/')[-1].split('.')[1] in ['png','jpg','jpeg','gif']
   

        
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
            
        self.coop_data[discord_id]['image'] = url
        self.__save()
        return True
    
    def get_image(self, discord_member: Member):
        discord_id = str(discord_member.id)
       
        
        if discord_id  in self.coop_data:
            
            return self.coop_data[discord_id].get('image', None)
    
    def set_color(self, discord_member: Member, color: str):
        discord_id = str(discord_member.id)
        
        if color.isdigit() is False:
            return None
   
        if '0x' in color or '#' in color:
            color = int(color, 16)
        else:
            color = int(color)
        
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
            
        self.coop_data[discord_id]['color'] = color
        self.__save()
        return True

    def set_description(self, discord_member: Member, description: str):
        discord_id = str(discord_member.id)
        
        if description == '':
            description = 'Not yet setup!'
        
        if discord_id not in self.coop_data:
            self.generate_profile(discord_member)
            
        self.coop_data[discord_id]['description'] = description
        self.__save()
        return True
    
    def get_color(self, discord_member: Member):
        discord_id = str(discord_member.id)
        
        
        if discord_id in self.coop_data:
            return self.coop_data[discord_id].get('color', None)
        
           

    def get_description(self, discord_member: Member):
        discord_id = str(discord_member.id)
      
        
        if discord_id  in self.coop_data:            
            return self.coop_data[discord_id].get('description', None)
        
    def get_member_uid(self, member: Member, region: str):

        discord_id = str(member.id)
        if discord_id in self.coop_data:
            d_ = self.coop_data[discord_id]['profiles']
            if region in d_:
                return d_[region].get("uid", None)

    def get_user_data(self, uid: int, options: str):

        if options == 'chars':

            gs.set_cookies(self.bot.b_config.get("cookies"))
            try:
                data = gs.get_characters(uid)
            except gs.DataNotPublic:
                return None
            else:
                
                data_simplified = {'characters': [], 'weapons': [], 'artifacts': []}
                for char in data:
                    emoji = get(self.bot.inf.emojis, name=char['element'].lower()) if self.bot.inf.emojis is not None else ''
                    element = self.bot.resource_manager.get_element(char['element'])
                    if emoji != '':
                        emoji = '<:'+emoji.name+":"+str(emoji.id)+'>'
                    data_simplified['characters'].append({
                        'name': char['name'],
                        'rarity': char['rarity'],
                        'level': char['level'],
                        'element': char['element'] + emoji,
                        'constellation': char['constellation'],
                        'friendship': char['friendship'],
                        'thumb': char['icon'],
                        'embed_color': element.get('color') if element is not None else 19561321,

                    })
                    data_simplified['weapons'].append({
                        'name': char['weapon']['name'],
                        'rarity': char['weapon']['rarity'],
                        'type': char['weapon']['type'],
                        'level': char['weapon']['level'],
                        'refinemeent': char['weapon']['refinement'],
                        'ascension': char['weapon']['refinement'],
                        'description' : char['weapon']['description'],
                        'thumb': char['weapon']['icon']
                    })
                    artis_tally = {}
                    arti_sets = {}
                    
                    artis = char['artifacts']
                    
                    for arti in artis:
                        if arti['set']['name'] not in artis_tally:
                            artis_tally[arti['set']['name']] = {}
                        if arti['set']['name'] not in arti_sets:
                            arti_sets[arti['set']['name']] = {str(e['pieces']): e['effect'] for e in arti['set']['effects']}
                        if 'pieces' not in artis_tally[arti['set']['name']]:
                            artis_tally[arti['set']['name']]['pieces'] = []
                        
                        artis_tally[arti['set']['name']]['pieces'].append({
                            'rarity': arti['rarity'],
                            'level': arti['level'],
                            'piece': arti['pos_name'].title()
                        })
                    for art in artis_tally:
                        d_ = artis_tally[art]
                        pieces = len(d_['pieces'])
                        if pieces < 2:
                            artis_tally[art]['bonus'] = 'N/A'
                        else:
                            if pieces < 4:
                                artis_tally[art]['bonus'] = arti_sets[art]['2']
                            else:
                                artis_tally[art]['bonus'] = arti_sets[art]['4']

                    data_simplified['artifacts'].append(artis_tally)
                
                return data_simplified        

        if options == 'stats':
            gs.set_cookies(self.bot.b_config.get("cookies"))
            try:
                data = gs.get_user_stats(uid)
            except gs.DataNotPublic:
                return None
            else:
                print(list(data.keys()))
                data_simplified = {'stats': {}, 'teapot': {}, 'exploration': {}}
                for sat in  data['stats']:
                    data_simplified['stats'][sat.replace("_"," ",99).title()] = data['stats'][sat]
                
                if 'teapot' in data:
                    if data['teapot'] is not None:
                        data_simplified['teapot']['name'] = data['teapot']["comfort_name"]
                        data_simplified['teapot']['level'] = data['teapot']['level']
                        data_simplified['teapot']['thumb'] = data['teapot']['comfort_icon']
                        data_simplified['teapot']['visitors'] = data['teapot']['visitors']
                        data_simplified['teapot']['realms'] = '🔸' + '\n🔸'.join([f['name'] for f in data['teapot']['realms']])
                        data_simplified['teapot']['items'] = data['teapot']['items']
                        data_simplified['teapot']['comfort'] = data['teapot']['comfort']

                if 'explorations' in data:
                    for exp in data['explorations']:                   
                        temp_dict = {}
                        for k in exp:
                            if k != 'name' and k !='icon':
                                temp_dict[k] = exp[k]
                            else:
                                if k == 'icon':
                                    temp_dict['thumb'] = exp[k]                        
                        temp_dict['offerings'] = 'N/A'
                        if len(exp['offerings']) > 0:
                            print(exp['offerings'])
                            temp_dict['offerings'] = '🔸' + '\n🔸'.join([f['name']+" "+ str(f['level']) for f in exp['offerings']])
                        data_simplified['exploration'][exp['name']] = temp_dict
                    print(data_simplified)
                return data_simplified      

    def create_stat_embeds(self, member: Member, data:dict):

        embeds = []

        stats = data['stats']
        stat_embed = Embed(title='Basic Statistics', color=self.res.get_color_from_image(member.avatar.url))

        for stat in stats:
            stat_embed.add_field(name=stat, value=stats[stat])
        
        stat_embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        stat_embed.set_thumbnail(url=member.avatar.url)
        stat_embed.set_footer(text=f' {member.display_name} - Basic Statistics')
        embeds.append(stat_embed)

        teapot = data['teapot']
        if len(teapot) != 0:
            tp_embed = Embed(title=f"Teapot - {teapot['name']}", color=self.res.get_color_from_image(member.avatar.url))

            for key in teapot:
                if key != 'thumb':
                    tp_embed.add_field(name=key.title(), value=teapot[key])
            
            tp_embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            tp_embed.set_thumbnail(url=member.avatar.url)
            if teapot['thumb'].startswith("http"):
                tp_embed.set_image(url=teapot['thumb'])
            tp_embed.set_footer(text=f' {member.display_name} - Teapot')
            embeds.append(tp_embed)
        exps = data['exploration']
        if len(exps) != 0:
            embed = Embed(title=f"Exploration", color=self.res.get_color_from_image(member.avatar.url))
            
            for exp in exps:
                desc_ = ''                
                desc_ += "```css\n"     
                for key in exps[exp]:
                    if key != 'thumb':                                           
                        desc_ += f"{key.title()} : {exps[exp][key]}"
                        if key == 'explored':
                            desc_ += '%'
                        desc_ += '\n'
                desc_  += "\n```"
                embed.add_field(name=exp, value=desc_)
            
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f' {member.display_name} - Exploration')

            embeds.append(embed)

        return embeds


    def create_char_embeds(self, data: dict):

        embeds = {'characters': [], 'weapons': [], 'artifacts': [], 'stats': []}
        keys = list(data.keys() )

        for i in range(len(data[keys[0]])):

            char = data['characters'][i]
            char_desc = self.bot.resource_manager.get_character_full_details(char['name'])
            if char_desc is not None:
                char_desc = char_desc.get('description', 'N/A')
            wep = data['weapons'][i]
            arti = data['artifacts'][i]

            char_embed = Embed(title=f"Basic Stats", description=char_desc, color=char['embed_color'])
            char_embed.set_author(name=char['name'], icon_url=char['thumb'])
            char_embed.set_thumbnail(url=char['thumb'])
            
            for k in char:
                if k not in ['thumb','embed_color','name']:
                    char_embed.add_field(name=k.title(), value=char[k], inline=True)
            
            char_embed.set_footer(text=f"{char['name']} - Basic Stats")
            embeds['characters'].append(char_embed)

            wep_embed = Embed(title=f"{wep['name']} - Basic Stats", description=wep['description'], color=char['embed_color'])
            wep_embed.set_author(name=char['name'], icon_url=char['thumb'])
            wep_embed.set_thumbnail(url=wep['thumb'])
            
            wep_embed.add_field(name='Equipped on', value=char['name'])
            for k in wep:
                if k not in ['name', 'thumb', 'description']:
                    wep_embed.add_field(name=k.title(), value=wep[k], inline=True)
            
            wep_embed.set_footer(text=f"{char['name']} - {wep['name']} Basic Stats")
            embeds['weapons'].append(wep_embed)

            arti_embed = Embed(title=f"Artifact Stats", description=char_desc +"\n *equipped on {char['name']}*" , color=char['embed_color'])
            for art in arti:
                name = art
                
                piece_bonus = 'No'
                if 2 <= len(arti[art]['pieces']) < 4:
                    piece_bonus = 2
                elif len(arti[art]['pieces']) > 3:
                    piece_bonus = 4
                desc_ = f"{piece_bonus} piece bonus\n **Description**: *{arti[art]['bonus']}*\n```css\n"
                for a in arti[art]['pieces']:
                    desc_ += f" {'⭐' * a['rarity']} {a['piece']} lvl. {a['level']}\n"
                desc_ += "\n```"

                arti_embed.add_field(name=name, value=desc_)


            arti_embed.set_author(name=char['name'], icon_url=char['thumb'])
            arti_embed.set_thumbnail(url=char['thumb'])
            
      
            
            arti_embed.set_footer(text=f"{char['name']} - Artifact Stats")
            embeds['artifacts'].append(arti_embed)

            chars = self.calculator.get_char_stats(char['name'].replace('"','',99), char['level'], char['rarity'])
            print(wep['name'])
            weps = self.calculator.get_weapon_stats(wep['name'].replace('"','',99).replace("'","",99), wep['level'], wep['ascension'])
            
            total = self.calculator.sum_stats(chars, weps)

            desc_ = f'\n*Character Stat!*\n```css\n'
            for char_ in chars:
                desc_ += f"{char_.replace('_',' ',99).upper()}: {chars[char_]}\n"
            desc_+= f"\n```\n*Weapon {wep['name']} Stats*\n```css\n"
            for wep in weps:
                desc_ += f"{wep.replace('_',' ',99).upper()}: {weps[wep]}\n"
            desc_ += f"\n```\n"
            sembed = Embed(title=f"Probable Stats without Artifacts", description=f"{char_desc} {desc_}", color=char['embed_color'])
            total_desc = '```css\n'
            for t in total:
                total_desc += f"{t.replace('_',' ',99).upper()}: {total[t]}\n"
            total_desc += "\n```\n"

            sembed.add_field(name='Stats Sum!', value=total_desc)
            sembed.set_author(name=char['name'], icon_url=char['thumb'])
            sembed.set_thumbnail(url=char['thumb'])
            embeds['stats'].append(sembed)

        if len(embeds['characters']) > 0:
            return embeds

            









