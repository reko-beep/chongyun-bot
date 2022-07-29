from base.image_generator import ImageGenerator
from base.resource_manager import ResourceManager
from sys import exit, argv
from json import load, dump
'''

CLI SCRIPT

_____________________________________


arg to passed: 1

Allowed:

    talents
    constellations

Example:

    python3 constellation_talents_img.py talents

Result:

    Generates and stores images in images/characters/character_name/



'''
def main():

    rm = ResourceManager()
    im = ImageGenerator(rm)
    characters = rm.genpath('data',rm.search('character',rm.goto("data").get('files')))
    print(characters)
    with open(characters, 'r') as f:
        data = load(f)



    arg_passed = ''
    if len(argv) > 1:
        arg_passed = argv[1]


    if arg_passed != '':
        if arg_passed in ['talents', 'constellations']:
            for char in data:            
                path = rm.genpath("images/characters", rm.search(char, rm.goto('images/characters').get('folders')))
                if path.split('/')[-1] == 'None':
                    pass
                else:

                    text_list = []
                    image_list = []
                    if arg_passed == 'talents':

                        for i in data[char]['talents']:
                            text_list.append(i['name'])
                            image_list.append(i['icon'])

                    if arg_passed == 'constellations':
                        for i in data[char]['constellations']:
                            text_list.append(data[char]['constellations'][i]['name'])
                            image_list.append(data[char]['constellations'][i]['icon'])
                            
                    if len(text_list) > 0 and len(image_list) > 0:
                        img = im.create_image(image_list, text_list, True, filename=arg_passed+'.png', filepath=path)
                        print(f'Generated {arg_passed} for character {char}\nSaved in {path}')
        else:
            exit('Argument not supported!')
    else:
        exit('No arguments passed')

if __name__ == '__main__':
    main()



