from typing_extensions import Required
import requests
from os import getcwd,mkdir, listdir
from os.path import exists, isfile, join
from json import dump, load
from html import unescape

class Fetcher:
    def __init__(self):
        self.base_url = 'https://genshin-impact.fandom.com/wiki/{arg}'
        self.session = requests.session()
        self.folder = f'{getcwd()}/assets/'
        self.data = {}
    
    def get(self, arg):
        return self.session.get(self.base_url.format(arg=arg))

    def save(self, path, file_name : str):
        if not exists(self.folder + '/' + path +'/'):
            mkdir(self.folder + '/' + path +'/')

        with open(self.folder + '/' + path +'/' + unescape(file_name).lower()+'.json', 'w') as f:
            dump(self.data,f,indent=1)

    def generate_key(self, string: str):
        seps = ['-','~','`',':',".","/",".", '%22', '22', '27']
        for sep in seps:
            string = string.replace(sep,'',99)
        string = string.replace('__','_',1).replace('_s_','_s',9).lower()
        return string

    def fetch(self):
        raise NotImplementedError
    
    def save_in_one(self, folder: str, name: str):
        if exists(self.folder+ '/' + folder):
            files_list = [join(self.folder+ '/' + folder+ "/" + f) for f in listdir(self.folder+ '/' + folder) if isfile(join(self.folder+ '/' + folder+ "/" + f))]
            temp_data = {}
            for file in files_list:
                file_name = file.split('/')[-1].split('.')[0].replace('%27','',1).title().replace('_',' ',99)
                print(file_name)
                with open(file, 'r') as f:
                    temp_data[file_name] = load(f)
            with open(self.folder+ '/' + folder + '/' + name,'w') as f:
                dump(temp_data,f,indent=1)

    def find_image(self,img):
        if img.name != 'img':
            img = img.find('img')
        if img is not None:
            if img.attrs['src'].startswith('http'):
                return (img.attrs['src'][:img.attrs['src'].find('/revision')])
            else:
                if 'data-src' in img.attrs:
                    return (img.attrs['data-src'][:img.attrs['data-src'].find('/revision')])
        return ''


