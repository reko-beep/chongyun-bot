from xml.dom.minidom import Element
from pyparsing import col
from requests import get
from bs4 import BeautifulSoup
from json import dump
from base.resource_manager import ResourceManager
rm = ResourceManager()
MAIN_URL = 'https://genshin-impact.fandom.com/wiki/Materials'
src = get(MAIN_URL).content
bs = BeautifulSoup(src, 'lxml')
columns = bs.find_all('div', {'class':'columntemplate'})
links = []
for column in columns:
    links_ = column.find_all("li")
    links += [f"https://genshin-impact.fandom.com"+l.find('a').attrs['href'] for l in links_]

OTHER_URL = 'https://genshin-impact.fandom.com/wiki/Talent_Level-Up_Materials'

PATH = rm.genpath('data')
src = get(OTHER_URL).content
bs = BeautifulSoup(src, 'lxml')
columns = bs.find_all('table', {'class':'nowraplinks'})
for column in columns:
    link_bar = column.find('td', {'class': 'navbox-list'})
    links_ = column.find_all('div', {'class' : "mini_card_container"}) if link_bar is not None else None
    if links_ is not None:
        links += [f"https://genshin-impact.fandom.com"+l.find('a').attrs['href'] for l in links_]

links += ['https://genshin-impact.fandom.com/wiki/Anemoculus', 'https://genshin-impact.fandom.com/wiki/Electroculus', 'https://genshin-impact.fandom.com/wiki/Geoculus']
print(links)

def get_table(bs: BeautifulSoup, id: str):
    table = bs.find('span', {'id': id})
    if table is not None:
        if table.parent is not None:
            tables = []
            siblings = table.parent.find_next_siblings()
            for sib in siblings:
                if sib.name == 'table':
                    tables.append(sib)
                if sib.name == 'h2':
                    break
            return tables if len(tables) > 0 else None


