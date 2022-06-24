from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from pyparsing import col
import requests
import re
from json import dump
from base.resource_manager import ResourceManager

rm = ResourceManager()

DATA_PATH = rm.genpath('data')

URL = 'https://genshin-impact.fandom.com/wiki/Wishes/History'
SERVER_TIMES = {'asia': -1, 'eu': -7, 'na': -13}

def get_table(bs: BeautifulSoup, id_: str):

    ele = bs.find('span', {'id': id_})
    if ele is not None:
        element = ele.parent.find_next_sibling()
        while element.name != 'table':
            element = element.find_next_sibling()
        return element

def convert_time_region(time_string: str, region:str):

    dt = datetime.strptime(time_string.strip()+" +0800",'%Y-%m-%d %H:%M:%S %z')
    correction = SERVER_TIMES[region]
    time = dt+timedelta(hours=correction)

    return str(time).split('+')[0]
    
def find_image(element):
    if element is not None:
        if 'data-src' in element.attrs:
            if element.attrs['data-src'].startswith('http'):
                return element.attrs['data-src'][:element.attrs['data-src'].find('/revision')]
        else:
            if 'src' in element.attrs:
                if element.attrs['src'].startswith('http'):
                    return element.attrs['src'][:element.attrs['src'].find('/revision')]
    return 'http://www.wellesleysocietyofartists.org/wp-content/uploads/2015/11/image-not-found.jpg'

def generate_id(string: str):
    seps = ["'", '"', '!','.','.','/','\\',';',':','`']
    for s in seps:
        string = string.replace(s, '', 99)
    return string.replace(' ','_',99).lower()

src = requests.get(URL).content
bs = BeautifulSoup(src, 'lxml')
table = get_table(bs, 'All_Wishes')
data = {'characters': [], 'weapons': [], 'standard': [], 'novice': []}
rows = table.find_all('tr')
last_banner = {
    'title': '',
    'time' : '',
    'type' : ''

}
for r in rows:
    columns = r.find_all('td')
    if len(columns) == 3:
        title = columns[0].find('a').attrs['title']
        data_items = []
        featured = columns[1].find_all('div', {'class': 'card_container'})
        type_banner = ''
        if len(featured) != 0:
            for f in featured:
                item = f.find('div', {'class': 'card_image'})
                if item is not None:
                    if 'weapon' in item.find('img').attrs['alt'].lower():
                        type_banner = 'weapons'                    
                    if 'character' in item.find('img').attrs['alt'].lower():
                        type_banner = 'characters'
                    
                    data_items.append({
                        'rarity' : f.attrs['class'][1].split('_')[1],
                        'name' : item.find('a').attrs['title'],
                        'id' : generate_id(item.find('a').attrs['title'])
                    })
        if 'wanderlust' in title.lower():
        
            type_banner = 'standard'
        if 'beginner' in title.lower():
            
            type_banner = 'novice'

        

        time_list = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', columns[2].attrs['data-sort-value'])
        time_start = ''
        time_end = ''
        print(title, time_list)
        if len(time_list) > 0:
            if len(time_list) > 1:
                time_end = time_list[0]
                time_start = time_list[1]
            else:
                time_end = ''
                time_start = time_list[0]
            
        else:
            time_start = time_end = ''
        times = {}
        

        for reg in SERVER_TIMES:
            times[reg] = {}
            if time_start != '':
                times[reg]['start'] = convert_time_region(time_start, reg)
            
            if time_end != '':
                times[reg]['end'] = convert_time_region(time_end, reg)

        data[type_banner].append({
            'title': title.split('/')[0] if '/' in title else title,
            'items': data_items,
            'start': time_start,
            'end' : time_end,
            'reg_times' : times,
            'img': find_image(columns[0].find('img'))
        })
        if last_banner['time'] == time_start and last_banner['type'] == type_banner:
            data[type_banner][-1]['second_character_banner'] = True
        else:
            last_banner['time'] = time_start 
            last_banner['type'] = type_banner


with open(DATA_PATH+'/banners.json', 'w') as f:
    dump(data, f, indent=1)


