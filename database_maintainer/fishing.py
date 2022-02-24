from io import BytesIO
import requests

from bs4 import BeautifulSoup
from json import dump, load
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from os import getcwd, mkdir

from os.path import exists
from time import sleep

path = getcwd()
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

def fetch_fishing_points():   

    url = 'https://genshin-impact.fandom.com/wiki/Fishing/Fishing_Points'

    src = requests.get(url).content

    bs = BeautifulSoup(src, 'lxml')

    cities = ['Mondstadt', 'Liyue', 'Inazuma', 'Enkanomiya']
    data = {}
    for city in cities:
        table = None
        list_ = []
        table_main = bs.find('span', {'id': city})
        if table_main is not None:
            table = table_main.parent.find_next_sibling()
        
        if table is not None:

            rows = table.find_all('tr')[1:]

            for row in rows:

                columns = row.find_all('td')

                if len(columns) >= 2:

                    location = columns[0].find('b').text.strip()
                    desc = columns[0].text.replace(location, '', 1).strip()
                    location_img = find_image(columns[1])
                    fish_loc = []
                    fishes = columns[2].find_all('div', {'class' : 'card_container'})

                    for fish in fishes:

                        icon = ''
                        title = ''
                        image = ''

                        icon_e = fish.find('div', {'class': 'card_icon'})

                        if icon_e is not None:

                            icon = find_image(icon_e)
                        
                        main_e = fish.find('div', {'class': 'card_image'})
                        
                        if main_e is not None:

                            sub_e = main_e.find("a")

                            if sub_e is not None:

                                title = sub_e.attrs['title']

                                image = find_image(sub_e)
                    
                        fish_loc.append({
                            'name' : title,
                            'bait': icon,
                            'image' : image
                        })

                list_.append( {
                    'location' : location,
                    'description' : desc,
                    'image' : location_img,
                    'fishes' : fish_loc
                })
            
            data[city] = list_


    with open("fishing.json", 'w') as f:
        dump(data, f ,indent=1)

data = {}
with open('fishing.json', 'r') as f:
    data = load(f)

def resize_image(image, to_size: tuple):
    width, height = image.size
    width_to, height_to = to_size
    calculated_size = image.size
    if width_to == 0:
        ratio = height_to/height
        calculated_size = (int(float(width) * float(ratio)),height_to )

    if height_to == 0:
        ratio = width_to/width     
        calculated_size = (width_to, int(float(height) * float(ratio)))

    image_resized = image.resize(calculated_size)

    return image_resized

def create_card(bait_url, fish_url, text):
    main_card = Image.new('RGBA', (230,230))
    card_image = Image.open(path +'/fish_card.png','r')

    r = requests.get(fish_url).content

    img = Image.open(BytesIO(r), 'r')
    fish_size = (0,150)
    fish_image = resize_image(img, fish_size)

    r = requests.get(bait_url).content

    img = Image.open(BytesIO(r), 'r')
    bait_size = (0,65)
    bait_image = resize_image(img, bait_size)    

    

    font = ImageFont.truetype(path + '/font.ttf', 20)

    if font.getsize(text)[0] > 220:
        text = text[:len(text) - (font.getsize(text)[0]-220)]  +'..'  


    main_card.paste(card_image, (15,15), card_image)
    main_card.paste(fish_image, (main_card.size[0]- fish_image.size[0]-5,30), fish_image)
    main_card.paste(bait_image, (-5,-5), bait_image)
    draw = ImageDraw.Draw(main_card)

    draw.text((27, 205), text, fill=(43,43,43,255), font=font)

    return main_card

def horizontally_fade_image(image, start_height_percent, end_height_percent):
    start_perc = start_height_percent/100
    end_perc = end_height_percent/100
    width, height = image.size
    pixels = image.load()
    for x in range(int(width*start_perc), int(width*end_perc)):
        for y in range(height):
            alpha = pixels[x, y][3]-int((x - width*start_perc)/width/.20 * 255)
            if alpha <= 0:
                alpha = 0            
            pixels[x, y] = pixels[x, y][:3] + (alpha,)
    for x in range(x, width):
        for y in range(height):
            pixels[x, y] = pixels[x, y][:3] + (0,)

