
import requests
from main import Fetcher
from bs4 import BeautifulSoup
import json
from logger import logc
from time import sleep

class Artifacts(Fetcher):
    def __init__(self):
        super().__init__()

    def fetch_lists(self, type: str = 'Artifacts/Sets'):
        list = []
        data = self.get(f'{type}').content
        bs = BeautifulSoup(data,'lxml')
        table_element = [table.find_next_sibling() for table in bs.find_all('p') if 'artifact sets' in table.text.lower()][1]     
        rows = table_element.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            check = (len(columns) >= 4)
            if check:
                link = columns[0].find('a')
                if link:
                    link = link.attrs['href'].split('/')[-1]
                    if link not in list:
                        list.append(link)
        logc(f'fetched lists for artifacts {type}')
        return list






    def fetch(self, arg):
        src = self.get(arg).content
        bs = BeautifulSoup(src,'lxml')
        name = arg.replace('_',' ',99).replace('%22','',9).replace('%27','', 99).title()
        datasources = [{'div':'flower'},{'div':'plume'},{'div':'sands'},{'div':'goblet'},{'div':'circlet'}]
        artifacts_dict = {}
        logc(f'fetching info for {name}')
        sets = []
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
                if data_source in ['circlet','plume','flower','sands','goblet']:
                    figure = element.find('img')
                    img = ''
                    if 'src' in figure.attrs:
                        if figure.attrs['src'].startswith('http'):
                            img = figure.attrs['src']
                        else:
                            if 'data-src' in figure.attrs:
                                img = figure.attrs['data-src'] 
                    value = element.find('div', {'class':'pi-data-value'}) 
                    # piece lore
                    for i in bs.find_all('h3'):
                        if value.text.replace(value.find('b').text,'',1).lower() in  i.text.lower():
                            siblings = i.find_next_siblings()
                            for sibling in siblings:
                                if sibling.name == 'p':
                                    description = sibling.text
                                    break
                    
                    if value.find('b') != None:
                        sets.append({'type': value.find('b').text.strip(), 'name': value.text.replace(value.find('b').text,'',1),'img': img, 'description': description})                            
                else:  
                    if element.find('h3') != None:
                        replace_text = element.find('h3').text                            
                    text_value = element.text.replace(replace_text,'',1).strip()
                    artifacts_dict[data_source] = text_value
        artifacts_dict['pieces'] = sets
        bonuses_dict = {}
        pieces = ['2','4']
        data_source = '{pc}pcBonus'
        for piece in pieces:
            element = bs.find('div',{'data-source': data_source.format(pc=piece)})
            if element is not None:
                value = element.find('div')
                if value is not None:
                    bonuses_dict[piece] = value.text.strip()
        artifacts_dict['bonus'] = bonuses_dict

        stars = ['1','2','3','4','5']
        rarity = []
        source_class = 'source{star}.{source}'
        obtain_dict = {}
        for star in stars:
            check = bs.find('div',{'data-source': source_class.format(star=star,source=1)})
            source_dict = {}
            if check is not None:
                sources_range = list(range(1,10,1))
                for source in sources_range:
                    element = bs.find('div',{'data-source': source_class.format(star=star,source=source)})
                    if element is not None:
                        if element.find('div',{'class': 'pi-data-value'}) is not None:
                            values_div = element.find('div',{'class': 'pi-data-value'})
                            if len(values_div.find_all('a')) != 0:
                                source_dict[str(source)] = [source_value.text.strip() for source_value in values_div.find_all('a')]
                obtain_dict[star] = source_dict
                rarity.append(int(star))
            
        artifacts_dict['obtain'] = obtain_dict
        artifacts_dict['rarity'] = rarity
        logc(f'fetched info for {name}')
        return artifacts_dict, name
        


