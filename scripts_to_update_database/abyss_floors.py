from requests import get
from bs4 import BeautifulSoup
from json import load, dump
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from os import getcwd, mkdir
from os.path import exists
MAIN_URL = 'https://genshin-impact.fandom.com/wiki/Spiral_Abyss/Floors'
font = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', 25)
def last_abyss_rotation():

    with get(MAIN_URL) as f:
        src = f.content
        bs = BeautifulSoup(src, 'lxml')
        span = bs.find('span', {'id': 'Past'})
        table = None
        for ele in span.parent.find_next_siblings():
            if ele.name == 'table':
                table = ele
        
        if table is not None:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all("td")
                if len(columns) > 0 and columns[0].find("a") != None:
                    return 'https://genshin-impact.fandom.com/'+columns[0].find('a').attrs['href']


def scrape_li_ul(ul_text):
    dict_ = {}
    bs = BeautifulSoup(ul_text, 'lxml')
    lis = bs.find_all('li')
    acceptable_dicts = ['Challenge Target', 'Enemy Level', 'Ley Line Disorder', 'Additional Effects']
    lis_text = []
    for li in lis:
        if li.find("b") is not None:
            main_key = li.find("b").text.strip().replace(":","",99)
            dict_[main_key] = {

            }
            uls  = li.find_all("ul")
            if len(uls) > 0:    
                for ul in uls:                
                    text = str(ul)
                    dict_[main_key] = scrape_li_ul(text)
                    
            else:
                images = li.find_all('div', {'class': 'card_image'})
                if len(images) > 0:
                    if type(dict_[main_key]) != str:
                        dict_[main_key]['enemies'] = []
                        for enem in images:
                            img = ''
                            if enem.find("img").attrs['src'].startswith('http'):
                                img = enem.find("img").attrs['src'][:enem.find("img").attrs['src'].find('/revision')]
                            else:
                                img = enem.find("img").attrs['data-src'][:enem.find("img").attrs['data-src'].find('/revision')]
                            if enem.find("img") is not None:
                                dict_[main_key]['enemies'].append(
                                    {
                                        'name': enem.find("a").attrs['title'],
                                        'img' : img,
                                        'amount': enem.parent.find('div', {'class': 'card_text'}).text

                                    }
                                )
                    else:
                        dict_['enemies'] = []
                        for enem in images:
                            img = ''
                            if enem.find("img").attrs['src'].startswith('http'):
                                img = enem.find("img").attrs['src'][:enem.find("img").attrs['src'].find('/revision')]
                            else:
                                img = enem.find("img").attrs['data-src'][:enem.find("img").attrs['data-src'].find('/revision')]
                            if enem.find("img") is not None:
                                dict_['enemies'].append(
                                    {
                                        'name': enem.find("a").attrs['title'],
                                        'img' : img,
                                        'amount': enem.parent.find('div', {'class': 'card_text'}).text

                                    }
                                )
                else:
                    if main_key in acceptable_dicts:
                        dict_[main_key] = li.text.replace(main_key, "",99).strip()
                    else:

                        if li.find('ul') is None:
                            lis_text.append(li.text)


    final_dict = {**dict_, **{'text': lis_text}}
    corrected_dict = {}
    for key in final_dict:
        if type(final_dict[key]) == dict or type(final_dict[key]) == list:
            if len(final_dict[key]) == 0:
                pass
            else:
                corrected_dict[key] = final_dict[key]
        else:          
        
            corrected_dict[key] = final_dict[key]

    return corrected_dict

