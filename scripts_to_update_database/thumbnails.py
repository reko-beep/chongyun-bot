from bs4 import BeautifulSoup
from requests import get
from os import getcwd

def find_image(img):
    if img.attrs['src'].startswith('http'):
        return img.attrs['src'][:img.attrs['src'].find('/revision')]
    else:
        return img.attrs['data-src'][:img.attrs['data-src'].find('/revision')]

URL = 'https://genshin-impact.fandom.com/wiki/Characters/List'


src = get(URL).content

bs = BeautifulSoup(src, 'lxml')
tables = bs.find_all('table')
tables_ = tables[1:3]

for table in tables_:
    rows = table.find_all('tr')[1:]
    for r in rows:
        columns = r.find_all("td")
        if columns[0].find('img') is not None:
            img = find_image(columns[0].find('img'))
        filename = columns[1].text.strip()

        with open(getcwd()+'/assets/images/thumbnails/'+filename+".png", 'wb') as f:
            with get(img) as r:
                f.write(r.content)
