import requests
from bs4 import BeautifulSoup
from main import Fetcher
from logger import logc

class OST(Fetcher):
    def __init__(self):
        super().__init__()

    def fetch_albums(self, arg: str = 'Soundtrack?so=search'):
        src = self.get(arg).content
        bs = BeautifulSoup(src, 'lxml')

        lists = []
        table = bs.find_all('table')[1]
        rows = table.find_all('tr')
        for r in rows:
            if len(r.find_all('td')) >= 5:
                lists.append(r.find_all('td')[1].find('a').attrs['href'].split('/')[-1])


        logc(f'fetched list for albums {lists}')
        return lists

    def fetch_languages(self):
        return ['English','Chinese','Korean','Japanese']

    def fetch_tracks(self, album_link: str):
        src = self.get(album_link).content
        bs = BeautifulSoup(src, 'lxml')

        image = self.find_image(bs.find('figure', {'data-source': 'image'}))
        list_ = []
        tables = bs.find_all('table')
        for table in tables:
            rows = table.find_all('tr')[1:]

            for row in rows:
                columns = row.find_all('td')

                if (len(columns) >= 4):
                    name = columns[1].text.strip()
                    audio = columns[2].find('audio')
                    if audio is not None:
                        if audio.find('source') is not None:
                            audio = audio.find('source').attrs['src'][:audio.find('source').attrs['src'].find('/revision')]
                    
                    play = columns[3].text.strip()

                    list_.append({
                        'name': name,
                        'audio': audio,
                        'src': play,
                        'album_image': image
                    })
        album_name = album_link.replace('_',' ',99)
        logc('fetched tracks for album', album_name)
        return list_, album_name    



d = OST()
d.fetch_albums()