def get_material_info(link: str):
    src = get(link).content
    bs = BeautifulSoup(src, 'lxml')
    data = {}
    data_sources = [d.attrs['data-source'] for d in bs.find_all(attrs={'data-source': True})]
    print(data_sources)
    for ds in data_sources:
        element = bs.find(attrs={'data-source': ds})
        if 'source' in ds:
            if 'source' not in data:
                data['source'] = []
            text_ = element.find("div").text.strip()
            if 'sold' in text_.lower():
                if len(element.find_all('a')) > 0:
                    data['shop'] = [l.attrs['title'] for l in element.find_all('a')]
            else:
                data['source'].append(text_)
        else:

            if ds == 'image':
                img = find_image(element.find("img"))
                data['img'] = img
            else:
                if ds == 'title':    
            
                    data[ds] = element.text.strip()
                else:
                    if ds == 'rarity':
                        number = '⭐'*int(element.find("div").find("img").attrs['alt'][0])
                        data[ds] = number
                    else:
                        if ds == 'type':
                            types = [a.attrs['title'] for a in element.find_all("a")]
                            data[ds] = types
                        else:

                            if 'lb' in ds:
                                ds = ds.replace("lb", 'living_being_',1).lower()
                            if element.find("div") is not None:
                                data[ds] = element.find("div").text.strip()
                            else:
                                data[ds] = element.text.strip()

    '''

    ascension usage

    '''

    ascension_usage_cards = []
    element = bs.find('span', {'id': 'Ascension_Usage'}) 
    if element is not None:
        element = element.parent.find_next_sibling()
        while element.name != 'h2':
            if element.name == 'div' and 'card_container' in element.attrs['class']:
                ascension_usage_cards.append(element)
            element = element.find_next_sibling()
    data['ascension_usage'] = {'character': [], 'weapon': [], 'misc': []}
    
    
    if len(ascension_usage_cards) > 0:
        for ascen in ascension_usage_cards:
            card = ascen.find('div', {'class': 'card_image'})
            if card is not None:
                type_ = card.find('img').attrs['alt'].split(' ')[0].lower() if card.find("img") is not None else 'misc'
                name = card.find("a").attrs['title']
                data['ascension_usage'][type_].append(name)
    if len(data['ascension_usage']['character']) == 0 and len(data['ascension_usage']['misc']) == 0 and len(data['ascension_usage']['weapon']) == 0:
        data.pop('ascension_usage')


    '''
    talent leveling usage
    '''


    
    ascension_usage_cards = []
    element = bs.find('span', {'id': 'Talent_Leveling_Usage'}) 
    if element is not None:
        element = element.parent.find_next_sibling()
        while element.name != 'h2':
            if element.name == 'div' and 'card_container' in element.attrs['class']:
                ascension_usage_cards.append(element)
            element = element.find_next_sibling()
    data['talent_leveling_usage'] = {'character': [], 'weapon': [], 'misc': []}
    
    
    if len(ascension_usage_cards) > 0:
        for ascen in ascension_usage_cards:
            card = ascen.find('div', {'class': 'card_image'})
            if card is not None:
                type_ = card.find('img').attrs['alt'].split(' ')[0].lower() if card.find("img") is not None else 'misc'
                name = card.find("a").attrs['title']
                data['talent_leveling_usage'][type_].append(name)
    if len(data['talent_leveling_usage']['character']) == 0 and len(data['talent_leveling_usage']['misc']) == 0 and len(data['talent_leveling_usage']['weapon']) == 0:
        data.pop('talent_leveling_usage')
    '''
    craft usage
    '''
    data['craft_usage'] = []
    item_splitter = '×'
    craft_usage_table = get_table(bs, 'Craft_Usage')
    if craft_usage_table is not None:
        for table in craft_usage_table:
            rows = table.find_all('tr')
            for r in rows:
                columns = r.find_all('td')
                if len(columns) == 3:
                    name = columns[0].text.strip()
                    type_process = columns[1].text.strip()                    
                    recipe_items = [{'item': it.split(item_splitter)[0], 'amount': it.split(item_splitter)[1]} for it in correct_text(columns[2].get_text(separator='\n').split('\n'))]
                    data['craft_usage'].append({
                        'name': name,
                        'type': type_process,
                        'items': recipe_items
                    })
    if len(data['craft_usage']) == 0:
        data.pop('craft_usage')
    '''
    fishing locations
    '''
    data['fishing_location'] = {}
    if 'fish' in [d.lower() for d in data['type']]:
        max_galleries = 3
        for i in range(max_galleries):
            element = bs.find('div', {'id': f'gallery-{i}'})
            if element is not None:
                city = element.find_previous_sibling().text.strip()
                if city not in data['fishing_location']:
                    if city.lower() != 'gallery':
                        data['fishing_location'][city] = []
                
                images = element.find_all('div', {'class': 'wikia-gallery-item'})
                for img in images:
                    img_link = img.find('a', {'class': 'image'})
                    if img_link is not None:
                        link = find_image(img_link.find('img'))
                        text = 'N/A'
                        if img.find('div', {'class': 'lightbox-caption'}).find('a') is not None:
                            text = img.find('div', {'class': 'lightbox-caption'}).find('a').attrs['title']
                        if city.lower() == 'gallery':
                            data['fish_image_splash'] = link
                        else:
                            data['fishing_location'][city].append({'img': link, 'title': text})

    if len(data['fishing_location']) == 0:
        data.pop('fishing_location')   

    '''
    recipes
    '''
    data['recipes'] = []
    recipes = bs.find_all('div', {'class': 'new_genshin_recipe_container'})
    if len(recipes) != 0:
        for recipe in recipes:

            type_ = recipe.find("span", {'class': 'new_genshin_recipe_header_main'}).find("span", {"class": 'new_genshin_recipe_header_text'}).text.strip()
            minutes = recipe.find("span", {'class': 'new_genshin_recipe_header_sub'}).find("span", {"class": 'new_genshin_recipe_header_text'}).text.strip() if recipe.find("span", {'class': 'new_genshin_recipe_header_sub'}) is not None else 'N/A'
            items = recipe.find("div", {'class': 'new_genshin_recipe_body'}).find_all("div", {"class" :"card_container"})
            print(items)
            item_list = []
            for itm in items:

                name = itm.find("div", {'class': 'card_image'}).find("a").attrs['title']
                amount = itm.find("div", {'class': 'card_text'}).text.strip()

                item_list.append({'name': name, 'amount': amount})
            
            yields = []
            yields_element = recipe.find("div", {'class': 'new_genshin_recipe_body_yield'}).find_all('div', {'class': 'card_container'})
            for y in yields_element:
                name = y.find("div", {'class': 'card_image'}).find("a").attrs['title']
                amount = y.find("div", {'class': 'card_text'}).text.strip()
                try:
                    i_ = item_list.index({'name': name, 'amount': amount})
                except ValueError:
                    pass
                else:
                    item_list.pop(i_)
                yields.append({'name': name, 'amount': amount})
            
            data['recipes'].append({
                'type': type_,
                'minutes': minutes,
                'items': item_list,
                'yield': yields
            })
    data['videos'] = []
            
    videos = bs.find_all('div', {'class': 'embedvideo'})
    if len(videos) != 0:
        for video in videos:
            url = video.find('iframe').attrs['src'].replace('?','',99)
            if url.startswith('//'):
                url = f'https:{url}'
            link = f"http://img.youtube.com/vi/{url.split('/')[-1].replace('?','',99)}/0.jpg"
            text = video.find('div', {'class': 'thumbcaption'}).text if video.find('div', {'class': 'thumbcaption'}) is not None else 'No Description'
            data['videos'].append({
                'url': url,
                'img': link,
                'text' : text
            })
                



                









    return data
        
def correct_text(text_list: list):
    text = []
    counter = 0
    list_ =  [t.strip() for t in text_list if t.strip() != '']
    for li in range(len(list_) // 2):
        tex = ' '.join(list_[li * 2: (li*2)+2])
        text.append(tex)
    return text
        




def find_image(img):
    if img.attrs['src'].startswith('http'):
        return img.attrs['src'][:img.attrs['src'].find('/revision')]
    else:
        return img.attrs['data-src'][:img.attrs['data-src'].find('/revision')]

data = {}
for link in links:
    ds = get_material_info(link)
    data[ds['title']] = ds

with open(PATH+"/materials.json", 'w') as f:
    dump(data, f, indent=1)


