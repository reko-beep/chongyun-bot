from requests import get
from bs4 import BeautifulSoup
from time import sleep
from os import getcwd, listdir
from os.path import isfile
from json import load, dump
from base.resource_manager import ResourceManager

rm = ResourceManager()

DATA_PATH = rm.genpath('data')
IMAGES_PATH = rm.genpath('images/weapons')

weapon_names = []
weapon_data = {}
with open(DATA_PATH+'/weapons.json', 'r') as f:
    weapon_data = load(f)

weapon_names = list(weapon_data.keys())
def get_weapon_name(wep_name: str):    

    for wep in weapon_names:        
        print(wep_name.lower(), wep.lower(), wep_name.lower() in wep.lower())
        if wep_name.lower() in wep.lower():            
            return wep+'.jpg'
    return ''.join(wep_name)+'_dberror.jpg'

def get_filename(wep_name:str):
    files = [f for f in listdir(IMAGES_PATH) if isfile(IMAGES_PATH+'/'+f)]
    for f in files:
        if wep_name.lower() in f.split(".")[0].lower():
            return f


def download_files():
    url = 'https://github.com/FortOfFans/FortOfFans.github.io/tree/main/Weapons'
    raw_url = 'https://raw.githubusercontent.com/FortOfFans/FortOfFans.github.io/main/Weapons/{weapon}'

    r = get(url).content
    bs = BeautifulSoup(r, 'lxml')
    rows = bs.find_all("div", {'role': 'row'})
    print(len(rows))
    links = []
    raw_links = []
    for row in rows:
        link_element = row.find('div', {'role': 'rowheader'})
        if link_element is not None:
            links.append(link_element.find("a").attrs['href'])

    for link in links:
        raw_links.append(raw_url.format(weapon=link.split('/')[-1]))

    for raw in raw_links:
        r = get(raw).content
        url_weapon_name = raw.split('/')[-1].replace('%20',' ', 99).replace("'", "",9).replace("-", " ", 99).split('.')[0]
        wep_ = get_weapon_name(url_weapon_name)
        with open(IMAGES_PATH+ wep_, 'wb') as f:
            f.write(r)
        sleep(2)




download_files()
for wep in weapon_data:
    file = get_filename(wep)
    weapon_data[wep]['file'] = file

with open(DATA_PATH+"/weapon_filed.json", 'w') as f:
    dump(weapon_data, f, indent=1)
