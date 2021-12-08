import logging
from .compute import E
from .util import interpolate_stat
from copy import deepcopy

class StatsManager:
    """Stores and Manages all the Character's stats."""

    def __init__(self, chara, inherent: dict):
        self.chara = chara
     
        # these values are static for the most part.
        # probably never change in the GRPG
        self.inherent = { 
            'Level': 0,
            'Progression': {   
                'Base HP': {}, 
                'Base ATK': {},
                'Base DEF': {},
                'Energy Recharge': {},
                'ATK': {},
                'Crit Rate': {},
                'Crit DMG': {}
            }
        }

        self.inherent = inherent

        # stats as shown in the character's stats screen in-game
        # may change due to several influences from domain, artifacts, food etc.,
        self.stats = { 
            'Max HP': E(0),
            'ATK': E(0),
            'DEF': E(0),
            'Elemental Mastery': E(0),
            'Max Stamina': E(0),
            'Crit DMG': E(0.5),
            'Crit Rate': E(0.5),
            'Healing Bonus': E(0),
            'Incoming Healing Bonus': E(0),
            'Energy Recharge': E(0),
            'CD Reduction': E(0),
            'Shield Strength': E(0),
            'Pyro DMG Bonus': E(0),
            'Pyro RES': E(0),
            'Hydro DMG Bonus': E(0),
            'Hydro RES': E(0),
            'Dendro DMG Bonus': E(0),
            'Dendro RES': E(0),
            'Electro DMG Bonus': E(0),
            'Electo RES': E(0),
            'Anemo DMG Bonus': E(0),
            'Anemo RES': E(0),
            'Cryo DMG Bonus': E(0),
            'Cryo RES': E(0),
            'Geo DMG Bonus': E(0),
            'Geo RES': E(0),
            'Physical DMG Bonus': E(0),
            'Physical RES': E(0)

        }

        # percentage buffs
        self.pbuffs = deepcopy(self.stats)
        # flat buffs
        self.fbuffs = deepcopy(self.stats)


    def prepare(self):
        """
        prepares all the stats
        this method must be run before using any stats.
        """

        # formulae (expressed in terms of flow graphs)
        s = self.stats
        pb = self.pbuffs
        fb = self.fbuffs
        i = self.inherent
        
        _base_hp = self.interpolate_stat('Base HP')
        s['Max HP'] = E(_base_hp) * (pb['Max HP'] + 1) + fb['Max HP']
        
        _base_atk = self.interpolate_stat('Base ATK') + self.chara.weapon.base_atk
        s['ATK'] = (pb['ATK'] + 1) * _base_atk + fb['ATK']

        s['DEF'] # = ?

        s['Elemental Mastery'] = s['Elemental Mastery'] + fb['Elemental Mastery']

        s['Max Stamina'] # = ?, maybe current stamina should be part of stats? cuz some domains affect that
        
                





    def apply_pbuffs(self, data):
        if not isinstance(data, dict) or not bool(data): return
        for stat, val in data.items():
            self.pbuffs[stat] += E(val)
            logging.info(f"{self.chara}: sm >> buffed {stat} % : +{val}. total: {self.pbuffs[stat].eq()}")


    def apply_fbuffs(self, data):
        if not isinstance(data, dict) or not bool(data): return
        for stat, val in data.items():
            self.fbuffs[stat] += E(val)
            logging.info(f"{self.chara}: sm >> buffed {stat} flat : +{val}. total: {self.fbuffs[stat].eq()}")



    def get_RES(self, element: str):
        """return's the character's aggregate RES (includes normal RES too) for given element"""
        return self.stats[element + ' RES']
        

    def interpolate_stat(self, stat_name):
        """calculates the stats for intermediate levels not listed in table"""
        
        table = self.inherent['Stats'][stat_name]
        level = self.inherent['Level']

        return interpolate_stat(table, level)

