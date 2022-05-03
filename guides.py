from os import getcwd, listdir, mkdir
from os.path import exists
from base.resource_manager import ResourceManager
from json import load, dump
import requests
from bs4 import BeautifulSoup
from time import sleep
rm = ResourceManager()

character_file_path = rm.genpath('data', 'characters.json')
with open(character_file_path, 'r') as f:
    character_data = load(f)

character_names = list(character_data.keys())
tree = ['Ascension Guides','Burst DPS','Healer','Main DPS','Sub DPS','Support']




def get_folder(character_name: str):

    folder = rm.goto('images/characters').get("folders")
    folder_search = rm.search(character_name, folder)
    if folder_search is not None:
        return folder_search
    else:
        character = rm.search(character_name, character_names)
        if character is not None:
            if len(character.split(" ")) > 1:
                if not exists(getcwd()+f'/assets/images/characters/{character.split(" ")[1]}'):
                    mkdir(getcwd()+f'/assets/images/characters/{character.split(" ")[1]}')
                return character.split(" ")[1]
            else:
                if not exists(getcwd()+f'/assets/images/characters/{character}'):
                    mkdir(getcwd()+f'/assets/images/characters/{character}')
                return character
        if not exists(getcwd()+f'/assets/images/characters/Traveler'):
            mkdir(getcwd()+f'/assets/images/characters/Traveler')
        return 'Traveler'
def folder_from_type(character_name: str, type_str: str):
    if type_str == 'as':
        if character_name == None:
            character_name = 'Traveler'
        if not exists(getcwd()+f'/assets/images/characters/{character_name}/ascension_talents'):
            mkdir(getcwd()+f'/assets/images/characters/{character_name}/ascension_talents')
        return 'ascension_talents'
    if type_str == 'b':
        if character_name == None:
            character_name = 'Traveler'
        if not exists(getcwd()+f'/assets/images/characters/{character_name}/builds'):
            mkdir(getcwd()+f'/assets/images/characters/{character_name}/builds')
        return 'builds'
    return ''

def get_type_from_string(character:str, string: str, folder:bool = True):
    if 'ascension' in string.lower():
        if folder:
            return folder_from_type(character, 'as')
        return 'as'
    else:
        if folder:
            return folder_from_type(character, 'b')
        return 'b'

def get_file_type_name(type_ : str):
    if 'ascension' in type_.lower():
        return 'ascension.png'
    else:        
        return type_.lower().replace(' ','_',99)+'.png'


def get_github_tree(link: str):
    base_link = 'https://github.com/FortOfFans/FortOfFans.github.io/tree/main/{link}'.format(link=link.replace(' ','%20',99))
    links = []
    with requests.get(base_link) as f:
        bs = BeautifulSoup(f.content, 'lxml')

        rows = bs.find_all("div", {'role': 'row'})
        for r in rows:
            ele = r.find('div', {'role':'rowheader'})
            if ele is not None:
                links.append(ele.find("a").attrs['href'].split('/')[-1])
    return links[1:]

def get_raw_link(key:str, file:str):
    base_link = 'https://raw.githubusercontent.com/FortOfFans/FortOfFans.github.io/main/{key}/{file}'
    return base_link.format(key=key.replace(' ','%20',99), file=file)


def download_image(tree: str, link: str, type:str):

    base_folder = rm.path.format(path='images/characters')
    character = link.split("_")[1].split(".")[0]
    character_folder = get_folder(character)

    type_folder = get_type_from_string(character_folder, type)
    file_name = get_file_type_name(type)
    print(file_name)
    if not exists(base_folder+'/'+character_folder+'/'+type_folder+'/'+ file_name):
        with open(base_folder+'/'+character_folder+'/'+type_folder+'/'+ file_name, 'wb') as f:
            raw_link = get_raw_link(tree, link)
            src = requests.get(raw_link)
        
            f.write(src.content)
            print('downloaded', raw_link, 'to', base_folder+'/'+character_folder+'/'+type_folder+'/', 'as', file_name)
    else:
        file_name = '_'.join(link.split("_")[2:]).lower().strip() if len(link.split('_')) > 1 else link
        if file_name.strip() == '':
            file_name = link
        with open(base_folder+'/'+character_folder+'/'+type_folder+'/'+ file_name, 'wb') as f:
            raw_link = get_raw_link(tree, link)
            src = requests.get(raw_link)
        
            f.write(src.content)
            print('downloaded', raw_link, 'to', base_folder+'/'+character_folder+'/'+type_folder+'/', 'as', file_name)

  



for t in tree[4:]:
    links = get_github_tree(t)
    print(links)
    for link in links:
        print(t)
        download_image(t, link, t)
        sleep(2)