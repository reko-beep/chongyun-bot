from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from base.resource_manager import ResourceManager
from requests import get
import random
from json import load

from os import getcwd

from aiohttp import request

class ImageGenerator:
    
    def __init__(self, rm: ResourceManager):
        '''
        Initializes Image Generator
        '''
        self.font = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', 25)       
        self.base_width = 256
        self.base_height = 256
        self.rm = rm
        self.font_path = rm.genpath('misc', rm.search('font',rm.goto('misc').get('files')))

    
    def calculate_image_wh(self, images_list : list, vertical: bool = False):
        '''
        calculate image width and height according to images provided
        '''
        w,h = 0,0
        margin_right = 45
        margin_bottom = 55
        for i in range(len(images_list)):
            if vertical:
                h += (self.base_height + margin_bottom)
            else:
                w += (self.base_height + margin_right)
        if w == 0:
            w = self.base_width
        if h == 0:
            h = self.base_height

        return w,h

    def create_blank_image(self, size: tuple, background_path : str= ''):
        '''
        creates a blank image
        '''

        w,h = size
        if background_path != '':
            img = Image.open(background_path, 'r').convert('RGBA')
            return Image.new('RGBA', size).paste(img, (0,0), img)
        else:
            return Image.new('RGBA', size)



    def image_from_url(self, url: str): 
        '''
        generates a PIL Image object from url
        '''
        if url.startswith('http') and url.split('/')[-1].split('.')[-1] in ['png','jpg', 'jpeg']:
            bytes_ = get(url).content
            return Image.open(BytesIO(bytes_), 'r').convert('RGBA')
    
    def create_image(self, images_list: list, text_list: list, to_save: bool = False, **kwargs):
        '''
        creates a image object
        and saves to filename provided in kwarg if to_save is set to true
        '''

        filename = kwargs.get('filename', 'temp.png')
        filepath = kwargs.get('filepath','/assets')

        #   calculates image height
        #   and width from images_list

        w,h = self.calculate_image_wh(images_list)
        image_blank = self.create_blank_image((w,h))

        for img in images_list:
            index_ = images_list.index(img)
            temp_img = self.image_from_url(img)
            img_width, img_height =  temp_img.size
            if temp_img is not None:
                image_blank.paste(temp_img, ((index_ * self.base_width)+ (45 * index_) +15, 17 ), temp_img)
                ImageDraw.Draw(image_blank).text(((index_ * self.base_width)+ (45 * index_)+ img_width+20, 25 ), text_list[index_].replace(' ','\n',10), fill=(255,255,255),font=self.font)

        if to_save:
            image_blank.save(filepath + '/'+ filename)        
        return image_blank

    def find_thumbnail(self, character_name: str):
        loaded_thumbs = self.rm.search(character_name, self.rm.goto('images/thumbnails').get('files'))
        if loaded_thumbs is not None:
            return self.rm.genpath('images/thumbnails',loaded_thumbs)

    def random_bg(self):
        return random.choice([self.rm.genpath('images/bgs',f) for f in self.rm.goto('images/bgs').get('files')])
    
    def create_comp_image(self,comp_title: str, chars_role : list, filename_return: bool = False):
        
        main_bg = Image.open(self.random_bg(),'r').convert('RGBA')

        title = comp_title
        test_font = ImageFont.truetype(self.font_path,size=105)
        ImageDraw.Draw(main_bg).text((main_bg.size[0]-test_font.getsize(title)[0]-30, 10), title,fill=(255,255,255,255), font=test_font)
        
        start_w = main_bg.size[0] - (301*4)

        role_font = ImageFont.truetype(self.font_path,size=30)
        for char in chars_role:
            char_key = list(char.keys())[0]
            role = char[char_key]
            char_image = self.find_thumbnail(char_key)
            if char_image is not None:
                img = Image.open(char_image,'r').convert('RGBA')
                main_bg.paste(img, (start_w, main_bg.size[1]-256), img)
                ImageDraw.Draw(main_bg).text((start_w+(role_font.getsize(role)[0]//2)+ 10, main_bg.size[1]-256-40), role, fill=(255,255,255,255), font=role_font)
                start_w += 301
        base_path = self.rm.genpath('images', 'teamcomps')
        print(base_path)
        key = title
        for i in ['-','_',' ','#',':',".","/","\\","!","`","~",","]:
            key = key.replace(i,'_',99)
        main_bg.save(base_path +'/' + key.lower().replace(' ','_', 99) +'.png',format='PNG')
        if filename_return:
            return key+'.png' 

