from datetime import datetime
from json import load, dump
from os import getcwd 
from os.path import exists
from datetime import datetime
from base.resource_manager import ResourceManager


DATA = {} #holds updater data
rm = ResourceManager()
if exists(getcwd()+'/updater.json',):
    with open(getcwd()+'/updater.json', 'r') as f:
        DATA = load(f)


def save_data():
    with open(getcwd()+'/updater.json', 'w') as f:
        dump(DATA, f , indent=1)


def compare_date(key, current_time, diff):
    if key in DATA:
        lasttm = DATA[key].get('time', None)
        if lasttm is not None:
            lasttm = datetime.strptime(lasttm, '%c')
            if (current_time-lasttm).seconds > diff:
                return True

character_file_path = rm.genpath('data', 'characters.json')
with open(character_file_path, 'r') as f:
    character_data = load(f)

import scripts_to_update_database.guides