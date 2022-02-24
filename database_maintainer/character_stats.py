from os import getcwd, mkdir
from os.path import exists
import requests
from bs4 import BeautifulSoup
from json import load, dump
from time import sleep


attacks = ['Normal Attack','Elemental Skill','Elemental Burst']


def load_characterdb():
    with open('characters.json','r') as f:
        return load(f)

character_data = load_characterdb()

def get_talent(character_name, talent_):
    character_ = character_name.split('_')[0]
    if character_ == 'feiyan':
        character_ = 'yanfei'
    if character_ == 'shougun':
        character_ = 'shogun'
    print(character_)
    for character in character_data:
        if character_.lower() in character.lower():
            talents = character_data[character].get('talents', None)
            if talents is not None:
                for talent in talents:
                    if talent_.lower() in talent['type'].lower():
                        return talent['name']


def fetch_character_lists():
    url = 'https://genshin.honeyhunterworld.com/db/char/characters/?lang=EN'
    r = requests.get(url).content

    bs = BeautifulSoup(r, 'lxml')
    lists = [f"https://genshin.honeyhunterworld.com{l.find('a').attrs['href']}" for l in bs.find_all('div', {'class': 'char_sea_cont'})]
    return lists

def get_skill_links(links, skill_name):
    for link in links:
        if len(link.attrs['href'].split('/')) >= 3:
            if link.attrs['href'].split('/')[2] == 'skill':
                if skill_name.lower() in link.text.lower():
                    return link.attrs['href']



def fetch_character_stats(url):
    test_url = url


    r = requests.get(test_url).content

    bs = BeautifulSoup(r, 'lxml')
    stat_dict = {}
    stat_table = bs.find('span',{'id':'scroll_stat'})
    if 'stat progression' in stat_table.text.lower():
        stat_table = stat_table.find_next_sibling()
        if stat_table is not None:
            stat_table = stat_table.find('table')

            keys = stat_table.find('tr')

            if keys is not None:
                keys = [key.text.strip().lower().replace('+','',99) for key in keys.find_all('td')[:-1]]
            
            items = stat_table.find_all('tr')[1:]

            if 'stat' not in stat_dict:
                stat_dict['stat'] = []
            for item in items:
                columns = item.find_all("td")[:-1]

                values = [value.text.strip().replace('%','',99) for value in columns]

                temp_dict = dict(zip(keys, values))

                stat_dict['stat'].append(temp_dict)

    talent_stats_link = {}

    links = bs.find_all('a')
    char = test_url.split('/')[-2]
    for attack in attacks:
        for link in links:
            name = get_talent(char, attack)
            print(name)
            u_ = get_skill_links(links, name)
            if u_ is not None:
                talent_stats_link[attack] = u_
    print(talent_stats_link)
    for link in talent_stats_link:
        stat_list = []
        key_ = link
        url = talent_stats_link[key_]
        r = requests.get(f'https://genshin.honeyhunterworld.com/{url}').content

        bs = BeautifulSoup(r, 'lxml')

        stat_table = bs.find('span',{'class':'item_secondary_title'})
        if 'talent progression' in stat_table.text.lower():
            stat_table = stat_table.find_next_sibling()
            if stat_table is not None:
                stat_table = stat_table.find('table')

                keys = stat_table.find('tr')

                if keys is not None:
                    keys = [key.text.strip().lower().replace('+','',99) for key in keys.find_all('td')[:-1]]
                keys[0] = 'title'
                items = stat_table.find_all('tr')

                for item in items:
                    columns = item.find_all("td")

                    values = [value.text.strip().replace('%','',99) for value in columns]

                    temp_dict = dict(zip(keys, values))

                    stat_list.append(temp_dict)
                talent_stats_link[key_] = stat_list     
    return stat_dict, talent_stats_link



def prettify_stats(data):    
    data = data['stat']
    new_dict = {}
    for dict_ in data:
        lv = dict_['lv'].replace('+','.5',1)
        keys = list(dict_.keys())
        keys.pop(0)       
        for key in keys:   
            if key.title() in new_dict:        
                new_dict[key.title()][lv] =  dict_[key]
            else:
                new_dict[key.title()] = {lv : dict_[key]}
            

    return new_dict


with open('kaeya_atk_stats.json','r') as f:
    data = load(f)


