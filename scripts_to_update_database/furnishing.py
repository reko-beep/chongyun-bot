from tkinter import Image
from requests import get
from bs4 import BeautifulSoup
from json import dump, load
from PIL import Image, ImageDraw, ImageFont
from os import getcwd
from io import BytesIO
from base.resource_manager import ResourceManager

rm = ResourceManager()

DATA_PATH = rm.genpath('data')
IMAGES_PATH = rm.genpath('images/furnishing')


MAIN_URL = 'https://genshin-impact.fandom.com/wiki/Serenitea_Pot/Sets'

def find_image(img):
    if img.attrs['src'].startswith('http'):
        return img.attrs['src'][:img.attrs['src'].find('/revision')]
    else:
        return img.attrs['data-src'][:img.attrs['data-src'].find('/revision')]

src = get(MAIN_URL).content

bs = BeautifulSoup(src, 'lxml')
table = bs.find_all('table')[2]

data = []
rows = table.find_all('tr')[1:]

for r in rows:
    columns = r.find_all("td")
    print(len(columns))
    if len(columns) == 7:

        data.append(
            {
                'img': find_image(columns[0].find('img')),
                'link': columns[0].find('a').attrs['href'],
                'title': columns[1].text.strip(),
                'rarity': int(columns[2].find('img').attrs['alt'][0]),
                'adeptal_energy': columns[3].text.strip(),
                'load': columns[4].text.strip(),
                'category': columns[5].text.strip(),
                'chars': [a.text for a in columns[6].find_all('a')]
            }
        )


def get_further_contents(dict_):
    link = dict_['link']
    src = get('https://genshin-impact.fandom.com/'+link).content
    bs = BeautifulSoup(src, 'lxml')

    further = {

    }

    bp = bs.find('div', {'data-source': 'blueprint'})
    if bp is not None:
        if bp.find('h3') is not None:
            further['blueprint'] = bp.text.replace(bp.find('h3').text, '', 1).strip()
    
    ds = bs.find("div", {'data-source': "description"})
    if ds is not None:
        further['description'] = ds.find("div").text.strip()

    gftsts = bs.find("div",{'class':'new_genshin_recipe_body'})
    print("getting more data for", dict_['title'])
   
    items = []

    if gftsts is not None:
        item_temp = gftsts.find_all("div", {'class': 'card_with_caption'})
        for itm in item_temp:
            title,amount,img = '','',''
            if itm.find("div",{'class': 'card_image'}) is not None:
                img = find_image(itm.find("div",{'class': 'card_image'}).find("img"))
            if itm.find("div",{'class': 'card_text'}) is not None:
                amount = itm.find("div",{'class': 'card_text'}).text
            if itm.find('div', {'class':'card_caption'})  is not None:
                title = itm.find('div', {'class':'card_caption'}).text.strip()

            items.append({
                'img': img,
                'amount': amount,
                'title': title
            })

    further['gift_sets'] = items
    return {**dict_, **further}


save = {'data': []}

for it in data:
    data_ = get_further_contents(it)
    save['data'].append(data_)

with open(DATA_PATH+"/furnishing.json", 'w') as f:
    dump(save, f, indent=1)



def generate_filename(string):
    seps = [',','.','/',';',':','-','!','`','/"']
    for s in seps:
        string = string.replace(s,'',99)
    return string.lower().replace(" ",'_',99)

def create_image(images_list, text_list, title):
    img = Image.open(getcwd()+'/bg.png', 'r').convert('RGBA')
    page_next = img.copy()
    font_title = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', size=65)
    font_item = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', size=17)
    start_x = 70
    start_y = 180
    max_ = 4
    row_count = 0
    pages = None
    ImageDraw.Draw(img).text((90,90), title, fill=(255,255,255), font=font_title)
    ImageDraw.Draw(page_next).text((90,90), title, fill=(255,255,255), font=font_title)
    for i in range(1, len(images_list)+1, 1):
       
        img_ = Image.open(BytesIO(get(images_list[i-1]).content),'r').convert('RGBA')
        print('row', row_count,'total item', i,'row item', i - (max_*row_count) -1,'x', start_x + (266* (i - (max_*row_count)-1 )))
        if i <= 12:
            
            img.paste(img_, (start_x + (360* (i - (max_*row_count) -1)), start_y + (row_count * 266)), img_)
            
            ImageDraw.Draw(img).text((start_x + (360* (i - (max_*row_count)-1)), start_y + (row_count * 266)+ 260), text_list[i-1], fill=(255,255,255), font=font_item)
        
        else:
            pages = True            
            print('x', (start_x + (360* (i - (max_*row_count) -1))),'row count', row_count, 'calculated', row_count-3, "y", start_y + ((row_count-3) * 266))
            page_next.paste(img_, (start_x + (360* (i - (max_*row_count) -1)), start_y + ((row_count-3) * 266)), img_)
            ImageDraw.Draw(page_next).text((start_x + (360* (i - (max_*row_count)-1)), start_y + ((row_count-3) * 266)+ 260), text_list[i-1], fill=(255,255,255), font=font_item)
      
        if i == max_+ (max_*row_count):           
            row_count += 1
    if pages:
        return img, page_next
    else:
        return img




with open(DATA_PATH+"/furnishing.json",'r') as f:
    data = load(f)['data']

for im in data:

    gft = im['gift_sets']
    gftt = [i['title'] for i in gft]
    gfti = [i['img'] for i in gft]

    img = create_image(gfti, gftt, im['title'])
    filename = generate_filename(im['title'])
    im['file'] = [filename+'.png']
    if type(img) == tuple:
        im['file'] = []
        for i in range(len(img)):
            img[i].save(getcwd()+'/furnishing/'+filename+f'_{i+1}.png')
            im['file'].append(filename+f'_{i+1}.png')

    else:        
        img.save(IMAGES_PATH+filename+'.png')

with open(DATA_PATH+"/furnishing.json",'w') as f:
    dump({'data': data},f,indent=1)