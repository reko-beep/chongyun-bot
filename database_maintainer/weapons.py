from typing import ItemsView
import requests
from main import Fetcher
from bs4 import BeautifulSoup
import json
from logger import logc
from time import sleep

class Weapons(Fetcher):
    def __init__(self):
        self.types = ['Swords','Bows','Claymores','Polearms','Catalysts']
        super().__init__()

    def fetch_lists(self, type):
        list = []
        if type in self.types:
            data = self.get(f'{type}').content
            bs = BeautifulSoup(data,'lxml')
            table_element = [table.find_next_sibling() for table in bs.find_all('p') if 'weapons match' in table.text][0]
            rows = table_element.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                check = (len(columns) >= 2)
                if check:
                    link = columns[1].find('a')
                    if link:
                        list.append(link.attrs['href'].split('/')[-1])
            logc(f'fetched lists for weapon type {type}')
            return list






    def fetch(self, arg):
        src = self.get(arg).content
        bs = BeautifulSoup(src,'lxml')
        name = arg.replace('%27','',99).replace('%22','',99).replace('_',' ',99).title()
        datasources = [{'div':'image'},{'div':'type'},{'div':'obtain'},{'div':'rarity'},{'div':'series'}]
        weapon_dict = {}
        logc(f'fetching info for {name}')
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
                                    text_value.append(figure.attrs['src'])
                                else:
                                    if 'data-src' in figure.attrs:
                                        text_value.append(figure.attrs['data-src'])
                    else:
                        if element.find('h3') != None:
                            replace_text = element.find('h3').text                            
                        text_value = element.text.replace(replace_text,'',1).strip()
                weapon_dict[data_source] = text_value
            
        # scraping 
        # weapon 
        # stats
     

        stat_element = [element.find_next_sibling() for element in bs.find_all('h2') if 'Base Stats' in element.text][0]
        if stat_element is not None:
            stat_head_element = bs.find('section', {'class': 'pi-smart-group-head'}).find_all('h3')
            stat_body_element = bs.find('section', {'class': 'pi-smart-group-body'}).find_all('div')
            stat_dict = {}
            print(len(stat_head_element),len(stat_body_element))
            for index in range(len(stat_head_element)):
                if index != len(stat_body_element):
                    stat_dict[stat_head_element[index].text] = stat_body_element[index].text

            weapon_dict['stats'] = stat_dict
        refinement_class = 'eff_rank{rank}_var1'

        refinement_dict = {}
        check = bs.find('td', {'data-source': refinement_class.format(rank=1)})
        ranks = [1,2,3,4,5]
        if check is not None:
            for rank in ranks:
                rank_element = bs.find('td', {'data-source': refinement_class.format(rank=rank)})
                text_ = rank_element.text 
                
                # modular text
                bolded_text = rank_element.find_all('b')
                value_dict = {}
                for b in range(len(bolded_text)):
                    text_ = text_.replace(bolded_text[b].text,f'-value{b}-',1)
                    value_dict[f'-value{b}-'] = bolded_text[b].text

                if 'text' not in refinement_dict:
                    refinement_dict['text'] = text_
                refinement_dict[str(rank)] = value_dict
            weapon_dict['refinement'] = refinement_dict

        #ascensions

        ascension_table = [element.find_next_sibling() for element in bs.find_all('h2') if 'Ascensions and Stats' in element.text]
        if len(ascension_table) >= 1:
            ascension_table = ascension_table[0]
        else:
            ascension_table = None
        if ascension_table is not None:
            ascension_elements = ascension_table.find_all('td', {'colspan': '4'})
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
            weapon_dict['ascension'] = ascension_dict
        logc(f'fetched info for {name}')
        return name,weapon_dict
        




