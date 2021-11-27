import requests
import json
from asyncio import sleep
from nextcord import Message, Member, Embed, File

import os

from os import getcwd,mkdir,listdir
from os.path import exists,join,isfile

from datetime import date, datetime

import re 
from urllib.parse import unquote
from base.canvas import BannerCanvas

from genshinstats import get_uid_from_authkey


sample_url = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1&sign_type=2&lang=en&authkey={authkey}&gacha_type={bannercode}&page={page}&size={size}&end_id={end}'
sample_input_url = 'https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?im_out=true&sign_type=2&auth_appid=im_ccs&authkey_ver=1&win_direction=portrait&lang=en&device_type=pc&ext=%7b%22loc%22%3a%7b%22x%22%3a336.237060546875%2c%22y%22%3a397.2837219238281%2c%22z%22%3a799.7633666992188%7d%2c%22platform%22%3a%22WinST%22%7d&game_version=OSRELWin2.2.0_R4547778_S4586310_D4595093&plat_type=pc&authkey=QMo%2fcQC%2fjcYRiR%2fy%2bEprx%2fyU3p%2bsKc5s1m83CGMmKuvb43kgnLwWbB%2b7pEDHLgBngO942G4CyUk4gCy4kkRGeC24DyiRtvrEH2omOAmCG58jqNwCyX068M%2bO6CEackc8ozvG9J%2b5wQCYydTm80Jz85HOyg9rIaKN7bnsPkfUu00%2fN3d2PRk2s2r8nmzsePKoqwp%2bIoQp5gm1m9aW8KYYPiRPtYYw%2fvSLAjhsqJVB77f8pEyT90ntBDx1QYp6TK9QKOS9xSFKr8azwMg5IkNRCun52ZuEf5A20kC0pIAOr3ZyTZ8xBVTG4l4MfBX0zFpHRksXKG8lpwWOQ48u4dMV3nlS6PWr2eB7FgPwIu%2blfVjlLiiyNHUiBMFCaHmu%2fL8hBFCEACNpm7WJIS6SlRkW6ivHoIuGqEpIroiBHl6JnUZY8uYdkg6Yt74RYodHZZ7je5PADyIqIlMEmdQhlVhflvzRxyZTqb5mT8Bdh%2bsh8ySJFo6EkdiBSJB14lMbKPBZor9P6dMClPJBGfWybqKJQWublRKHJqk1976T4IIufkaVyEzZSGybz5FFq6xcYnvuXqKOCqsPGRpE%2fnIukXU6JaV5Vn2qa9sYsYb8fdNHRsn8Ce2hDohcVAEU5Wh4RqHhAt903nFeY4ogkQ3QEv%2fMEorC9BujRJsnf8RtPeP6%2bQqYbV0FzFFExC8gcTWH0cdPPvCiCVv60DLdX2NLaKIxlaFp7PVzrTVQD2CUXmGANMYgYE9oUncuJ9JKYTRCXf5egxMtzR4J%2bWVnRW%2fR5cUsRQchpJMNiaEw1pfCp6HoR1LUyRV2HRLn4hxlq4CiqfbIthBfn5C%2bTmSVkbTR9NqAxf8TGvuj%2fBVyD3hsngGy6CYkM2Ot143%2fL4TZACnY%2bUGUvP0AC%2b%2f3HO3DDh7azH8xgenkJhZeAxcINqlEeA0QW9NzO1VUQIN5dDdZnwjZugtGvIl9lz8exXY5IO5X3RlphbQL8NS%2bUVUyltAk9xKt2vCByc%2fAeGL41WNF0hV0w%2bFZpOHvHMZFpTOrqYdppwcy15VXKqRcb4Z0FwDtzLBVQS%2fnLGZiyLdIqHQSnCE%2fC41eXCqUR4Me3OsUO8P4hjUuK76jd6zRZ0mCRnmNNMHv%2fouysFl7JzoX9oPjLKcPidKVU1XpCe6Y6S5wZoAlnyzdGfw2Ivg2YBRrDmG%2bowgMODLX%2beYvads10iPp8vHAoH18TspZw4Mut4aNYm9iL7lgDL0gbWgZmIDaB1kFh6CaGyynvVVoovgjITZUDT%2fC20VIa2%2fSZGt%2b4bj7kUmj1EGcsQu%2brHfwjruqrS8bxxWZbcWtUWoBgUU%2fIrF13ulbXRbTTjgy0Q1iHkb1%2bFt4%2fll%2f%2fw%3d%3d&game_biz=hk4e_global'

