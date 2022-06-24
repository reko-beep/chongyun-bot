from requests import get
from bs4 import BeautifulSoup
from json import load, dump

URL = 'https://genshin-impact.fandom.com/wiki/Shops'

src = get(URL).content
bs = BeautifulSoup(src, 'lxml')

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

def find_image(img):
    if img.attrs['src'].startswith('http'):
        return img.attrs['src'][:img.attrs['src'].find('/revision')]
    else:
        return img.attrs['data-src'][:img.attrs['data-src'].find('/revision')]

def get_shop_info(link: str):
    src = get(link).content
    bs = BeautifulSoup(src, 'lxml')

    data = {}
    data['vendor'] = link.split('/')[-1].replace('_',' ',99).title()
    img = bs.find("figure", {'data-source': 'image'})
    if img is not None:
        data['image'] = find_image(img.find('img'))
    
    data_sources = ['realname', 'region']
    for ds in data_sources:
        element = bs.find("div", {'data-source': ds})
        if element is not None:
            data[ds] = element.find('div').text.strip()
    
    reward = bs.find("div", {'data-source': 'dialoguereward'})

    if reward is not None:
        text = reward.find('div', {'class':'card_container'})
        if text is not None:
            data['dialoguereward'] = text.find('div', {'class':'card_image'}).find('a').attrs['title']
    
    shop_tables = get_table(bs, 'Shop')
    for count, table in enumerate(shop_tables):
        rows = table.find_all('tr')
        headings = [h.text.strip() for h in rows[0].find_all('th')]
        values = []
        for r in rows[1:-1]:
            values.append([c.text.strip() for c in r.find_all('td')])
        data[f'shop_items_{count}'] = {
            'headings': headings,
            'values': values
        }

    location = bs.find('div', {'id': 'gallery-0'})
    data['locations'] = []
    location_imgs = location.find_all("div", {"class": "wikia-gallery-item"}) if location is not None else None
    if location_imgs is not None:
        for img in location_imgs:

            img_e = find_image(img.find("div",{'class': 'thumb'}).find('a').find('img'))
            text = img.find("div", {'class': "lightbox-caption"}).text.strip()
            data['locations'].append({'img': img_e, 'text': text})

    return data




data = {'shops': []}
tables = get_table(bs, 'Local_Specialties')
print(tables)
if tables is not None:
    for table in tables:
        rows = table.find_all('tr')
        for r in rows:
            columns = r.find_all('td')
            if len(columns) > 1:
                link = 'https://genshin-impact.fandom.com'+columns[0].find('a').attrs['href']
                d = get_shop_info(link)              
                data['shops'].append(d)

with open('shops.json', 'w') as f:
    dump(data, f, indent=1)


