import requests
import json
import time


import os

from os import getcwd,mkdir
from os.path import exists

from datetime import date, datetime

import re 
from urllib.parse import unquote
from canvas import BannerCanvas

from genshinstats import get_uid_from_authkey

sample_url = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1&sign_type=2&lang=en&authkey={authkey}&gacha_type={bannercode}&page={page}&size={size}&end_id={end}'
sample_input_url = 'https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?im_out=true&sign_type=2&auth_appid=im_ccs&authkey_ver=1&win_direction=portrait&lang=en&device_type=pc&ext=%7b%22loc%22%3a%7b%22x%22%3a336.237060546875%2c%22y%22%3a397.2837219238281%2c%22z%22%3a799.7633666992188%7d%2c%22platform%22%3a%22WinST%22%7d&game_version=OSRELWin2.2.0_R4547778_S4586310_D4595093&plat_type=pc&authkey=QMo%2fcQC%2fjcYRiR%2fy%2bEprx%2fyU3p%2bsKc5s1m83CGMmKuvb43kgnLwWbB%2b7pEDHLgBngO942G4CyUk4gCy4kkRGeC24DyiRtvrEH2omOAmCG58jqNwCyX068M%2bO6CEackc8ozvG9J%2b5wQCYydTm80Jz85HOyg9rIaKN7bnsPkfUu00%2fN3d2PRk2s2r8nmzsePKoqwp%2bIoQp5gm1m9aW8KYYPiRPtYYw%2fvSLAjhsqJVB77f8pEyT90ntBDx1QYp6TK9QKOS9xSFKr8azwMg5IkNRCun52ZuEf5A20kC0pIAOr3ZyTZ8xBVTG4l4MfBX0zFpHRksXKG8lpwWOQ48u4dMV3nlS6PWr2eB7FgPwIu%2blfVjlLiiyNHUiBMFCaHmu%2fL8hBFCEACNpm7WJIS6SlRkW6ivHoIuGqEpIroiBHl6JnUZY8uYdkg6Yt74RYodHZZ7je5PADyIqIlMEmdQhlVhflvzRxyZTqb5mT8Bdh%2bsh8ySJFo6EkdiBSJB14lMbKPBZor9P6dMClPJBGfWybqKJQWublRKHJqk1976T4IIufkaVyEzZSGybz5FFq6xcYnvuXqKOCqsPGRpE%2fnIukXU6JaV5Vn2qa9sYsYb8fdNHRsn8Ce2hDohcVAEU5Wh4RqHhAt903nFeY4ogkQ3QEv%2fMEorC9BujRJsnf8RtPeP6%2bQqYbV0FzFFExC8gcTWH0cdPPvCiCVv60DLdX2NLaKIxlaFp7PVzrTVQD2CUXmGANMYgYE9oUncuJ9JKYTRCXf5egxMtzR4J%2bWVnRW%2fR5cUsRQchpJMNiaEw1pfCp6HoR1LUyRV2HRLn4hxlq4CiqfbIthBfn5C%2bTmSVkbTR9NqAxf8TGvuj%2fBVyD3hsngGy6CYkM2Ot143%2fL4TZACnY%2bUGUvP0AC%2b%2f3HO3DDh7azH8xgenkJhZeAxcINqlEeA0QW9NzO1VUQIN5dDdZnwjZugtGvIl9lz8exXY5IO5X3RlphbQL8NS%2bUVUyltAk9xKt2vCByc%2fAeGL41WNF0hV0w%2bFZpOHvHMZFpTOrqYdppwcy15VXKqRcb4Z0FwDtzLBVQS%2fnLGZiyLdIqHQSnCE%2fC41eXCqUR4Me3OsUO8P4hjUuK76jd6zRZ0mCRnmNNMHv%2fouysFl7JzoX9oPjLKcPidKVU1XpCe6Y6S5wZoAlnyzdGfw2Ivg2YBRrDmG%2bowgMODLX%2beYvads10iPp8vHAoH18TspZw4Mut4aNYm9iL7lgDL0gbWgZmIDaB1kFh6CaGyynvVVoovgjITZUDT%2fC20VIa2%2fSZGt%2b4bj7kUmj1EGcsQu%2brHfwjruqrS8bxxWZbcWtUWoBgUU%2fIrF13ulbXRbTTjgy0Q1iHkb1%2bFt4%2fll%2f%2fw%3d%3d&game_biz=hk4e_global'

