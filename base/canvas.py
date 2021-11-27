from os import getcwd,mkdir
from os.path import exists
from bs4 import BeautifulSoup
from html2image import Html2Image
import io

from PIL import ImageFont



class BannerCanvas:
    def __init__(self, uid: int):
        self.path = getcwd()+'/assets/wishes/'
        self.file = f'{self.path}/assests/template.html'
        self.light_font = f'{self.path}/assests/inter.ttf'        
        self.src = ''

        if not exists(f'{self.path}/uids/{uid}/images/'):
            mkdir(f'{self.path}/uids/{uid}/images/')

        self.renderer = Html2Image(custom_flags=['--virtual-time-budget=50000', '--hide-scrollbars'],output_path=f'{self.path}/uids/{uid}/images/')
        self.width = 450
        self.height = 80 #pity + heading height
        self.width_iter = 0
        self.items = 0
        self.uid = uid
        self.__load()
    
    def __load(self):
        if exists(self.file):
            with open(self.file,'r') as f:
                self.src = BeautifulSoup(f.read(),'html.parser')

    def get_pil_text_size(self, text, font_size):
        font = ImageFont.truetype(self.light_font, font_size)
        size = font.getsize(text)
        return size

    def set_heading(self,banner_code: str):
        '''
        Sets banner heading
        '''

        headings = {'100': 'Standard Banner','200': 'Permanent Banner','301': 'Character Banner','302': 'Weapon Banner', '400': 'Character Event Wish-2'}

        
        main_banner = self.src.find('div',{'class':'banner'})
        exists = self.src.find('div',{'class':'heading'})
        if exists:
            exists.string = str(headings[banner_code])
        else:
            heading_tag = self.src.new_tag('div',attrs={'class':'heading'})
            heading_tag.string = headings[banner_code]
            main_banner.append(heading_tag)
        

    def add_pity(self,star: str,pity: int):
        '''
        adds current pity for star
        '''
        pity_tag = self.src.find('div',{'class':'pity-counter'})
        star_tags = {'5':'five-star','4':'four-star'}

        # value
        span_value = self.src.new_tag('span',attrs={'class':'item-value'})
        span_value.string = str(pity)
        value_tag = self.src.new_tag('div',attrs={'class':f'item-circle {star_tags[star]}'})
        value_tag.append(span_value)

        if pity_tag:
            pity_tag.append(value_tag)
        else:
            pity_tag = self.src.new_tag('div',attrs={'class':'pity-counter'})       
            pity_tag.append(value_tag)


    def add_field(self, field_name: str ,field_value: str):
        '''
        adds a field with name having value
        '''
        main_container = self.src.find('div',{'class':'container'})       

        #   Value tags

        span_value = self.src.new_tag('span',attrs={'class':'value'})
        span_value.string = str(field_value)
        value_tag = self.src.new_tag('div',attrs={'class':'value-field'})
        value_tag.append(span_value)

        #   field tags
        field_tag = self.src.new_tag('div',attrs={'class':'field-heading'})
        field_tag.string = str(field_name)

        #main tag
        main_tag = self.src.new_tag('div',attrs={'class':'field'})
        main_tag.append(field_tag)
        main_tag.append(value_tag)
        self.height += 110 # field height

        if main_container:
            main_container.append(main_tag)
        else:
            main_container = self.src.new_tag('div',attrs={'class':'container'})       
            main_container.append(main_tag)

    def add_item(self, star:str, item_name: str ,item_pity: str):
        '''
        adds pulled item pulled at pity item_pity
        '''

        main_container = self.src.find('div',{'class':'item-container'})       
        star_tags = {'5':'five-star','4':'four-star'}
        #   Value tags

        pity_value = self.src.new_tag('span')
        pity_value.string = str(item_pity)
        pity_tag = self.src.new_tag('div',attrs={'class':f'item-circle {star_tags[star]}'})
        pity_tag.append(pity_value)

        #   field tags
        name_tag = self.src.new_tag('span',attrs={'class':'item-value'})
        name_tag.string = str(item_name)

        #main tag
        field_tags = {'5':'five-border','4':'four-border'}
        main_tag = self.src.new_tag('div',attrs={'class':f'item-field {field_tags[star]}'})
        main_tag.append(pity_tag)
        main_tag.append(name_tag)

        if main_container:
            main_container.append(main_tag)
        else:
            main_container = self.src.new_tag('div',attrs={'class':'item-container'})       
            main_container.append(main_tag)
        print(self.width_iter,self.width)
        if self.width_iter > 380: #item containers width
            self.height += 35 #an items row height
            self.width_iter = 0
            print('height added')
        else:
            self.width_iter += self.get_pil_text_size(item_name,15)[0]
        self.height += 10 # 4 items add 41 to height

    
    def get_html(self):
        with open(f'{self.path}/test.html','w') as f:
            f.write(self.src.prettify())
        return self.src.prettify()

    def save_pic(self, banner_code: int = -1):
        '''
        generate image 
        '''
        filename = ''
        if self.uid != -1:
            if banner_code != -1:
                filename = f'{self.uid}_{banner_code}.png'
            else:
                filename = f'{self.uid}.png'
        else:
            filename = f'temp.png'
        
        #   adds 85 as bottom padding
        self.height += 85        

        self.renderer.screenshot(html_str=self.get_html(),save_as=filename,size=(self.width,self.height))
        