def vertically_fade_image(image, start_height_percent, end_height_percent):
    start_perc = start_height_percent/100
    end_perc = end_height_percent/100
    width, height = image.size
    pixels = image.load()
    for y in range(int(height*start_perc), int(height*end_perc)):
        for x in range(width):
            print(pixels[x, y])
            alpha = pixels[x, y][3]-int((y - height*start_perc)/height/.20 * 255)
            if alpha <= 0:
                alpha = 0            
            pixels[x, y] = pixels[x, y][:3] + (alpha,)
    for y in range(y, height):
        for x in range(width):
            pixels[x, y] = pixels[x, y][:3] + (0,)


def create_map(map_url, text):

    r = requests.get(map_url).content

    img = Image.open(BytesIO(r), 'r').convert('RGBA')
    height = 1080-44
    img = resize_image(img, (0,height))
    to_fade = img.transpose(0)
    horizontally_fade_image(to_fade, 75, 100)
    final_image= to_fade.transpose(0)

    enhancer = ImageEnhance.Sharpness(final_image)
    final_image = enhancer.enhance(1.5)

    

    font = ImageFont.truetype(path + '/bold.ttf', 65)

    draw = ImageDraw.Draw(final_image)

    correction = 0
    
    if (img.width - font.getsize(text)[0] + correction) < 310:
        correction = 125



    # Create piece of canvas to draw text on and blur
    blurred = Image.new('RGBA', final_image.size)
    draw = ImageDraw.Draw(blurred)
    draw.text(xy=(img.width- font.getsize(text)[0] + correction, img.height-75), text=text, fill='yellow', font=font, anchor='mm')
    blurred = blurred.filter(ImageFilter.BoxBlur(7))

    # Paste soft text onto background
    final_image.paste(blurred,blurred)

    # Draw on sharp text
    draw = ImageDraw.Draw(final_image)
    draw.text(xy=(img.width - font.getsize(text)[0]+ correction, img.height-75), text=text, fill='white', font=font, anchor='mm')
   

    final_image.show()

    return final_image

def generate_key(string: str):
        seps = ['-','~','`',':',".","/",".", '_', ' ']
        for sep in seps:
            string = string.replace(sep,'_',99)
        string = string.replace('__','_',1).replace('_s_','_s',9).lower()
        return string

def create_fishing_images():
    last = ''
    count = 0
    
    
    for city in data:

        if not exists(getcwd()+ '/'+ city):
            mkdir(getcwd()+ '/'+ city)
    
  

        for fishpoint in data[city]:

            main = fishpoint
            bs = Image.open(path+ '/fishbg.png', 'r') 
            print(main['image'], main['location'])
            map_ = create_map(main['image'], main['location'])
            post = ((bs.size[0]-map_.size[0])-23, (bs.size[1]-map_.size[1])-22)
            bs.paste(map_, post, map_)

            fishes = main['fishes']
            x_start = 45
            y_start = 132
            split_line = 3
            rc = 1
            for fish in fishes:

                if fishes.index(fish) >= split_line* rc:
                    y_start += 235
                    x_start = 45
                    rc += 1

                check = create_card(fish['bait'], fish['image'], fish['name'])
                bs.paste(check, (x_start, y_start), check)
                x_start += 235
            

            if not exists(getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +'.png'):
                if  getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +'.png' != last:
                    bs.save(getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +'.png')
                    data[city][data[city].index(fishpoint)]['file'] = generate_key(main['location']) +'.png'
                    last = getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +'.png'
                    count = 0
                else:
                    count += 1
                    bs.save(getcwd()+ '/'+ city + '/' + generate_key(main['location']) +f'_{count}.png')
                    data[city][data[city].index(fishpoint)]['file'] = generate_key(main['location']) +f'_{count}.png'
                    last = getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +f'_{count}.png'

            else:
                count += 1
                bs.save(getcwd()+ '/'+ city + '/' + generate_key(main['location']) +f'_{count}.png')
                data[city][data[city].index(fishpoint)]['file'] = generate_key(main['location']) +f'_{count}.png'
                last = getcwd()+ '/'+ city +'/' +  generate_key(main['location']) +f'_{count}.png'

            sleep(2)

    with open('fishing_final.json', 'w') as f:
        dump(data, f, indent=1)
                


  

create_fishing_images()
