from base.resource_manager import ResourceManager
from random import choice
from  json import load,dump

from PIL import Image, ImageDraw, ImageFont

res_handler = ResourceManager()



char_images = {}
def random_bg():
    
    bgs = res_handler.goto("images/bgs").get("files")

    return res_handler.genpath('images/bgs', choice(bgs))

def create_teamcomp_image(comp_title, chars):
    main_bg = Image.open(random_bg(),'r').convert('RGBA')
    font_path = res_handler.genpath('misc', 'font.otf')
    title = comp_title
    test_font = ImageFont.truetype(font_path,size=105)
    ImageDraw.Draw(main_bg).text((main_bg.size[0]-test_font.getsize(title)[0]-30, 10), title,fill=(255,255,255,255), font=test_font)
    chars = chars
    start_w = main_bg.size[0] - (301*4)

    role_font = ImageFont.truetype(font_path,size=30)
    for char in chars:
        char_key = list(char.keys())[0]
        role = char[char_key]
        char_image = res_handler.search(char_key, res_handler.goto("images/thumbnails").get('files'))

        
        
        if char_image is not None:
            char_image = res_handler.genpath('images/thumbnails', char_image)
            img = Image.open(char_image,'r').convert('RGBA')
            main_bg.paste(img, (start_w, main_bg.size[1]-256), img)
            ImageDraw.Draw(main_bg).text((start_w+(role_font.getsize(role)[0]//2)+ 10, main_bg.size[1]-256-40), role, fill=(255,255,255,255), font=role_font)
            start_w += 301
    
    file_name = comp_title.lower().replace(' ','_',99999).replace('-','',99)+'.png'
    print('filename', file_name)
    path = res_handler.genpath('images/teamcomps' ,file_name)
    main_bg.save(path,format='PNG')
    return file_name

DATA_FILE = res_handler.db.format(path='teamcomp.json')

with open(DATA_FILE, 'r') as f:
    data = load(f)


for tc in data:
    file = create_teamcomp_image(tc['title'], tc['chars'])
    print('generated', file)
    tc['file'] = file

with open(DATA_FILE, 'w') as f:
    dump(data, f, indent=1)