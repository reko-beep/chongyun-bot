from numpy import fix
from pip import main
import requests
from bs4 import BeautifulSoup
from time import sleep
from json import dump
ABYSS_CONSTANT = 'https://genshin-impact.fandom.com/wiki/Spiral_Abyss/Floors/Abyss_Corridor'
ABYSS_ROTATION = 'https://genshin-impact.fandom.com/wiki/Spiral_Abyss/Floors/Abyssal_Moon_Spire'

src = requests.get(ABYSS_ROTATION).content

bs = BeautifulSoup(src, 'lxml')


def generate_key(string: str):
        seps = ['-','~','`',':',".","/",".", '%22', '22', '27']
        for sep in seps:
            string = string.replace(sep,'',99)
        string = string.replace('__','_',1).replace('_s_','_s',9).lower()
        return string

def get_between_elements(element, element_tag_second):

    upper_check = element.parent.name
    lists = []
    check = element
    if check is not None:
        while check.name != element_tag_second.name:       
                lists.append(check)
                check.find_next_sibling()

    
    return lists

def find_image(img):
        if img.name != 'img':
            img = img.find('img')
        if img is not None:
            if img.attrs['src'].startswith('http'):
                return (img.attrs['src'][:img.attrs['src'].find('/revision')])
            else:
                if 'data-src' in img.attrs:
                    return (img.attrs['data-src'][:img.attrs['data-src'].find('/revision')])
        return ''



def card_element(card_container):
        image = ''
        amount = ''
        title = ''
        image_element = card_container.find('div', {'class':'card_image'})
        if image_element is not None:
            if image_element.find('a') is not None:
                title = image_element.find('a').attrs['title']
            image = find_image(image_element)
        amount_element = card_container.find('div', {'class': 'card_text'})
        if amount_element is not None:
            amount = amount_element.text.replace(',','',9).strip()
        if title == amount == '':
            return None, None, None
        return title, image, amount

FLOOR_ID_TEMPLATE = 'Floor_{number}'
floor_dict = {}

for i in range(9,12,1):

    mainfloor = bs.find('span', {'id': FLOOR_ID_TEMPLATE.format(number=i)})
    mainelement = None
    if mainfloor is not None:
        mainelement = mainfloor.parent
    
    if mainelement is not None:
        nex = mainelement.find_next_sibling()
        
        floor_dict[FLOOR_ID_TEMPLATE.format(number=i).lower()] = {}
        check = lambda x : x.name == 'ul'

        fixed_elements = []
        while nex.name != 'h3':
            if nex.name == 'ul':
                fixed_elements.append(nex)
            nex = nex.find_next_sibling()


        for ele in fixed_elements:
            if ele.name == 'ul':

                sub_ele = ele.find_all('li', recursive=True)
                for sub_e in sub_ele:
                    if sub_e.find('b') is not None:
                        main_key = sub_e.find('b').text.strip()
                        chamber = False
                        sub_sub_ele = sub_e.find('ul', recursive=True).find_all('li', recursive=True) if sub_e.find('ul') is not None else None
                        sub_obj = {

                        }
                        if 'chamber' in main_key.lower():

                            chamber = True
                            sub_obj[main_key] = {}
                        

                        if sub_sub_ele is not None:

                            
                            for s in sub_sub_ele:

                                if chamber != True:

                                    floor_dict[FLOOR_ID_TEMPLATE.format(number=i).lower()][main_key] = s.text.strip()
                                
                                else:

                                    

                                    s_key = s.find('b').text.strip()

                                    cards_check = s.find_all('div', {'class': 'card_container'})

                                    if len(cards_check) != 0:
                                        cards = [dict(zip(['title','image','amount'], card_element(c))) for c in cards_check]

                                        sub_obj[main_key][s_key] = cards
                                    else:
                                        sub_obj[main_key][s_key] = s.text.replace(s_key,'',1)

                            if chamber == True:

                                floor_dict[FLOOR_ID_TEMPLATE.format(number=i).lower()] = { **floor_dict[FLOOR_ID_TEMPLATE.format(number=i).lower()], **sub_obj}


with open('abyss.json', 'w') as f:
    dump(floor_dict, f, indent=1)



                            




                            


       

                    







    



