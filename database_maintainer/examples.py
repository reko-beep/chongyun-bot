
from os import getcwd
from bs4 import BeautifulSoup

import requests
from artifacts import Artifacts
from characters import Characters
from domain import Domains
from voiceovers import VoiceOvers
from weapons import Weapons
from ost import OST
from json import dump, load

def fetch_artifacts(path):

    '''
    Fetches all artifacts from genshin fandom
    '''
    

    save_data = {}
    test = Artifacts()
    sets = test.fetch_lists()
    for set in sets:
        data, name = test.fetch(set)
        save_data[name] = data
    
    with open(path+ '/artifacts.json','w') as f:
        dump(save_data,f,indent=1)

def fetch_characters(path):
    '''
    Fetches all characters from genshin fandom
    '''
    save_data = {}
    test = Characters()
    list_,info = test.fetch_lists()
    for character in list_:
        print(character, list_, info, list_.index(character))
        more = info[list_.index(character)]
        data,name = test.fetch(character)
        if 'image' in data:
            data['image'].append(more.get('thumbnail','Not found'))
        else:
            data['image'] = [more.get('thumbnail','Not found')]
        more.pop('thumbnail')
        more_keys = list(more.keys())
        for key in more_keys:
            if key in data:
                pass
            else:
                data[key] = more.get(key,'Not Found')       
        save_data[name] = data
    with open(path + '\characters.json','w') as f:
        dump(save_data,f,indent=1)


def fetch_domains(path):
    save_data = {}
    d = Domains()
    list_ = d.fetch_lists()
    for type in list_:
        data = d.fetch(type)
        key = d.generate_key(type)
        save_data[key] = data
    with open(path+"/domains.json",'w') as f:
        dump(save_data,f,indent=1)
        



#
# search domain for a a type, city, day


#with open('domains.json','r') as f:
#    data = load(f)

#domain = Domains()
#result = domain.search_for_domain(data, 'weapon_ascension_materials','mondstadt','tuesday')

#
#   creates single image for all images
# 

#image_buffer = domain.create_image(result['images'])



def fetch_voiceovers(path):
    '''
    Fetches all characters from genshin fandom
    '''
    voice = VoiceOvers()

    languages = voice.fetch_languages()
    characters = voice.fetch_characters()
    data_save = {}
    for language in languages:
        for character in characters:
            data = voice.fetch_voiceovers(character,language)
            if language in data_save:
                data_save[language][character.replace('_',' ',99)] = data
            else:
                data_save[language] = {character.replace('_',' ',99) : data}

    with open(path + '/voiceovers.json','w',encoding='utf-8') as f:
        dump(data_save,f,indent=1)

def fetch_weapons(path):
    '''
    Fetches all weapons from genshin fandom
    '''
    save_data = {}
    test = Weapons()
    data_ = {}
    for type in test.types:
        list_weapons = test.fetch_lists(type)
        for weapon in list_weapons:
            name,data = test.fetch(weapon)

            data_[name] = data
            
   
    with open(path+ f'/weapons.json','w') as f:
        dump(data_,f,indent=1)

def fetch_osts(path):
    save_data = {}
    d = OST()
    albums = d.fetch_albums()
    for album in albums:
        data, name = d.fetch_tracks(album)        
        save_data[name] = data
    with open(path+"/albums.json",'w') as f:
        dump(save_data,f,indent=1)



'''
save_data = {}
test = Characters()
list_,info = test.fetch_lists()
for char in list_:
    r = requests.get('https://genshin-impact.fandom.com/wiki/{char}/Voice-Overs'.format(char=char)).content
    print('https://genshin-impact.fandom.com/wiki/{char}/Voice-Overs'.format(char=char))
    bs =BeautifulSoup(r, 'lxml')
    story = bs.find('span', {'id': 'Story'})
    tables = []
    if story is not None:
        element = story.parent.find_next_sibling()
        while element.name != 'h2':
            if element.name == 'table':
                tables.append(element)
            element = element.find_next_sibling()

    for table in tables:

        rows = table.find_all('tr')[1:]
        quotes = []

        for r in rows:

            columns = r.find('td')            
            if columns is not None:
                t = columns.text.strip()[columns.text.strip().find('.ogg')+len('.ogg'):]
                print(t)
                if t.startswith('Media:'):
                    pass
                else:
                    quotes.append(t)
        save_data[char] = quotes

with open('char_quotes.json', 'w') as f:
    dump(save_data, f, indent=1)
    '''


fetch_voiceovers(getcwd()) 