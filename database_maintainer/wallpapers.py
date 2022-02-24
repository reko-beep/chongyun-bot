
import requests
from bs4 import BeautifulSoup
from time import sleep
from json import dump

base_url = 'https://wall.alphacoders.com/by_sub_category.php?id=333944&name=Genshin+Impact+Wallpapers&page={pg}'

data_chars = {}

def generate_link(link, id_link):
    id_ = 0
    if 'i=' in id_link:
        id_ = id_link[id_link.find('i=')+len('i='):]
    if id_ != 0:
        main_link = link[:link.find('/thumb')]

        ext = link[-3:]

        return main_link +'/'+ id_ + '.'+ext

def check_pages(BSOBJ):
    p = BSOBJ.find('div', {'class': 'hidden-xs visible-sm'})
    print(p)
    pagination = p.find('ul', {'class': 'pagination'})
    print(pagination)
    return len(pagination.find_all('li'))

def get_characters():
    src = requests.get(base_url).content
    bs = BeautifulSoup(src, 'lxml')

    char = bs.find('div', {'class':'characters-container'})
    data_links = {}
    chars = char.find_all('h4')
    for img in chars:

        link_id = img.find('a')
        if link_id is not None:
            id_ = link_id.attrs['href']
            if id_ not in data_links:
                data_links[link_id.text.strip()] = id_+ "?page={page}"
    return data_links



chars = get_characters()

for char in chars:
    url = chars[char]
    data = []
    page_end = 171
    first_url = ''
    for pg in list(range(1,171,1)):
        
        print('char', char,'page now', pg ,'end page', page_end, 'first url', first_url)
        if pg > page_end:
            break
        src = requests.get(url.format(page=pg)).content
        bs = BeautifulSoup(src, 'lxml')
        images = bs.find_all('div', {'class':'boxgrid'})
        
        for img in images:
            
            link_id = img.find('a')
            if link_id is not None:
                id_ = link_id.attrs['href']
                if images.index(img) == 0:   
                    print('now url',id_)
                    if id_ != first_url:                 
                        first_url = id_
                    else:
                        page_end = pg
                    
            picture = img.find('picture')

            if picture is not None:
                img_ = picture.find('img')
                if img_ is not None:
                    l = generate_link(img_.attrs['src'], id_)
                    if l not in data:
                        data.append(l)
        data_chars[char] = data
        sleep(5)



with open('wallpapers.json','w') as f:
    dump(data_chars, f, indent=1)