class GenshinGacha:
    def __init__(self):
        self.url = ''
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        self.url = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog'  
        self.path = getcwd()+f'/assets/wishes/'
        pass
    
    def create_folder(self, uid:int):        
        if not exists(f'{self.path}/uids/{uid}'):
            mkdir(f'{self.path}/uids/{uid}')


    def generate_key(self,str_ :str):  
        '''
        generates a easily accessible dictionary key for user
        '''
        str_ = str_.lower()  
        keys = [';',':',"'",'-','\\','.',',','/','!',' ']
        for i in keys:
            str_ = str_.replace(i,'_',99)
        str_ = str_.replace('_s_','s_',9)
        return str_

    def get_region(self,uid: int):
        regions = {'8':'os_asia','7': 'os_euro'}
        uid_ = str(uid)
        print(uid_[:1])
        if uid_[:1] in regions:
            return regions[uid_[:1]]   


    def get_history(self, authkey: str,bannercode : str,page: str,size: str,end: str, uid: str):
        '''
        get wish history
        authkey - > str
        bannercode -> 301, 302, 200, 100
        page - > 1 for first
        size -> 6 or 20
        end -> 0 for first or id of last wish in previous page
        '''        
        params = {
            'authkey_ver': '1',
            'lang': 'en-us',
            'authkey': str(authkey),
            'gacha_type' : str(bannercode),        
            'page': str(page),
            'end_id': str(end),
            'size': str(size),
            'region': self.get_region(uid)
        }
        headers = {
            'user-agent': self.USER_AGENT,
            'Content-Type': 'application/json',
            'cookie': 'ltuid=6457775;ltoken=tJLdlousrYagG8jky6vKNJpKWnqS8joxuby1D3mS;'        
        } 
        session = requests.get(self.url,params=params,headers=headers)
        if session.status_code != 404:
            data = session.json()
            if data['retcode'] == 0:
                if data['message'] == 'OK':
                    return data
                else:
                    raise Exception(data['message'])
            else:
                raise Exception(f"retcode {data['retcode']} - message {data['message']}")
        else:
            raise Exception('error code 404')


    def load_banners(self):
        '''
        load all banners
        '''
        if os.path.exists(f'{self.path}/assests/banners.json'):
            with open(f'{self.path}/assests/banners.json','r') as f:
                return json.load(f)

    def load_weapons(self):
        '''
        load all weapons
        '''
        if os.path.exists(f'{self.path}/assests/weapons_wish.json'):
            with open(f'{self.path}/assests/weapons_wish.json','r') as f:
                return json.load(f)

    def load_characters(self):
        '''
        load all characters
        '''
        
        if os.path.exists(f'{self.path}/assests/characters_wish.json'):
            with open(f'{self.path}/assests/characters_wish.json','r') as f:
                return json.load(f)




    def get_banners(self,all_banners: dict,pull_time: str, banner_code: str):
        """
        to do: pull time compare and bannercode
        return: list of banners    
        
            #wishes / pull time format
            #2021-03-02 18:48:40
            #%Y-%M-%d %H:%M:%S 
        """    
        pull_datetime = datetime.strptime(pull_time,'%Y-%m-%d %H:%M:%S')
        found_banners = []
        if banner_code == '200':
            found_banners.append(all_banners[banner_code][0])
        else:
            if banner_code == '100':
                found_banners.append(all_banners[banner_code][0])
            else:
                banner_codes_allowed = ['301','302']
                if banner_code in all_banners:
                    if banner_code in banner_codes_allowed:
                        for i in all_banners[banner_code]:
                            start_time = datetime.strptime(i['start'],'%Y-%m-%d %H:%M:%S')
                            end_time = datetime.strptime(i['end'],'%Y-%m-%d %H:%M:%S')
                            if start_time < pull_datetime < end_time:
                                found_banners.append(i)
        return found_banners

    def array_diff(self,array1:list ,array2: list):
        '''
        returns new items in a array

        array1 - array2 returns new items thats not common in both
        '''
        result = []
        for dict_ in array2:
            if dict_ in array1:
                pass
            else:
                result.append(dict_)        
        return result

    def extract_authkey(self,string: str):
        """Extracts an authkey from the provided string. Returns None if not found."""
        match = re.search(r'https://.+?authkey=([^&#]+)', string, re.MULTILINE)
        if match is not None:
            return unquote(match.group(1))
        return None

    def fetch_wishhistory(self,authkey : str,uid:int=-1):
        '''
        fetches all banner wish histories from api
        and stores it in wishhistory.json

        returns:
         uid
        '''
        banner_code = [301,302,100,200]
        if authkey.startswith('https://'):
            authkey_ = self.extract_authkey(authkey)
        else:
            authkey_ = authkey
        print(f'found authkey - {authkey_}')
        save_data = {}
        if uid == -1:
            uid = get_uid_from_authkey(authkey_)
        self.create_folder(uid)
        for i in banner_code:
            banner = str(i)
            page = 1
            end = 0
            save_ = {} 
            fetch = True        
            while fetch == True:                  
                full_data = self.get_history(authkey_,banner,page,20,end,str(uid))            
                #print(full_data)
                if full_data is not None:
                    if full_data['message'] == 'OK':
                        if 'data' in full_data:
                            data = full_data['data']
                            if banner not in save_data:                    
                                save_data[banner] = {'total':0,'list':[]}                                    
                            save_data[banner]['total'] += int(data['size'])                                              
                            if 'list' in data:                              
                                if len(data['list']) > 1:
                                    if type(data['list']) == list:
                                        if type(save_data[banner]['list']) == list:
                                            save_data[banner]['list'] += data['list']                                       
                                    end = data['list'][-1]['id']
                                    page += 1
                                else:
                                    fetch = False
                            else:
                                fetch = False
                            time.sleep(5)

                            
                        else:
                            fetch = False
                else:
                    raise Exception('Data could not be fetched!')
        '''
        checks if local wish history exists
        '''
        data = {}
        temp_data = {}
        if exists(f'{self.path}/uids/{uid}/wishhistory-{uid}.json'):
            with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','r') as f:
                temp_data = json.load(f)
        if len(temp_data) != 0:
            for i in banner_code:
                banner = str(i)
                previous_array = temp_data[banner]['list']
                new_array = save_data[banner]['list']
                new_items = self.array_diff(previous_array,new_array)
                with open(f'{self.path}/uids/{uid}/newitems_{banner}.json','w') as f:
                    json.dump(new_items,f)
                data[banner] = {'total': len(previous_array)+ len(new_items), 'list': previous_array + new_items}
        else:
            data = save_data
        with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','w') as f:
                json.dump(data,f,indent=1)
        return uid






    def get_banner_featured(self,banner_dict: dict):
        '''
        gets banner featured 3,4,5 stars from banner dict
        '''
        five_star = []
        four_star = []
        three_star = []
        if 'featured' in banner_dict:
            for featured_item in banner_dict['featured']:
                if featured_item['rank'] == "5":
                    five_star.append({'id': featured_item['id'], 'type': featured_item['type']})
                else:
                    if featured_item['rank'] == "4":
                        four_star.append({'id': featured_item['id'], 'type': featured_item['type']})
                    else:                    
                        three_star.append({'id': featured_item['id'], 'type': featured_item['type']})
        return {'threestar': three_star, 'fourstar': four_star, 'fivestar': five_star}

    def get_banner_weapons(self,banner_dict: dict):
        '''
        gets banner weapons from banner dict
        '''
        weapons = []
        if 'weapons' in banner_dict:
            for weapon_item in banner_dict['weapons']:
                weapons.append({'id': weapon_item['id'],'rank': weapon_item['rank']})
        return weapons

    def get_banner_characters(self,banner_dict: dict):
        '''
        gets banner characters  from banner dict
        '''
        characters = []
        if 'characters' in banner_dict:
            for character_item in banner_dict['characters']:
                characters.append({'id': character_item['id'],'rank': character_item['rank']})
        return characters        


    def banner_in_wishes(self,wishes_list : list, id_: str, start :str, end: str):
        '''
        It is used to return index of banner objects generated during sorting pulls according to banners
        '''
        for i in wishes_list:
            if i['id'] == id_: 
                if i['start'] == start:
                    if i['end'] == end:
                        return wishes_list.index(i)


    def pull_in_banner(self,pulls_list : list, id_: str, rank: str):
        '''
        It is used to return index of pull objects generated during adding pulls to banner
        '''
        for i in pulls_list:
            if i['id'] == id_: 
                if i['rank'] == rank:                
                    return pulls_list.index(i)

    def if_fivestars_in_banner(self,banner_dict: dict):
        '''
        check for featured 5 stars in banner_dict
        '''

        featured = self.get_banner_featured(banner_dict)
        items = self.get_banner_characters(banner_dict) + self.get_banner_weapons(banner_dict) + featured['fivestar']
        check = False
        check_list = []
        if items:
            check_list = [i['rank'] for i in items]
            if '5' in check_list:
                check = True
        return check

    def chance_for_fivestar(self,banner_object: dict, pity: int):
        '''
        calculates chance for 5 star for 5 star pity provided
        '''
        ratesfivestar = {'75': '0.6%','89':'32.4%','90':'100%'}
        if self.if_fivestars_in_banner(banner_object):
            for pity_check in ratesfivestar:            
                if pity <= int(pity_check):                
                    return ratesfivestar[pity_check]
                                        
    def rank_pity_dict(self,five_starpity: int, four_starpity: int):
        '''
        generates pity dict for ranks 5star and 4star
        '''
        return {'5starpity': five_starpity,'4starpity': four_starpity}


    def correct_pity(self,banner_dict: dict, last_banner_dict: dict, pity: int):
        '''
        checks if previous one was same banner and returns the corrected pity
        '''
        if last_banner_dict['banner_code'] == banner_dict['banner_code'] == '301' or last_banner_dict['banner_code'] == banner_dict['banner_code'] == '302':        
            return last_banner_dict['5starpity']
        else:
            return 0
    
    def chance_result_dict(self,rank: str,result: str, chance: str):
        '''
        generates dict containing chance and result of pull done
        '''
        return {f'{rank}starwishresut': result, f'chancefor{rank}star': chance}

    def calculate_primogems(self,pulls: int):
        '''
        calculates primogems for no of pulls done
        '''
        return pulls * 160
        
    def stage_for_5star(self,five_starpity: int, rateup: bool):
        '''
        returns stage for 5 star next pull HARD | SOFT | 5050
        '''
        rate_Text = ''
        if rateup == False:
            rate_Text = 'Your next pull is guaranteed for 5 star featured character!'
        else:
            if rateup == True:
                rate_Text = 'You are at 50/50 pull for 5 star featured character!'
        if five_starpity <= 74:
            return f'Hard Pity - Each next pull has 0.6% chance of being a 5 star item! {rate_Text}'
        elif five_starpity <= 89:
            return f'Soft Pity - Each next pull has 32.4% chance of being a 5 star item! {rate_Text}'
        elif five_starpity <= 89:
            return f'Guaranteed - Next pull should have 100% chance of being a 5 star item! {rate_Text}'

    def stage_for_4star(self,four_starpity: int):
        '''
        returns stage for 4 star next pull HARD | SOFT | 5050
        '''
        if four_starpity <= 5:
            return 'Soft Pity - Each next pull has 13% chance of being a 4 star item!'
        elif 6 <= four_starpity <= 10:
            return 'Guaranteed - Next pull should have 100% chance of being a 4 star item!'

    def if_featured(self,banner_dict : dict, id_: str):
        '''
        checks if an item pulled is featured for banner  [banner_dict]
        '''
        featured = banner_dict['featured5star'] 
        list_ = [i['id'] for i in featured]
        print(id_,list_)
        if (id_ in list_) in [False,True]:
            return id_ in list_
        return ''
    
    def rateup_previous(self,wishes: list):
        if len(wishes) > 1:
            return wishes[len(wishes)-1]['rateup']

    def calculate_pity(self,banner_object: dict, pull:dict, fivestarpity: int, fourstarpity: int):
        '''

        calculates 5 and 4 star pities for banner 

        '''
        

        pities = {'302': {'5star' : 90, '4star': 80},'301': {'5star': 90, '4star': 10}, '200': {'5star': 90, '4star': 10}, '100': {'5star': 90, '4star': 10} }
        result = 'lost'        
        if pull['rank_type'] == '5':                        
            result = 'won' 
            banner_object['5starpities'].append(fivestarpity)
            #print(banner_object['rateup']) 
            if banner_object['rateup'] == True:
                banner_object['5050items'].append(pull['name'])                                                                   
            banner_object['rateup'] = self.if_featured(banner_object,self.generate_key(pull['name']))                           
            fivestarpity = 1     
            banner_object['5staritems'].append(pull['name'])                              
        else:
            if fivestarpity < pities[str(banner_object['banner_code'])]['5star']:
                fivestarpity += 1
            else:
                fivestarpity = 1  
        if pull['rank_type'] == '4':
            banner_object['4staritems'].append(pull['name'])   
            banner_object['4starpities'].append(fourstarpity)  
            fourstarpity =  1
        else:                  
            if fourstarpity < pities[str(banner_object['banner_code'])]['4star']:
                fourstarpity += 1
            else:
                fourstarpity = 1      
        return fivestarpity,fourstarpity 
                       

    def process_wishes(self,uid: int):
        '''

        process wishes from wish history file
        sorts them according to banners and pities and primogems info etc

        '''
        banners = self.load_banners()
        data = {}
        self.create_folder(uid)
        with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','r') as f:
            data = json.load(f)
        wishes = []
        for banner_code in data:            
            fourstarpity = 0
            fivestarpity = 0
            fourstarstage = ''
            fivestarstage = ''
            totalpulls = 0
            if 'list' in data[banner_code]:
                list_pulls = data[banner_code]['list']               
                print(f'banner code {banner_code}')          
                for index in range(len(list_pulls)-1,-1,-1):            
                    pull = list_pulls[index]                             
                    foundBanners = self.get_banners(banners,pull['time'],banner_code)   
                    '''
                    if banner_code in ['301','302']:                 
                    names = [(i['start'],pull['time'],i['end'], (len(foundBanners) == 1)) for i in foundBanners]     
                    print(names)
                    '''
                    one_banner = (len(foundBanners) == 1)
                    #print(f'found one banner {one_banner}')
                    if one_banner:       #checks if only one banner is found
                        index_in_wishes = self.banner_in_wishes(wishes,self.generate_key(foundBanners[0]['name']),foundBanners[0]['start'],foundBanners[0]['end'])
                        #print(f'index in wishes list {index_in_wishes}')
                        '''
                        check if a banner object already exists in wishes[list] and
                        if present
                            returns its index.
                        else
                            creates a banner object
                        '''                
                        if index_in_wishes == None:  
                            if len(wishes) > 1:                    
                                lastbanner = wishes[len(wishes)-1]
                                fivestarpity = self.correct_pity(banner_object,lastbanner,fivestarpity)                        
                            #print(f'new banner')
                            featuredItems = self.get_banner_featured(foundBanners[0])
                            weaponItems = self.get_banner_weapons(foundBanners[0])
                            characterItems = self.get_banner_characters(foundBanners[0])
                            '''
                            Pity calculation only if banner is character_event -> 301                
                            '''                   
                            banner_object = {
                                'id': self.generate_key(foundBanners[0]['name']),
                                'name': foundBanners[0]['name'],
                                'start': foundBanners[0]['start'],
                                'end': foundBanners[0]['end'],
                                'banner_code': banner_code,
                                'featured5star': featuredItems['fivestar'],
                                'featured4star': featuredItems['fourstar'],
                                'featured3star': featuredItems['threestar'],
                                'weapons': weaponItems,
                                'characters': characterItems,
                                'pulls' : [],
                                'totalpulls': 0,
                                '5starpity': fivestarpity,
                                '4starpity': fourstarpity,
                                '5starstage': '', 
                                '4starstage': '',
                                '4starchance': '',
                                '5starpities': [], #at which pities 5 star was pulled
                                '4starpities': [], #at which pities 4 star was pulled
                                '5staritems': [],
                                '4staritems': [],
                                '5050items': [],
                                'rateup': self.rateup_previous(wishes)                   #true if 50/50, false if 100              
                                }  
                            #print(f'banner {banner_object}')
                            wishes.append(banner_object)   
                        else:
                            print(f'same banner')
                        if index_in_wishes == None:
                            index_in_wishes = self.banner_in_wishes(wishes,self.generate_key(foundBanners[0]['name']),foundBanners[0]['start'],foundBanners[0]['end'])   
                        else:
                            banner_object = wishes[index_in_wishes]             
                        '''
                        Pity calculation for events            
                        '''                        
                    #print(f'pities [5star {fivestarpity} | 4star {fourstarpity}]')                    
                        chanceforfivestar = self.chance_for_fivestar(banner_object,fivestarpity)
                        fivestarpity, fourstarpity = self.calculate_pity(banner_object,pull,fivestarpity,fourstarpity)
                        banner_object['5starpity'] = fivestarpity
                        banner_object['4starpity'] = fourstarpity
                        '''

                        todo: pull and pity stuff here

                        '''
                        if banner_object:
                            '''
                            pity stuff here
                            '''
                            pity_ = self.rank_pity_dict(fivestarpity,fourstarpity)
                            chance_ = {}
                            if pull['rank_type'] == '5':
                                chance_ = self.chance_result_dict(pull['rank_type'],'won',chanceforfivestar)
                            #print(pity_) 
                            pull_object = dict({
                                'id': self.generate_key(pull['name']),
                                'type': pull['item_type'],
                                'time': pull['time'],
                                'rank': pull['rank_type']                                           
                                },**pity_,** chance_)    
                                              
                            banner_object['chancefor5star'] = chanceforfivestar               
                            banner_object['pulls'].append(pull_object)
                            banner_object['totalpulls'] += 1
                            #print(stage_for_5star(fivestarpity, banner_object['rateup']))
                            banner_object['5starstage'] = self.stage_for_5star(fivestarpity, banner_object['rateup'])
                            #print(stage_for_4star(fourstarpity))
                            banner_object['4starstage'] = self.stage_for_4star(fourstarpity)
                            banner_object['primogems'] = self.calculate_primogems(banner_object['totalpulls'])

        #return wishes        

        '''
        for checking just if its working as intended
        '''
        self.create_folder(uid)
        with open(f'{self.path}/uids/{uid}/wishes-{uid}.json','w') as f:
            json.dump({'data':wishes},f,indent=1)

    def fetch_statistics(self,uid: int,banner_code : str):
        '''
        call this after processing wishes

        generates stats for each type of banner

        '''
        data = {}
        if exists(f'{self.path}/uids/{uid}/wishes-{uid}.json'):
            with open(f'{self.path}/uids/{uid}/wishes-{uid}.json','r') as f:
                data = json.load(f)       
            wishes = data['data']
            stats = {'5starpity':0,'4starpity':0,'5staritems':[],'4staritems':[],'5050items':[],'5050pulls': [],'5starpities':[],'4starpities': [],'chancefor5star':'','totalpulls': 0,'primogems':0,'pulls': {}}
            for i in wishes:
                if banner_code == i['banner_code']:
                    dict_ = i  
                    pulls_ = stats['pulls']             
                    dict_['pulls'] = dict_['pulls']
                    pulls_[dict_['id']] = dict_['pulls']
                    stats['5staritems'] += dict_['5staritems']
                    stats['4staritems'] += dict_['4staritems']  
                    stats['5050items'] += dict_['5050items']  
                    stats['5starpities'] += dict_['5starpities']  
                    stats['4starpities'] += dict_['4starpities'] 
                    stats['chancefor5star'] = dict_['chancefor5star']     
                    stats['5starstage'] = dict_['5starstage'] 
                    stats['4starstage'] = dict_['4starstage'] 
                    stats['totalpulls'] += dict_['totalpulls']    
                    stats['5050pulls'].append(dict_['rateup'])
                    stats['primogems'] += dict_['primogems']
                    stats['pulls'] = pulls_
                    stats['5starpity'] = dict_['5starpity']
                    stats['4starpity'] = dict_['4starpity']

            return stats
                
    def create_canvas_image(self, uid: int):
        '''

        creates canvas image

        '''
        banners = [301,200,302,100]           
        for banner in banners:
            canvas = BannerCanvas(uid) 
            stat = self.fetch_statistics(uid,str(banner))
            canvas.set_heading(str(banner))
            canvas.add_pity('5',stat['5starpity'])
            canvas.add_pity('4',stat['4starpity'])                         
            canvas.add_field('Total Pulls',stat['totalpulls'])
            canvas.add_field('Primogems',stat['primogems'])

            fivestars = zip(stat['5starpities'],stat['5staritems'])
            for item in fivestars:
                canvas.add_item('5',item[1],item[0])
            fourstars = zip(stat['4starpities'],stat['4staritems'])
            for item in fourstars:
                canvas.add_item('4',item[1],item[0])
            
            
            if len(stat['5050pulls']) > 1:
                if stat['5050pulls'][-1] == True:
                    canvas.add_field('At 50/50 Pull','Yes')
                else:
                    canvas.add_field('At 50/50 Pull','No')
            canvas.add_field('50/50s won',len(stat['5050items']))         
            canvas.save_pic(uid,banner)

'''
example 

Gacha = GenshinGacha()
authkey = Gacha.extract_authkey('feedback_url')
uid = Gacha.fetch_wishhistory(authkey, *optional uid*)
Gacha.process_wishes(uid)
Gacha.create_canvas_image(uid)
'''