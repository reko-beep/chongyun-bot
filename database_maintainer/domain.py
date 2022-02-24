from os import getcwd
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
from io import BytesIO
from main import Fetcher
from nextcord import File, Embed

class Domains(Fetcher):
    def __init__(self):
        super().__init__()


    def fetch_lists(self):
        return ['Weapon_Ascension_Materials','Talent_Level-Up_Materials']

    def fetch(self,arg):
        save_data = []
        src = self.get(arg=arg).content
        bs = BeautifulSoup(src, 'lxml')
        nations = ['Mondstadt','Liyue','Inazuma']       
        type_key = self.generate_key(arg)
        for nation in nations:
            main = bs.find('span',{'id': nation}).parent
            table = [i for i in main.find_next_siblings() if i.name == 'table'][0]
            area_element = main.find_next_sibling()
            area = ''
            if area_element is not None:
                if area_element.find('a') is not None:
                    area = area_element.find('a').attrs['title']

            rows = table.find_all('tr')
            
            for row in rows[1:]:
                
                columns = row.find_all("td")
                if len(columns) >= 3:
                    days = columns[0].text.strip().split('/')
                    books = columns[1].find('a').attrs['title']
                    images = [self.find_image(im) for im in columns[1].find_all('div',{'class': 'card_image'})]
                    characters_list = [im.find('a').attrs['title'].strip() for im in columns[-1].find_all('div',{'class': 'card_image'})]

                    if type_key == 'weapon_ascension_materials':
                        characters_list = []
                        for im in columns[-1].find_all('div',{'class': 'card_container'}):
                            if im.attrs['class'][1] in ['card_4','card_5']:
                                characters_list.append(im.find('a').attrs['title'])
                    
                    save_data.append(
                        {   'nation': nation,
                            'area': area,
                            'days': days,
                            'books': books,
                            'images': images,
                            'characters': characters_list,
                            'type': type_key


                        }
                    )
        return save_data



    def create_image(self, images_list ):
        '''
        creates a single image of all items of book series etc
        '''
        
        with open('template_image.json','r') as f:
            template =  json.load(f)
        new = Image.new(mode='RGBA',size=(template['dimensions']['width'],template['dimensions']['height']))
        images = {}
        for c, i in enumerate(images_list,1):
            images[str(c)] = i
        
        for image in images:
            url = images[image]
            x_pos = template[image]['x']
            y_pos = template[image]['y']
            r = requests.get(url).content        
            paste_ = Image.open(BytesIO(r))
            new.paste(paste_, (x_pos,y_pos))
        buffer = BytesIO()
        new.save(buffer,format='PNG')
        buffer.seek(0)
        return buffer

    def search_for_domain(self, data, type, nation, day):
        '''
        ---
        args
        ---
        data: domain data
        type: weapon_ascension_materials or talent_levelup_materials
        nation: mondstadt, liyue or inazuma
        day: tuesday etc
        '''
        if type in data:
            search_dict = data[type]
            for domain_ in search_dict:
                if nation.lower() in domain_['nation'].lower():
                    if day.lower() in [da.lower() for da in domain_['days']]:
                        return domain_