def check_if_charged(dict_, lvl):
    title = dict_['title'].split(' ')
    if 'charged' in title[0].lower():
        if title[-1] in ['DMG', 'Shot']:
            if f'lv{lvl}' in dict_:
                return 'DMG', lvl.replace("+", '.5',1), dict_[f'lv{lvl}']
        else:
            return 'Stamina Cost', lvl.replace("+", '.5',1), dict_[f'lv{lvl}']
    return None, None, None

def check_if_plunge(dict_, lvl):
    title = dict_['title'].split(' ')
    if 'plunge' in title[0].lower():
        if title[-1] == 'DMG':
            if f'lv{lvl}' in dict_:
                return 'DMG', lvl.replace("+", '.5',1), dict_[f'lv{lvl}']        
    return None, None, None


def check_if_normal(dict_, lvl):
    title = dict_['title']
    if title[0].isdigit():
        if 'hit' in title.lower():        
            if f'lv{lvl}' in dict_:
                return 'DMG', int(title[0]), dict_[f'lv{lvl}']        
    return None, None, None



def check_if_elemental(dict_, lvl):
    key = ''    
    key = dict_['title']    
    if f'lv{lvl}' in dict_:
        return key, lvl, dict_[f'lv{lvl}']   
    return None, None, None
    
    


def get_elemental_keys(key):
    title = key.split(' ')
    
    if 'element' in title[0].lower():
        return title[1].lower()


def prettify_atks(data):
    temp_dict = {}
    for attack in attacks:
        temp_data = {}
        if attack in data:
            if attack == 'Normal Attack':
                temp_dict['normal'] = {}
                temp_dict['charged'] = {}
                temp_dict['plunge'] = {}
                max_levels = int(list(data[attack][0].keys())[-1].replace('lv','',1))
                lvl_ranges = [l.replace('lv','',99) for l in list(data[attack][0].keys())[1:]]
                for lvl in lvl_ranges:
                    for dict_ in data[attack][1:]:                
                        key, index, value = check_if_normal(dict_, lvl)
                        if key == index == value == None:
                            key, lvl_, value = check_if_charged(dict_, lvl)
                            if key == lvl_ == value == None:
                                if key == index == value == None:
                                    key, lvl_, value = check_if_plunge(dict_, lvl)
                                    if key == lvl_ == value == None:
                                        pass
                                    else:
                                        if key not in temp_dict['plunge']:
                                            temp_dict['plunge'][key] = {}
                                            temp_dict['plunge'][key][lvl_] =  value
                                        else:
                                            temp_dict['plunge'][key][lvl_] =  value
                                        temp_dict['plunge']['max_level'] = lvl_
                            else:
                                if key not in temp_dict['charged']:
                                    temp_dict['charged'][key] = {}
                                    temp_dict['charged'][key][lvl_] =  value
                                else:
                                    temp_dict['charged'][key][lvl_] =  value
                                temp_dict['charged']['max_level'] = lvl_
                        else:
                            if key not in temp_dict['normal']:                            
                                temp_dict['normal'][key] = {lvl : []}   
                            if lvl not in temp_dict['normal'][key]: 
                                temp_dict['normal'][key][lvl] = []
                            temp_dict['normal'][key][lvl].insert(index, value)
                    temp_dict['normal']['max_level'] = max_levels        
            else:
                key = get_elemental_keys(attack)
                for dict_ in data[attack][1:]:                
                    if key is not None:
                        if key not in temp_dict:
                            temp_dict[key] = {}
                        lvl_ranges = [l.replace('lv','',99) for l in list(data[attack][0].keys())[1:]]
                        for lvl_ in lvl_ranges:
                            sub_key, lvl, value = check_if_elemental(dict_, lvl_)
                            if sub_key not in temp_dict[key]:
                                temp_dict[key][sub_key] = {}
                            temp_dict[key][sub_key][lvl] = value
    return temp_dict
            


   
search = fetch_character_lists()[42:]

for link in search:
    stats, atks = fetch_character_stats(link)
    stat_data = prettify_stats(stats)
    atk_data = prettify_atks(atks)

    data = {
    'Stats': stat_data,
    'Talents': atk_data
    }
    char = link.split('/')[-2]
    print('fetched stats for', char)
    if not exists(getcwd()+'/stats/'):
        mkdir(getcwd()+'/stats/')
    with open(getcwd()+'/stats/'+char+'.json','w') as f:
        dump(data,f, indent=1)
    sleep(5)
