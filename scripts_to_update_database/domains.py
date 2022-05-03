from fileinput import filename
from lib2to3.pytree import convert
from numpy import save
from requests import get
from bs4 import BeautifulSoup
from json import dump, load
from PIL import Image, ImageFilter
from io import BytesIO

from os import getcwd
from os.path import exists

def load_file(filename):
    if exists(getcwd()+'/'+filename):
        with open(getcwd()+'/'+filename, 'r') as f:
            return load(f)
    return {}

def save_file(data,filename):
    with open(getcwd()+'/'+filename, 'w') as f:
            dump(data, f, indent=1)

def generate_id(string:str):
    seps = [',','.','/','\\','-','!','`','|']
    for s in seps:
        string = string.replace(s,'',99)
    return string.replace(' ','_',99).lower()

def get_bs(link : str):

    src= get(link).content
    return BeautifulSoup(src,'lxml')
def get_image(img):    
    if 'data-src' in img.attrs:
        if img.attrs['data-src'].startswith("http"):
            return img.attrs['data-src'][:img.attrs['data-src'].find('/revision')]
        else:
            return img.attrs['src'][:img.attrs['src'].find('/revision')]
    else:
        return img.attrs['src'][:img.attrs['src'].find('/revision')]
     
def get_domain_info(bs: BeautifulSoup, id:str):
    ele = bs.find('span', {'id': id})
    data = {}
    if ele.parent is not None:
        link = [e for e in ele.parent.find_next_siblings() if e.name=='p']
        if len(link) > 0:
            domain = "https://gensin-impact.fandom.com/"+link[0].find_all("a")[0].attrs['href']
            bs_ = get_bs(domain)
            data['location'] = bs_.find('div', {'data-source': 'type'}).find('div').text.strip()
            data['type'] = bs_.find("h2", {'data-item-name': 'secondary_title'}).find('a').attrs['title']
            data['description'] = bs_.find('div', {'data-source': 'description'}).text.replace("Description",'',1).strip()
            data['required_ar'] = bs_.find("div", {'data-source': 'requiredAR'}).text.strip()
            data['required_party_level'] = bs_.find("div", {'data-source': 'recLevel'}).text.strip()
            img = bs_.find('figure', {'data-source': 'image'})
            if img.find('img') is not None:               
                data['image'] = img.find("a").attrs['href'][:img.find("a").attrs['href'].find('/revision')]
            data['title'] = bs_.find("h2", {'data-source': 'title'}).text.strip()
            data['id'] = generate_id(data['title'])
            return data


def get_table(bs: BeautifulSoup, id: str):

    ele = bs.find('span', {'id': id})
    if ele.parent is not None:
        table = [e for e in ele.parent.find_next_siblings() if e.name =='table']
        link = [e for e in ele.parent.find_next_siblings() if e.name=='p']
        if len(table) > 0:
            return table[0]
'''
data = load_file('domains.json')
REGIONS = ['Mondstadt','Liyue','Inazuma']

bs = get_bs('https://genshin-impact.fandom.com/wiki/Weapon_Ascension_Materials')

for region in REGIONS:
    table = get_table(bs, region)
    domain = get_domain_info(bs, region)
    if 'domains' not in data:
        data['domains'] = {}
    
    if domain is not None:       
        data['domains'][domain['id']] = {k : domain[k] for k in domain if k !=' id'}

    if 'rotations' not in data:
        data['rotations'] = []

    rotation_data = {}

    rows = table.find_all("tr")
    for r in rows[1:-2]:
        columns = r.find_all('td')
        days = columns[0].text.strip().split('/')
        series = columns[1].find("a").attrs['title']
        items_list = []
        items = columns[1].find_all('div', {'card_image'})
        for itm in items:
            title_ = itm.find('a').attrs['title']
            image = get_image(itm.find('a').find('img'))

            items_list.append({'title': title_,
                                'img': image})
        for_ = columns[2].find_all('div', {'card_image'})
        for_items = []
        for itm in for_:
            title_ = itm.find('a').attrs['title']
            image = get_image(itm.find('a').find('img'))

            for_items.append({'title': title_,
                                'img': image})
        data['rotations'].append({
            'days': days,
            'domain_id': domain['id'],
            'items': items_list,
            'series': series,
            'for': for_items
        })

save_file(data, 'domains.json')

'''

def resize_image(size, h):
    ratio = h/size[1]
    return (int(round(size[0]*ratio)), int(round(size[1]*ratio)))


data = load_file('domains.json')

for rotation in data['rotations']:
    domain = data['domains'][rotation['domain_id']]
    if 'forgery' in domain['type'].lower():
        rotation['type'] = 'weapon'
    else:
        rotation['type'] = 'talents'

    img = Image.open(BytesIO(get(domain['image']).content), 'r').convert('RGBA')
    size = resize_image(img.size, 1102)
    print(size)
    img = img.resize(size)

    blurred = img.filter(ImageFilter.GaussianBlur(radius=20))
    img_new = Image.new('RGBA', (1920,1102))
    img_new.paste(blurred, (0,0), blurred)

    imgs = [i['img'] for i in rotation['items']]
    file_name = rotation['domain_id']+'_'+ '_'.join([d.lower() for d in rotation['days']])+'.png'
    print(file_name)
    items_pos = {
        "1": {
            "x" : 730,
            "y" : 0
        },
        "2" : {
            "x" : 1060,
            "y" : 360
        },
        "3" : {
            "x": 730,
            "y": 750

        },
        "4" : {
            "x": 440,
            "y": 360

        }
        }

    for i in range(1, len(imgs)+1,1):
        i_mg = Image.open(BytesIO(get(imgs[i-1]).content), 'r').convert("RGBA")
        img_new.paste(i_mg, (items_pos[str(i)]['x'], items_pos[str(i)]['y']), i_mg)
    rotation['file'] = file_name
    img_new.save(getcwd()+'/domains/'+file_name)

save_file(data, 'domains.json')