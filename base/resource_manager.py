
from os import getcwd, listdir
from os.path import exists, isfile, isdir
from json import load, dump
from colorthief import ColorThief
import requests
from io import BytesIO
class ResourceManager:
    def __init__(self, site: str = ''):
        '''
        Initializes Resource Manager Client
        '''
        self.site = site+'/assets/' if site != '' else 'http://127.0.0.1:80/assets/'        
        self.files = ['characters.json','quests.json','voiceovers.json','quests.json','wallpapers.json','weapons.json'
                    ,'domains.json', 'artifacts.json', 'furnishing.json', 'materials.json']
        
        self.path = getcwd()+'/assets/{path}'
        self.db = getcwd()+'/db/{path}'
        self.cached_colors = {

        }


        self.__load()
        self.__load_colors()
    
    def __load_colors(self):
        path = self.db.format(path='cc.json')
        if exists(path):
            with open(path, 'r') as f:
                self.cached_colors = load(f)
    
    def __save_colors(self):
        path = self.db.format(path='cc.json')        
        with open(path, 'w') as f:
            dump(self.cached_colors, f, indent=1)
    

    def flatten_list(self, list_ : list):
        if len(list_) > 0:
            return list_[0]
        else:
            return ''

    def __path(self, path_: str):

        if exists(self.path.format(path=path_)):
            return self.path.format(path=path_)

    def search(self, search_string: str , search_list: list, split_search:bool=True):
        """
        searches a string in search_list
        """
        if split_search:
            if ' ' in search_string:
                search_string = search_string.split(' ')
        for s_item in search_list:
            if type(search_string) == list:
                for s in search_string:
                    if s.lower() in s_item.lower():
                        return s_item
            else:
                if search_string.lower() in s_item.lower():
                    return s_item

    def __search(self, search_string: str , search_list: list):
        """
        searches a string in search_list
        """
        if ' ' in search_string:
            search_string = search_string.split(' ')
        for s_item in search_list:
            if type(search_string) == list:
                for s in search_string:
                    if s.lower() in s_item.lower():
                        return s_item
            else:
                if search_string.lower() in s_item.lower():
                    return s_item

    def __load(self):
        for file in self.files:
            p = self.__path(f'/data/{file}')
            if p is not None:

                with open(p, 'r') as f:

                    self.__dict__[file.split('.')[0]] = load(f)
        
        

    def genpath(self, path: str, file_name: str):
        return self.path.format(path=f'{path}/{file_name}')

    def __navigate(self, path, files: bool = True, dirs: bool = True):
        list_dir = {}

        if path != '' and '.' not in path and path[-1] != '/' :
            path += '/' 
        
        gen_path = self.__path(path)

        if exists(gen_path):
            if isfile(gen_path):
                return {'files': [gen_path]}
            lister = listdir(gen_path)
            if files:              
                    list_dir['files'] = [file for file in lister if isfile(self.genpath(path, file))]
            if dirs:
                    list_dir['folders'] = [folder for folder in lister if isdir(self.genpath(path, folder))]

        return list_dir 
    
    def goto(self, path, files: bool = True, dirs: bool = True):
        list_dir = {}

        if path != '' and '.' not in path and path[-1] != '/' :
            path += '/' 
        gen_path = self.__path(path)
        
        if exists(gen_path):
            if isfile(gen_path):
                return {'files': [gen_path]}
            lister = listdir(gen_path)
            if files:              
                    list_dir['files'] = [file for file in lister if isfile(self.genpath(path, file))]
            if dirs:
                    list_dir['folders'] = [folder for folder in lister if isdir(self.genpath(path, folder))]
        return list_dir 

    def dbfile(self, path, files: bool = True, dirs: bool = True):
        list_dir = {}

        if '.' not in path and path[-1] != '/':
            path += '/' 
        gen_path = self.db.format(path=path)
        
        if exists(gen_path):
            if isfile(gen_path):
                return {'files': [gen_path]}
            lister = listdir(gen_path)
            if files:              
                    list_dir['files'] = [file for file in lister if isfile(self.genpath(path, file))]
            if dirs:
                    list_dir['folders'] = [folder for folder in lister if isdir(self.genpath(path, folder))]

        return list_dir 


    def get_character_guides(self, character_name: str, option: str, url:bool = False):

        characters = self.__navigate('images/characters/',False)['folders']
        character_folder = self.__search(character_name, characters)

        if character_folder is not None:
            options = self.__navigate(f'images/characters/{character_folder}', False)['folders']

            option_selected = self.__search(option, options)
            if option_selected is not None:
                paths =  [self.genpath(f'images/characters/{character_folder}/{option_selected}', f)
                         for f in self.__navigate(f'images/characters/{character_folder}/{option_selected}', True, False)['files']]
                return [self.convert_to_url(p, url) for p in paths]

    def convert_to_url(self, path_: str, url: bool= False):
        if url:
            return path_.replace(getcwd()+'/assets/', self.site)
        else:
            return path_


    def get_comps(self, character_name: str, url: bool):
        file = self.db.format(path='teamcomp.json')
        with open(file, 'r') as f:
            data = load(f)['data']
        teamcomps = []
        character_name = character_name.strip()
        for c,i in enumerate(data):
            
            chars = [list(k.keys())[0] for k in i['chars']]
            
            for char in chars:               
                if char.lower() in character_name.lower():
                    if url:
                        path = self.genpath('images/teamcomps', i['file'])
                        i['file'] = self.convert_to_url(path, url)
                    else:
                        i['file'] = self.genpath('images/teamcomps', i['file'])
                    teamcomps.append({ **i, **{'index': c}})
        return teamcomps

    def get_color_from_image(self, url, rgb:bool=False, hex:bool=False, int_color:bool=True):

        if url in self.cached_colors:
            return self.cached_colors[url]
        else:
            with requests.get(url) as f:
                test = ColorThief(BytesIO(f.content))
                def clamp(x): 
                    return max(0, min(x, 255))
                color = test.get_color(quality=1)
                if rgb:
                    return color
                if hex:
                    return "{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2]))
                self.cached_colors[url] = int("{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2])),16)
                self.__save_colors()
                return int("{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2])),16)

    def get_abyss_details(self):
        path = self.res_handler.genpath('data', self.res_handler.search('abyss',self.res_handler.goto('data').get('files')))        
        with open(path, 'r') as f:
            return load(f)

    def get_character_full_details(self, character_name: str,split_search:bool=True):

        data = {}
        character_search_list = list(self.characters.keys())
        character = self.__search(character_name, character_search_list)
        url = True
        if character is not None:
            data = self.characters[character]
            builds = self.get_character_guides(character, 'b', url)
            ascension = self.get_character_guides(character, 'as',  url)
            data['builds'] = builds
            data['ascension_imgs'] = ascension
            data['teamcomps'] = self.get_comps(character_name, url)
        return data if len(data) != 0 else None

    def getdata(self, key: str):

        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise Exception(f'No data exists with {key}!')


    def get_element(self, element: str):
        element_file = self.genpath('jsons',self.search('element',self.goto('jsons').get('files')))
        with open(element_file,'r') as f:
            element_data = load(f)
            element_searched = self.search(element, list(element_data.keys()))
            if element_searched is not None:
                return element_data[element_searched]


    def get_weapon_details(self, weapon_name:str, split_search:bool=True):

        
        weapons_names = list(self.weapons.keys())
        selected_weapon = self.search(weapon_name, weapons_names, split_search)

        if selected_weapon is not None:
            return self.weapons[selected_weapon]
    
    def get_artifact_details(self, artifact_name:str, split_search:bool=True):
    
        
        artifacts_names = list(self.artifacts.keys())
        selected_artifact = self.search(artifact_name, artifacts_names, split_search)

        if selected_artifact is not None:
            return self.artifacts[selected_artifact]
    
    def get_furnishing_details(self, character_name:str, split_search:bool=True):
        
        
        furnishings = self.furnishing['data']
        searched = []
        for furn in furnishings:
            selected= self.search(character_name, furn['chars'], split_search)
            if selected is not None:
                searched.append(furn)

        if len(searched) != 0:
            return searched
    
    def get_domain(self, day:str='', region:str='', type_:str=''):

        with open(self.path.format(path='data/domains.json'), 'r') as f:
            data = load(f)
        
        searched = []
        search_data = data['rotations']

        for rot in search_data:
            domain = data['domains'][rot['domain_id']]
            days = [d.lower() for d in rot['days']]
            days += ['']
            type_rot = [rot['type']]
            type_rot += ['']
            region_rot = ['', domain['location'].split(",")[-1].lower().strip()]
            if day in days and type_ in type_rot and region in region_rot:
                searched.append({
                    'domain_name' : domain['title'],
                    'domain_location' : domain['location'],
                    'domain_description': domain['description'],
                    'day' : '🔸'+'\n🔸'.join([d.title() for d in days]),
                    'type': domain['type'] +' | ' + rot['type'].title(),
                    'required_ar': domain['required_ar'],
                    'required_plevel': domain['required_party_level'],
                    'domain_image': domain['image'],
                    'farmed_for': [f['title'] for f in rot['for']],
                    'item_series': rot['series'],
                    'items': [f['title'] for f in rot['items']],
                    'file': self.genpath("images/domains", rot['file'])
                })
        return searched

    def get_material_details(self, material_name:str, split_search:bool=True):

        material_list = list(self.materials.keys())
        material = self.search(material_name, material_list, split_search)

        if material is not None:
            return self.materials[material]
