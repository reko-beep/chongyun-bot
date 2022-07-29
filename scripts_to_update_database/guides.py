from distutils.command.build import build
from genericpath import isdir
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

BASE_PATH = rm.genpath("images/characters",'')

SWITCHER = {
    'ascension': 'ascension_talents',
    'build': 'builds',
    'base': ''
}

def get_character_folder(character_name: str):
    if 'traveler' in character_name:
        return BASE_PATH+'traveler'
    print(character_name)
    character = rm.search(character_name, character_names, False)

    folders = [folder for folder in listdir(BASE_PATH) if isdir(BASE_PATH+folder)]
    print(character, folders)
    checker =  rm.search(character, folders)
    if checker is not None:
        return BASE_PATH+checker
    return BASE_PATH+character



def folder_exists(folder_path: str):

    folder_names = folder_path.split('/')
    for name in folder_names:
        if name != '':
            path = folder_path[:folder_path.find(name)+len(name)]
                
            if not exists(path):
                mkdir(path)
    
    return True
       



def download_image(link: str, folder_path: str, ascension: bool=False, build_type:str=''):
    
    file_name = link.split("/")[-1]
    if ascension:
        file_name = 'ascension.jpg'
    else:
        file_name = build_type.replace("%20", '_', 99)
    if len(link.split("/")[-1].split("_")) > 2:
        file_name += '_'+link.split("/")[-1].split("_")[-1].split('.')[0]
    if '.jpg' not in file_name:
        file_name += '.jpg'
    file_name = file_name.lower()
    with requests.get(link) as r:
        with open(folder_path+"/"+file_name, 'wb') as f:
            f.write(r.content)


def download_ascension_guides():
    '''

    Download all world of teyvat ascension guides

    '''
    link = 'https://github.com/FortOfFans/FortOfFans.github.io/tree/main/Ascension%20Guides/'
    download_link = 'https://raw.githubusercontent.com/FortOfFans/FortOfFans.github.io/main/Ascension%20Guides/{link}'
    src = requests.get(link).content
    bs = BeautifulSoup(src, 'lxml')

    '''
    get all ascension images links
    '''

    rows = bs.find_all('div', {'role': 'row'})

    images_links = []
    for row in rows:

        link_ = row.find("a")
        if link_ is not None:
            images_links.append(download_link.format(link=link_.attrs['href'].split('/')[-1]))
    
    for l in images_links[1:]:
        print('downloading', l)
        character_name = l.split("/")[-1].split('_')[1].lower().replace(".jpg", '', 1).replace(".jpg", '', 1)
        folder_path = get_character_folder(character_name)
        path_final = folder_path+"/"+SWITCHER.get("ascension")+"/"
        checker = folder_exists(path_final)
        if checker:
            
            download_image(l, path_final, True)

def download_build():
    '''

    Download all world of teyvat ascension guides

    '''
    link = 'https://github.com/FortOfFans/FortOfFans.github.io/tree/main/Characters/en-US/{type}/'
    download_link = 'https://raw.githubusercontent.com/FortOfFans/FortOfFans.github.io/main/Characters/en-US/{type}/{link}'
    
    TYPES = ['Burst%20DPS', 'Sub%20DPS','Healer', 'Support']
    '''
    get all ascension images links
    '''

    for type_ in TYPES:

        src = requests.get(link.format(type=type_)).content
        bs = BeautifulSoup(src, 'lxml')
        rows = bs.find_all('div', {'role': 'row'})

        images_links = []
        for row in rows:

            link_ = row.find("a")
            if link_ is not None:
                images_links.append(download_link.format(type=type_, link=link_.attrs['href'].split('/')[-1]))
        
        for l in images_links[1:]:
            print('downloading', l)
            character_name = l.split("/")[-1].split('_')[1].lower().replace(".jpg", '', 1).replace(".jpg", '', 1)
            folder_path = get_character_folder(character_name)
            path_final = folder_path+"/"+SWITCHER.get("build")+"/"
            checker = folder_exists(path_final)
            if checker:
                
                download_image(l, path_final, False, type_)

    
    
download_build()