def get_abyss_content():
    url = 'https://genshin-impact.fandom.com/wiki/Spiral_Abyss/Floors'
    with get(url) as r:
        src = r.content
        bs = BeautifulSoup(src, 'lxml')
        main_dict = {

        }
        floors = [1,2,3,4,5,6,7,8,9,10,11,12]
        allowed_main_keys = ['Ley Line Disorder','Additional Effects', 'Chamber']
        for floor in floors:
            main_dict[f"floor_{floor}"] = {}
            floor_ele = bs.find("span", {'id': f'Floor_{floor}'})
            print(floor_ele)
            if floor_ele is not None:
                for e in floor_ele.parent.find_next_siblings():
                    if e.name != 'h3':
                        text = str(e) if e.name == 'ul' else ''
                        print(text)
                        if text != '':
                            dict_ = scrape_li_ul(text)
                            main_dict[f"floor_{floor}"] = {**main_dict[f"floor_{floor}"],
                                                            **dict_}
                    else:
                        break
        corrected_dict = {

        }
        for main_key in main_dict:
            corrected_dict[main_key] = {

            }
            for sub_keys in main_dict[main_key]:
                for ak in allowed_main_keys:
                    if ak in sub_keys:
                        corrected_dict[main_key][sub_keys] = main_dict[main_key][sub_keys]

        
        with open("abyss.json", 'w') as f:
            dump(corrected_dict, f, indent=1)

def get_url_image(image_url):

    with get(image_url) as f:
        return Image.open(BytesIO(f.content)).convert("RGBA")

def create_abyss_image(images_list, text_list):
    max_images_width = 4
    max_rows = 3

    new = Image.open(getcwd()+'/assets/misc/abyssbg.png', 'r').convert("RGBA")

    start_x = 40
    start_y = 30
    row_count = 0
    fixed_count = 0
    for i_count in range(1, len(images_list)+1, 1):

        img = get_url_image(images_list[i_count-1])
        new.paste(img , (start_x+ (((i_count-1)- (row_count*max_images_width))*550 + 30), (start_y + (row_count*300))), img)
        ImageDraw.Draw(new).text(((((i_count-1)- (row_count*max_images_width))*560 + 30), (start_y + (row_count*300)+ 258)),text_list[i_count-1], font=font, fill=(255,255,255))
        if i_count >= max_images_width*(row_count+1):
            row_count += 1

    return new


def create_abyss_images():
    with open('abyss.json', 'r') as f:
        data = load(f)

    path = getcwd()+'/abyss/{floor}/{chamber}/{half}.png'
    path_check = getcwd()+"/abyss/"
    chamber_key = 'Chamber {number}'
    for floor in data:
        for i in range(1, 4, 1):
            if not exists(path_check+'/'+floor):
                mkdir(path_check+'/'+floor)
            if not exists(path_check+'/'+floor+'/'+chamber_key.format(number=i).replace(" ","_",99).lower()):
                mkdir(path_check+'/'+floor+'/'+chamber_key.format(number=i).replace(" ","_",99).lower())
            if chamber_key.format(number=i) in data[floor]:
                
                halves = data[floor][chamber_key.format(number=i)]
                if 'First Half' in halves:
                    images = [i['img'] for i in halves['First Half']['enemies']]
                    text = [i['name'][:50]+'..' for i in halves['First Half']['enemies']]
                    img = create_abyss_image(images, text)
                    
                    print('created image', path.format(floor=floor,chamber=chamber_key.format(number=i).replace(" ","_",99).lower(),half='first_half'))
                   
                    img.save(path.format(floor=floor,chamber=chamber_key.format(number=i).replace(" ","_",99).lower(),half='first_half'))
                if 'Second Half' in halves:
                    images = [i['img'] for i in halves['Second Half']['enemies']]
                    text = [i['name'][:40]+'..' for i in halves['Second Half']['enemies']]
                    img = create_abyss_image(images, text)
                    img.save(path.format(floor=floor,chamber=chamber_key.format(number=i).replace(" ","_",99).lower(), half='second_half'))
                    
                    print('created image', path.format(floor=floor,chamber=chamber_key.format(number=i).replace(" ","_",99).lower(),half='second_half'))


get_abyss_content()
create_abyss_images()