class GenshinGacha:
    def __init__(self):
        self.url = ''
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Unity 3D; ZFBrowser 2.1.0; Genshin Impact 2.3.0_4786731_4861639) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
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

    #
    # depreciated stopped working as of 23 december, 2021
    #
    '''
    def get_history(self, authkey: str,bannercode : str,page: str,size: str,end: str):
        
        get wish history
        authkey - > str
        bannercode -> 301, 302, 200, 100
        page - > 1 for first
        size -> 6 or 20
        end -> 0 for first or id of last wish in previous page
               
        params = {
            'authkey_ver': '1',
            'sign_type': '2',            
            'auth_appid': 'webview_gacha',
            'lang': 'en',                 
            'region': 'os_asia',      
            'init_type': '100',
            'authkey': str(authkey),            
            'game_biz': 'hk4e_global',
            'gacha_type' : str(bannercode),        
            'page': str(page),            
            'size': str(size),
            'end_id': str(end),

        }
        
        session = requests.get(self.url,params=params,headers=headers)
        print(session.headers)
        if session.status_code != 404:
            data = session.json()
            print(data)
            if data['retcode'] == 0:
                if data['message'] == 'OK':
                    return data
        return None
    '''
    def get_history(self, link, gacha_type: str,page : str, size: str, end : str):
        headers = {
            'user-agent': self.USER_AGENT,
            'Content-Type': 'application/json',    
        } 
        session = requests.get(link.format(gachatype=gacha_type,page=page,size=size,end=end),headers=headers)
        if session.status_code != 404:
            data = session.json()
            if data['retcode'] == 0:
                if data['message'] == 'OK':
                    return data
        return None

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
                banner_codes_allowed = ['301','302','400']
                if banner_code in all_banners:
                    if banner_code in banner_codes_allowed:
                        for i in all_banners[banner_code]:
                            start_time = datetime.strptime(i['start'],'%Y-%m-%d %H:%M:%S')
                            end_time = datetime.strptime(i['end'],'%Y-%m-%d %H:%M:%S')
                            if start_time < pull_datetime < end_time:
                                found_banners.append(i)
        return found_banners

    def filter_second_character_banner_wishes(self, data: dict):
        changed_data = data
        check = ('301' in data)
        banner_400 = []
        if check:
            for pull in data['301']['list']:
                if pull['gacha_type'] == '400':
                    banner_400.append(pull)
            pulls_301 = data['301']['list']
            changed_301 = []
            for pull in pulls_301:
                if pull not in banner_400:
                    changed_301.append(pull)
            changed_data['100'] = data['100']
            changed_data['200'] = data['200']
            changed_data['302'] = data['302']
            changed_data['301'] = {'total' : len(changed_301), 'list': changed_301}
            previous = []
            if '400' in changed_data:
                previous = changed_data['400']['list']
            changed_data['400'] = {'total' : len(banner_400) + len(previous), 'list' : banner_400 + previous}
            return changed_data




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

    def create_link_from_outputfile(self,output_file_link: str):
        '''
        creates link from uploaded output file link
        '''
        data = requests.get(output_file_link).content.decode('utf-8')
        lines = data.splitlines()
        urls = []
        for line in lines:
            if line.startswith('OnGetWebViewPageFinish:'):
                urls.append(line[line.find('OnGetWebViewPageFinish:')+len('OnGetWebViewPageFinish:'):])
        if urls[-1].startswith('https://webstatic-sea.mihoyo.com'):
            params = urls[-1][urls[-1].find('index.html')+len('index.html'):].replace('#/log','',1)
            link = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog{params}&gacha_type={gachatype}&page={page}&size={size}&end_id={end}'
            return link.replace('{params}',params,1)
        return ''

    def create_link_from_link(self,output_link: str):
        '''
        creates api link from a wish history link
        '''
        output_link = output_link[output_link.find('https://webstatic-sea.mihoyo.com'):]
        params = output_link[output_link.find('index.html')+len('index.html'):output_link.find('#/log')]
        link = 'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog{params}&gacha_type={gachatype}&page={page}&size={size}&end_id={end}'
        return link.replace('{params}',params,1)
        

    def get_uid_from_history(self, link:str):
        '''

        gets uid from wish history

        '''
        banners = [301,302,200,100]
        for banner in banners:
            r = requests.get(link.format(gachatype=banner,page=1,size=6,end=0)).json()
            if r['message'] == 'OK':
                if 'list' in r['data']:
                    if bool(r['data']['list']):
                        uid = r['data']['list'][0]['uid']
                        return uid

    def check_output_file(self, output_file_link: str):
        print(output_file_link.split('/')[-1])
        checker = ('output_log' in output_file_link.split('/')[-1])
        return checker




    def fetch_wishhistory(self, output_file_link: str, uid: int=-1):
        '''
        fetches all banner wish histories from api
        and stores it in wishhistory.json

        returns:
         uid
         and dict showing which banner had new items pulled
        '''
        new_items_banner = {}
        banner_code = [301,302,100,200,400]
        '''
        if authkey.startswith('https://'):
            authkey_ = self.extract_authkey(authkey)
        else:
            authkey_ = authkey
        print(f'found authkey - {authkey_}')        
        
        if uid == -1:
            uid = get_uid_from_authkey(authkey_)
        '''
        print(self.check_output_file(output_file_link))
        if self.check_output_file(output_file_link):
            link = self.create_link_from_outputfile(output_file_link)
            print(link)
        else:
            link = self.create_link_from_link(output_file_link)
            print(link)   
            if '{params}' in link:
                link = ''         
        if link == '':
            return None
        uid = self.get_uid_from_history(link)
        if uid is not None:            
            self.create_folder(uid)
        else:
            return None
        save_data = {}
        for i in banner_code:
            banner = str(i)
            page = 1
            end = 0
            save_ = {} 
            fetch = True        
            while fetch == True:                  
                full_data = self.get_history(link,str(i),str(page),'20',end)       
                #print(full_data)
                print(i)
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
                        else:
                            fetch = False
                else:
                    return None,None
        '''
        checks if local wish history exists
        '''
        data = {}
        temp_data = {}
        if exists(f'{self.path}/uids/{uid}/wishhistory-{uid}.json'):
            with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','r') as f:
                temp_data = json.load(f)
        new_items_banner = {}
        if len(temp_data) != 0:
            for i in banner_code:
                banner = str(i)
                if banner in temp_data:
                    previous_array = temp_data[banner]['list']
                    new_array = save_data[banner]['list']
                    new_items = self.array_diff(previous_array,new_array) 
                    new_items_banner[banner] = (len(new_items) !=0)
                    with open(f'{self.path}/uids/{uid}/newitems_{banner}.json','w') as f:
                        json.dump(new_items,f)
                    data[banner] = {'total': len(previous_array)+ len(new_items), 'list': previous_array + new_items}
                else:
                    if banner in save_data:
                        new_items = save_data[banner]['list']
                        data[banner] = {'total': len(new_items), 'list': new_items}
                        new_items_banner[banner] = (len(new_items) !=0)
        else:
            data = save_data
            for i in banner_code:
                new_items_banner[i] = True
        with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','w') as f:
                json.dump(data,f,indent=1)
        return uid,new_items_banner






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


    def correct_pity(self,banner_dict: dict, last_banner_dict: dict):
        '''
        checks if previous one was same banner and returns the corrected pity
        '''
        if last_banner_dict['banner_code'] in ['301','400']:
            if banner_dict['banner_code'] in ['301','400']:
                return last_banner_dict['5starpity']          
        
        if last_banner_dict['banner_code'] == banner_dict['banner_code'] == '302':        
            return last_banner_dict['5starpity']
        
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
        

        pities = {'302': {'5star' : 90, '4star': 8},'400': {'5star': 90, '4star': 10},'301': {'5star': 90, '4star': 10}, '200': {'5star': 90, '4star': 10}, '100': {'5star': 90, '4star': 10} }
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
                       

    def process_wishes(self,uid: int, banner_code: str):
        '''

        process wishes from wish history file
        sorts them according to banners and pities and primogems info etc

        '''
        banners = self.load_banners()
        data = {}
        self.create_folder(uid)
        if exists(f'{self.path}/uids/{uid}/wishhistory-{uid}.json'):
            with open(f'{self.path}/uids/{uid}/wishhistory-{uid}.json','r') as f:
                data = json.load(f)
            wishes = []           
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
                    if banner_code != '301':                         
                        foundBanners = self.get_banners(banners,pull['time'],banner_code)   
                    else:
                        banner_code = pull['gacha_type']                        
                        foundBanners = self.get_banners(banners,pull['time'],banner_code)
                        if pull['gacha_type'] == '400':
                            print(foundBanners, pull['gacha_type'])  
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
                                fivestarpity = self.correct_pity(banner_object,lastbanner)                        
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
                            if pull['gacha_type'] == '400':
                                print(banner_object)
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
            if banner_code == '400':
                banner_code = '301'
            with open(f'{self.path}/uids/{uid}/wishes-{uid}-{banner_code}.json','w') as f:
                json.dump({'data':wishes},f,indent=1)
                return True
        return None

    
    def fetch_statistics(self,uid: int,banner_code : str):
        '''
        call this after processing wishes

        generates stats for each type of banner

        '''
        search_banner = ''
        if banner_code == '400':
            search_banner = '400'
            banner_code ='301'
        else:
            search_banner = banner_code

        data = {}
        if exists(f'{self.path}/uids/{uid}/wishes-{uid}-{banner_code}.json'):
            with open(f'{self.path}/uids/{uid}/wishes-{uid}-{banner_code}.json','r') as f:
                data = json.load(f)       
            wishes = data['data']
            stats = {'5starpity':0,'4starpity':0,'5staritems':[],'4staritems':[],'5050items':[],'5050pulls': [],'5starpities':[],'4starpities': [],'chancefor5star':'','totalpulls': 0,'primogems':0,'pulls': {}}
            for i in wishes:
                if search_banner == i['banner_code']:
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
                
    def create_canvas_image(self, uid: int, banner: str):
        '''

        creates canvas image

        '''  
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
        if banner not in ['100','200']:
            canvas.add_field('50/50s won',len(stat['5050items']))         
        canvas.save_pic(banner)

    def embed_status(self, author: Member, uid: str, status: str):
        embed = Embed(title=f'Wish history',
                            color=0xf5e0d0) 
        embed.set_author(name=author.display_name,icon_url=author.avatar.url)
        embed.add_field(name='UID', value=str(uid))
        embed.add_field(name='Status', value=status)
        return embed

    async def process_authkey(self, wishhistory_link: str, author: Member,message: Message, change_status: bool = False):
        '''
        single function to do all things
        '''
        
        uid,banner_new = self.fetch_wishhistory(wishhistory_link)
        if change_status:
            embed = self.embed_status(author,uid,'Fetching wish history')
            await message.edit(embed=embed)
        if uid is not None and banner_new is not None:
            if len(banner_new) !=0:
                for banner in banner_new:
                    if banner_new[banner] == True: # if new items found
                        processed = self.process_wishes(uid,str(banner))
                        if change_status:
                            embed = self.embed_status(author,uid,f'Processing Wishes for Banner Type {banner}!')
                            await message.edit(embed=embed)
                        if processed:
                            self.create_canvas_image(uid, str(banner))
                            if change_status:
                                embed = self.embed_status(author,uid,f'Generating Image for Banner Type {banner}!')
                                await message.edit(embed=embed)
                if change_status:
                    embed = self.embed_status(author,uid,f'All done!')
                    await message.edit(embed=embed) 
                    return True
        

    async def fetch_image(self, uid: str, banner_code: str):
        if exists(f'{self.path}/uids/{uid}/images/{uid}_{banner_code}.png'):
            return File(f'{self.path}/uids/{uid}/images/{uid}_{banner_code}.png',filename=f'{uid}_{banner_code}.png'), str(f'{uid}_{banner_code}.png')
        return None, None

    def resave_images(self):
        uids = listdir(f'{self.path}/uids/')
        for uid in uids:
            print(uid)
            if exists(f'{self.path}/uids/{uid}/'):
                files = [f'{self.path}/uids/{uid}/{file}' for file in listdir(f'{self.path}/uids/{uid}/') if isfile(f'{self.path}/uids/{uid}/{file}')]
                wishes_files = [file for file in files if 'wishes-' in file.split('/')[-1]]
                for wish in wishes_files:
                    banner_code = wish.split('/')[-1].split('-')[-1].split('.')[0]
                    self.create_canvas_image(uid,banner_code)
      
