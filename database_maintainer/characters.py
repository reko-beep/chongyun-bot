from typing import ItemsView
import requests
from main import Fetcher
from bs4 import BeautifulSoup
from json import dump
from logger import logc
from time import sleep

class Characters(Fetcher):
    def __init__(self):
        super().__init__()

    def fetch_lists(self, type: str = 'Characters/List'):
        list = []
        info = []
        data = self.get(f'{type}').content
        bs = BeautifulSoup(data,'lxml')
        table_element = [table.find_next_sibling() for table in bs.find_all('p') if 'characters match' in table.text.lower()]
        for t_e in table_element:
            rows = t_e.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                check = (len(columns) >= 2)
                if check:
                    thumbnail = self.find_image(columns[0].find('img'))
                    nation = columns[5].text.strip()
                    element = columns[3].text.strip()
                    if columns[2].find('img') is not None:
                        rarity = int(columns[2].find('img').attrs['alt'][0])
                    rarity = 0
                    weapon = columns[4].text.strip()
                    link = columns[1].find('a')
                    info.append({
                        'thumbnail': thumbnail,
                        'nation' : nation,
                        'element': element,
                        'rarity': rarity,
                        'weapon': weapon
                    })

                    if link:
                        link = link.attrs['href'].split('/')[-1]
                        if link not in list:
                            list.append(link)
        logc(f'fetched lists for characters {type}')        
        return list, info


    def fetch_info(self, bs : BeautifulSoup):
        list = []        
        table_element = [table.find_next_sibling() for table in bs.find_all('p') if 'characters match' in table.text.lower()]
        for t_e in table_element:
            rows = t_e.find_all('tr')
            for row in rows[1:]:
                columns = row.find_all('td')
                check = (len(columns) >= 7)
                if check:
                    thumbnail = self.find_image(columns[0].find('img'))
                    nation = columns[6].text.strip()
                    element = columns[3].text.strip()
                    if columns[2].find('img') is not None:
                        rarity = int(columns[2].find('img').attrs['alt'][0])
                    rarity = 0
                    weapon = columns[4].text.strip()
                    list.append({
                        'thumbnail': thumbnail,
                        'nation' : nation,
                        'element': element,
                        'rarity': rarity,
                        'weapon': weapon
                    })
        print(list)
        return list




    def fetch(self, arg):
        src = self.get(arg).content
        bs = BeautifulSoup(src,'lxml')
        character_name = arg.replace('_',' ',1).title()
        datasources = [{'div':'image'},{'td':'element'},{'td':'weapon'},{'div':'sex'},{'td':'rarity'},{'div':'series'},{'div':'constellation'},{'div':'birthday'},{'div':'region'},{'div':'affiliation'},{'div':'releaseDate'},{'div':'dish'},{'div':'parents'},{'div':'obtain'},{'div':'siblings'},{'div':'ancestry'}]
        character_dict = {}
        logc(f'fetching info for {character_name}')
        for ds in datasources:
            tag_name = list(ds.keys())[0]
            data_source = ds[tag_name]

            #   scraping image, 
            #   type, how to obtain, 
            #   rarity, series, 

            element = bs.find(tag_name, {'data-source': data_source})
            
            replace_text = ''
            text_value = ''
            if element is not None:
                if data_source == 'rarity':
                    if element.find('img') != None:
                        text_value = int(element.find('img').attrs['alt'][:1].strip())
                else:
                    if data_source == 'image':
                        figures = element.find_all('img')
                        text_value = []
                        for figure in figures:
                            if 'src' in figure.attrs:
                                if figure.attrs['src'].startswith('http'):
                                    text_value.append(figure.attrs['src'][:figure.attrs['src'].find('/revision')])
                                else:
                                    if 'data-src' in figure.attrs:
                                        text_value.append(figure.attrs['data-src'][:figure.attrs['data-src'].find('/revision')])
                    else:
                        if data_source in ['affiliation','parents','ancestry','constellation']:
                            text_value = []
                            text_value = [affil.text.strip() for affil in element.find_all('a')]
                        else:
                            if data_source == 'obtain':
                                text_value = []
                                text_value = [constil.text.strip() for constil in element.find_all('a') if constil.text.strip().lower() != 'how to obtain']

                            else:
                                if element.find('h3') != None:
                                    replace_text = element.find('h3').text                            
                                text_value = element.text.replace(replace_text,'',1).strip()
                character_dict[data_source] = text_value

        #constellation
        constellation_dict = {}

        constellation_table = bs.find('span',{'id':'Constellation'})
        if constellation_table is not None:
            constellation_table = constellation_table.parent.find_next_sibling()
        
        
        if constellation_table is not None:
            rows = constellation_table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if (len(columns) >=4):
                    icon = self.find_image(columns[1])
                    level = columns[0].text.strip()
                    name = columns[2].text.strip()
                    effect = columns[3].text.strip()
                    constellation_dict[str(level)] = {
                        'name' : name,
                        'effect': effect,
                        'icon': icon
                    }
        character_dict['constellations'] = constellation_dict

        talent_table = bs.find('span',{'id':'Talents'})
        if talent_table is not None:
            talent_table = talent_table.parent.find_next_sibling()
        talent_list = []
        if talent_table is not None:
            talent_list = []
            rows = talent_table.find_all('tr')
            for row in rows[1:]:
                if row.find('td',{'colspan': '3'}) is not None:
                    pass
                else:
                    image = row.find('td', {'style': 'width: 45px'})
                    if image is not None:
                        image = self.find_image(image)
                    else:
                        image = ''
                    columns = row.find_all('td', {'style': 'width: 50%'})

                    if (len(columns) >= 2):
                        talent_list.append( {
                            'icon': image,
                            'name': columns[0].text.strip(),
                            'type': columns[1].text.strip()
                            })


        character_dict['talents'] = talent_list
        




        #ascensions

        ascension_table = bs.find('span',{'id':'Ascensions_and_Stats'})
        if ascension_table is not None:
            ascension_table = ascension_table.parent.find_next_sibling()
        else:
            ascension_table = bs.find('span',{'id':'Ascensions'})
            if ascension_table is not None:
                ascension_table = ascension_table.parent.find_next_sibling()
        
        if ascension_table is not None:
            ascension_elements = ascension_table.find_all('td', {'colspan': '6'})
            ascension_dict = {}

            for as_e in ascension_elements:
                text_to_replace = as_e.find('span').text
                bold_to_replace = as_e.find('b').text
                level = as_e.text.replace(text_to_replace,'',1).replace(bold_to_replace,'',1).strip()[-2]
                items_list = []
                items = as_e.find_all('div',{'class': 'card_container'})
                for item in items:
                    title = item.find('a').attrs['title']
                    amount = item.find('div',{'class': 'card_text'}).text
                    items_list.append({'name': title, 'amount': amount})
                
                ascension_dict[level] = items_list
            character_dict['ascension'] = ascension_dict

        sleep(2)

        # scraping 
        # description
        src = self.get(arg+'/Lore').content
        bs = BeautifulSoup(src,'lxml')
        quote = bs.find('blockquote')
        if quote is not None:
            character_dict['description'] = quote.text.strip()
        logc(f'fetched info for {character_name}')
        
        return  character_dict, character_name  
        


