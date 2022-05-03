
from os.path import exists
from os import getcwd    
from json import load,dump

profile = {                   
                'profiles': {},
                'leylines' : [],
                'domains' : [],
                'points' : 0,
                'points_to_give' : 0
            }


def load_file(filename):
    if exists(getcwd()+'/'+filename):
        with open(getcwd()+'/'+filename, 'r') as f:
            return load(f)
    return {}

def save_file(data,filename):
    with open(getcwd()+'/'+filename, 'w') as f:
            dump(data, f, indent=1)


data = load_file("coop.json")
prev_data = load_file("genshin.json")


for did in prev_data:
    profiles = {}
    servers = prev_data[did]['servers']
    for serv in servers:
        profiles[serv] = {
            'uid': servers[serv]
        }
    if 'wl' in prev_data[did]:
        for wl in prev_data[did]['wl']:
            if serv in profiles:
                profiles[serv]['wl'] = prev_data[did]['wl'][wl]
    
    data[did] = {'profiles': profiles,
      'leylines' : [],
                'domains' : [],
                'points' : 0,
                'points_to_give' : 0
            }

save_file(data, 'coop_transfered.json')
