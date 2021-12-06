from .compute import V

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
            'Max HP': V(0),
            'ATK': V(0),
            'DEF': V(0),
            'Elemental Mastery': V(0),
            'Max Stamina': V(0),
            'Crit DMG': V(0),
            'Crit Rate': V(0),
            'Healing Bonus': V(0),
            'Incoming Healing Bonus': V(0),
            'Energy Recharge': V(0),
            'CD Reduction': V(0),
            'Shield Strength': V(0),
            'Pyro DMG Bonus': V(0),
            'Pyro RES': V(0),
            'Hydro DMG Bonus': V(0),
            'Hydro RES': V(0),
            'Dendro DMG Bonus': V(0),
            'Dendro RES': V(0),
            'Electro DMG Bonus': V(0),
            'Electo RES': V(0),
            'Anemo DMG Bonus': V(0),
            'Anemo RES': V(0),
            'Cryo DMG Bonus': V(0),
            'Cryo RES': V(0),
            'Geo DMG Bonus': V(0),
            'Geo RES': V(0),
            'Physical DMG Bonus': V(0),
            'Physical RES': V(0)

        }

        # percentage buffs
        self.pbuffs = self.stats
        # flat buffs
        self.fbuffs = self.stats


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
        s['Max HP'] = V(_base_hp) * (pb['Max HP'] + 1) + fb['Max HP']
        
        _base_atk = self.interpolate_stat('Base ATK') + self.chara.weapon['Base ATK']
        s['ATK'] = (pb['ATK'] + 1) * _base_atk + fb['ATK']

        s['DEF'] # = ?

        s['Elemental Mastery'] = s['Elemental Mastery'] + fb['Elemental Mastery']

        s['Max Stamina'] # = ?, maybe current stamina should be part of stats? cuz some domains affect that
        
                







        def buff(self, *, stat, val):
            pass





    def interpolate_stat(self, stat_name):
        """calculates the stats for intermediate levels not listed in table"""
        
        table = self.inherent['Stats'][stat_name]
        level = self.inherent['Level']

        if not bool(table): return 0

        stat = table.get(level)
        
        if not stat:
            # find the lower and higher levels that the given level is between.
            low = high = 1      
            for lvl in table.keys():
                if level > lvl:
                    low = lvl
                else:
                    high = lvl
                    break

            step = (table[high] - table[low]) / (high - low)
            stat = table[low] + (step * (level - low))

        return stat