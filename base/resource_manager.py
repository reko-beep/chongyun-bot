
from os import getcwd, listdir
from os.path import exists, isfile, isdir
from json import load, dump

class ResourceManager:
    def __init__(self, site: str = ''):
        '''
        Initializes Resource Manager Client
        '''
        self.site = site+'/assets/' if site != '' else 'http://127.0.0.1:5000/assets/'        
        self.files = ['characters.json','quests.json','voiceovers.json',
                    'polearms.json','swords.json','quests.json','wallpapers.json',
                    'catalysts.json','claymores.json','domains.json', 'artifacts.json']
        
        self.path = getcwd()+'/assets/{path}'
        self.db = getcwd()+'/db/{path}'


        self.__load()
    
    def flatten_list(self, list_ : list):
        if len(list_) > 0:
            return list_[0]
        else:
            return ''

    def __path(self, path_: str):

        if exists(self.path.format(path=path_)):
            return self.path.format(path=path_)

    def __search(self, search_string: str , search_list: list):
        """
        searches a string in search_list
        """
        for s_item in search_list:
            if search_string.lower() in s_item.lower():
                return s_item

    def __load(self):
        for file in self.files:
            p = self.__path(f'/db/{file}')
            if p is not None:

                with open(p, 'r') as f:

                    self.__dict__[file.split('.')[0]] = load(f)

    def __genpath(self, path: str, file_name: str):
        return self.path.format(path=f'{path}/{file_name}')

    def __navigate(self, path, files: bool = True, dirs: bool = True):
        list_dir = {}

        if '.' not in path and path[-1] != '/':
            path += '/' 
        
        gen_path = self.__path(path)
        
        print('Folder', dirs, 'Files', files, 'Path', path, 'Generated Path', gen_path)  

        if exists(gen_path):
            if isfile(gen_path):
                return {'files': [gen_path]}
            lister = listdir(gen_path)
            if files:              
                    list_dir['files'] = [file for file in lister if isfile(self.__genpath(path, file))]
            if dirs:
                    list_dir['folders'] = [folder for folder in lister if isdir(self.__genpath(path, folder))]

        return list_dir 
    
    def goto(self, path, files: bool = True, dirs: bool = True):
        '''
        navigates to asset path

        return
        {
            'files': [files, f, ...]
            'folders' : [folders, f , ...]
        }
        '''
        list_dir = {}

        if '.' not in path and path[-1] != '/':
            path += '/' 
        print(path)
        gen_path = self.__path(path)
        
        print('Folder', dirs, 'Files', files, 'Path', path, 'Generated Path', gen_path)  
        if exists(gen_path):
            if isfile(gen_path):
                return {'files': [gen_path]}
            lister = listdir(gen_path)
            if files:              
                    list_dir['files'] = [file for file in lister if isfile(self.__genpath(path, file))]
            if dirs:
                    list_dir['folders'] = [folder for folder in lister if isdir(self.__genpath(path, folder))]

        return list_dir 

    def dbfile(self, file_path: str, load_data:bool = False):
        '''
            generates a path for database file or loads data if set true
        '''

        if '.' not in file_path and file_path[-1] != '/':
            file_path += '/' 

        gen_path = self.db.format(path=file_path)
        
        if exists(gen_path):
            if isfile(gen_path):
                if load_data:
                    if gen_path.split('/')[-1].split('.')[-1] in ['json','txt']:
                        with open(gen_path, 'r') as f:
                            return load(f)
                return gen_path
            
         


    def get_character_guides(self, character_name: str, option: str, url:bool = False):
        '''
        gets all character guides for a [character_name] having option [option | builds | ascention_talents]
        url if set true generates url 
        '''

        characters = self.__navigate('images/characters/',False)['folders']
        print(characters)
        character_folder = self.__search(character_name, characters)

        if character_folder is not None:
            options = self.__navigate(f'images/characters/{character_folder}', False)['folders']

            option_selected = self.__search(option, options)
            if option_selected is not None:
                paths =  [self.__genpath(f'images/characters/{character_folder}/{option_selected}', f)
                         for f in self.__navigate(f'images/characters/{character_folder}/{option_selected}', True, False)['files']]
                return [self.convert_to_url(p, url) for p in paths]

    def convert_to_url(self, path_: str, url: bool= False):
        '''
        converts to a url for webserver link
        provided a local path path_
        '''
        if url:
            return path_.replace(getcwd()+'/assets/', self.site)
        else:
            return path_


    def get_character_full_details(self, character_name: str, url: bool):
        '''
        gets all details for character [character_name]
        '''

        data = {}
        character_search_list = list(self.characters.keys())
        character = self.__search(character_name, character_search_list)

        if character is not None:
            data = self.characters[character]
            builds = self.get_character_guides(character, 'b', url)
            ascension = self.get_character_guides(character, 'as',  url)
            data['builds'] = builds
            data['ascension_imgs'] = ascension

        return data if len(data) != 0 else None

    def getdata(self, key: str):

        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise Exception(f'No data exists with {key}!')


    def character_details(self, character_name: str, details: list):
        raise NotImplementedError



