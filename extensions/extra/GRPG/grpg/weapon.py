import json
import os

from thefuzz import process as fuzz_process

from .compute import E
from .util import interpolate_stat


class Weapon:
    def __init__(self, name, level):
        
        weps_file = os.path.join(os.path.dirname(__file__), 'weapons_list.json')
        with open(weps_file) as f:
            all_weps = json.load(f)
        
        wep_names = list(all_weps.keys())
        name, _certainity = fuzz_process.extractOne(name, wep_names)


        self.name = name
        self.level = level  
        self.data = all_weps[name]


    @property
    def base_atk(self):
        """returns the Base ATK of the weapon"""    
        table = {k: v for k, v in self.data['Base ATK'].items()}
        return interpolate_stat(table, self.level)
        


    @property
    def pbuffs(self):
        """Returns the buffs provided by passive"""

        data = dict()
        for k, table in self.data['pbuffs'].items():
            data[k] = interpolate_stat(table, self.level)

        return data