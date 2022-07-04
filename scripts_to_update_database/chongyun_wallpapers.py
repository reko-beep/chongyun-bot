from requests import get

from bs4 import BeautifulSoup
from base.resource_manager import ResourceManager
from json import load, dump
rm = ResourceManager()
imgs = []

link = 'https://wall.alphacoders.com/tag/chongyun-(genshin-impact)-wallpapers?page={pg}'

for i in range(1,100,1):
    print(link.format(pg=i))
    src = get(link.format(pg=i)).content
    bs = BeautifulSoup(src, 'lxml')
    main_ = bs.find_all('div', {'class': 'thumb-container-big'})
    print(len(main_))
    if len(main_) != 0:
        for l in main_:
            pic = l.find('picture')
            if pic.find('img') is not None:
                if pic.find('img').attrs['src'] not in imgs:
                    imgs.append(pic.find('img').attrs['src'])
    else:
        break


DATA_PATH = rm.genpath('data', 'chongyun_wallpapers.json')
print(DATA_PATH)
with open(DATA_PATH, 'w') as f:
    dump({'data': imgs }, f, indent=1)