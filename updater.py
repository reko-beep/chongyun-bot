from datetime import datetime
from json import load, dump
from os import getcwd 
from os.path import exists
from datetime import datetime


DATA = {} #holds updater data

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



