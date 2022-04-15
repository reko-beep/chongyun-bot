from PIL import Image, ImageDraw, ImageFont
import requests
from os import getcwd
from io import BytesIO
from json import load, dump


def create_image(set,  images_list ):
        font = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', 45)
        with open(f'{getcwd()}/template_image.json','r') as f:
            template =  load(f)
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
        
        ImageDraw.Draw(new).text((460,500), text=set.replace(' ','\n',99), font=font, fill=(255,255,255))
        new.save(getcwd()+'/artifacts/'+set+'.png',format='PNG')
        print('image created for', set)
        
artifacts = {}
with open(getcwd()+'/assets/data/artifacts.json','r') as f:
    artifacts = load(f)


for arti in artifacts:
    images = [i['img'][:i['img'].find('/revision')] for i in artifacts[arti]['pieces']]
    create_image(arti, images)
    artifacts[arti]['file'] = arti+'.png'


with open('artifacts_filed.json', 'w') as f:
    dump(artifacts, f, indent=1)