from os.path import exists
from json import load, dump
from os import getcwd
from base.resource_manager import ResourceManager

class StatCalculator:
    def __init__(self, bot):
        self.bot = bot
        self.resm : ResourceManager = bot.resource_manager
        self.char_data = self.load_file(self.resm.genpath('data','char_level.json'))
        self.wep_data = self.load_file(self.resm.genpath('data','weapons.json'))
        self.curves = self.load_file(self.resm.genpath('data','weapon_level.json'))   
        pass



    def load_file(self, file: str):
    
        if exists(file):
            with open(file, 'r') as f:
                return load(f)
        return {}

    def save_file(self, data: dict, file: str):
        
        with open(file, 'w') as f:
                dump(data, f, indent=1)

    def generate_key(self, string: str):

        seps = ['-','/','\\','.',',','~','!','#','$']
        for s in seps:
            string = string.replace(s, '', 99)
        return string.replace(" ",'_',99).lower()

    def get_insensitive_key(self, dict, key):
        for k in dict:
            if key.lower() in k.lower():
                return dict[k]

    def get_base_value(self, char_name:str, type_:str=''):
        data = self.char_data
        for char in data['base_value']:
            search = char_name.lower()
            if ' ' in char_name:
                search = char_name.lower().split(' ')

            if type(search) == list:
                for s in search:
                    if s in char.lower():
                        if type_ == 'bonus':
                            return data['bonus']['base_value'][char]
                        return data['base_value'][char]
            else:
                if search in char.lower():
                    if type_ == 'bonus':
                        return data['bonus']['base_value'][char]
                    return data['base_value'][char]

    def get_level_multiplier(self, level: str, star: str):
        data = self.char_data['level_multiplier']
        level = level if type(level) == str else str(level)
        star = star if type(star) == str else str(star)
        return data[level][star]
            
    def get_ascension_levels(self, level:str):

        ascension_dict = {"20": 1, "40": 2, "50": 3,"60": 4,"70": 5, "80": 6}
        for level_check in ascension_dict:
            if int(level) < int(level_check):
                return ascension_dict[level_check]-1
        if int(level) > 80:
            return 6

    def get_section_ascension_phase(self, level: str):
        data = self.char_data['section_ascension_phase']
        ascension = self.get_ascension_levels(level)
        if ascension is not None:
            ascension = str(ascension)
            if ascension in data:
                return data[ascension]
        return 0

    def get_max_ascension_value(self, char_name:str):
        data = self.char_data['max_ascension_values']
        for char in data:
            search = char_name.lower()
            if ' ' in char_name:
                search = char_name.lower().split(' ')

            if type(search) == list:
                for s in search:
                    if s in char.lower():
                        return data[char]
            else:
                if search in char.lower():
                    return data[char]
    
    def get_special_stat(self, char_name:str, level: str):
        ascension = self.get_ascension_levels(level)

        stat = self.get_base_value(char_name, 'bonus')
        if stat is not None:
            name = list(stat.keys())[0]
            value = stat[name]

            if ascension is not None:
                if '%' in value:
                    return {name : eval(str(float(self.char_data['bonus']['ascension_multiplier'][str(ascension)]))+'*'+value.replace('%', '', 10)), 'perc': True}

                else:
                    return {name : eval(str(float(self.char_data['bonus']['ascension_multiplier'][str(ascension)]))+'*'+value), 'perc': False}

    def get_char_stats(self, char_name:str, level: int, stars: int):
       

        stats = {

        }
        char_stat_formula = '{base_value}*{level_multiplier}+({section_ascension_phase}*{max_ascension_values})'
        base_stats = self.get_base_value(char_name)
        for stat in base_stats:
            stat_value = eval(char_stat_formula.format(base_value=base_stats[stat], level_multiplier=self.get_level_multiplier( level, stars), section_ascension_phase=self.get_section_ascension_phase(level), max_ascension_values=self.get_max_ascension_value( char_name)[stat]))
            stats[stat] = int(round(float(stat_value),1))
        
        special_stat = self.get_special_stat(char_name, level)

        if special_stat is not None:
            key = [k for k in special_stat if k !=' perc'][0]
            if special_stat['perc'] == True:
                if key in stats and key in ['hp', 'atk', 'def']:
                    stats[f"{key}_bonus"] = str( int(round(float(special_stat[key]),1)))+'%'                
                if key in stats and key not in ['hp', 'atk', 'def']:
                    stats[key] = eval(special_stat[key].replace('%','',1)+"+"+stats[key])+"%"
                if key not in stats:
                    stats[key] = str( int(round(float(special_stat[key]),1)))+'%'                
            if special_stat['perc'] == False:
                if key in stats:
                    stats[key] +=  int(round(float(special_stat[key]),1))
                else:
                    stats[key] =  int(round(float(special_stat[key]),1))

        stats['crit_dmg'] = '50%'
        stats['crit_rate'] = '5%'
        return stats

    def get_weapon_curve(self, weapon_name: str, level: str, ascension_level: str):
       
        
        weapons = list(self.wep_data.keys())
        curve_data = {}
        for wep in weapons:
            if weapon_name.replace("'","",99).lower() in wep.lower():
                atk = self.get_insensitive_key(self.wep_data[wep]['stats'], 'Base ATK').split('-')[0].strip()                
                substat = self.wep_data[wep]['stats']['2nd StatType']
                if substat == 'None':
                    substat_value = '0'
                else:
                    substat_value = self.get_insensitive_key(self.wep_data[wep]['stats'], '2nd Stat(Lv.').split('-')[0].strip()
                is_perc = False
                if '%' in substat_value:
                    is_perc = True
                curve_type = ''
                rarity = str(self.wep_data[wep]['rarity'])
                for r in range(int(rarity), -1, -1):
                    if str(r) in self.curves['base_value']:
                        if str(atk) in self.curves['base_value'][str(r)]:
                            curve_type = self.curves['base_value'][str(r)][str(atk)]
                print('fetched attack', atk)
                if curve_type != '':
                    curve_data['base_value'] = atk
                    curve_data['base_level_multiplier'] = self.curves['level_multiplier'][curve_type][int(level)-1]
                    curve_data['ascension_value'] = '0'
                    if int(ascension_level) <= len(self.curves['ascension_value'][rarity]):
                        if self.curves['ascension_value'][rarity][int(ascension_level)-1] == 'None':
                            for c in self.curves['ascension_value'][rarity][::-1]:
                                if c != 'None':
                                    curve_data['ascension_value'] = c
                                    break
                        else:
                            curve_data['ascension_value'] = self.curves['ascension_value'][rarity][int(ascension_level)-1]

                curve_data['substat'] = {}

                substat_levels = [int(lvl) for lvl in self.curves['sub_stat']['level_multiplier'].keys()]

                for check in range(len(substat_levels)):
                    if not int(level) > substat_levels[check]:
                        curve_data['substat']['multiplier'] = self.curves['sub_stat']['level_multiplier'][str(substat_levels[check])]
                        break
                curve_data['substat']['base_value'] = substat_value
                curve_data['substat']['name'] = self.generate_key(substat)
                curve_data['substat']['perc'] = is_perc

        return curve_data

    def get_weapon_stats(self, wep_name:str, level: str, ascension:str):

        stat = {}
        data = self.get_weapon_curve(wep_name, level, ascension)
        base_stat = '{base_value}*{base_level_multiplier}+{ascension_value}'
        sub_stat = '{base_value}*{multiplier}'
        atk = int(round(float(eval(base_stat.format(base_value=data['base_value'], base_level_multiplier=data['base_level_multiplier'], ascension_value=data['ascension_value']))),1))
        stat['atk'] = atk
        if data['substat']['perc']:
            stat[data['substat']['name']]= str(int(round(float(eval(sub_stat.format(base_value=data['substat']['base_value'].replace('%','',1), multiplier=data['substat']['multiplier']))),1)))+'%'
        else:
            stat[data['substat']['name']]= int(round(float(eval(sub_stat.format(base_value=data['substat']['base_value'], multiplier=data['substat']['multiplier']))),1))

        return stat

    def check_bonusstat(self, key,  value):
        if key in ['atk', 'hp', 'def']:
            if type(value) == str:
                if '%' in value:
                    return True
            else:
                if type(value) == int:
                    return False

    def sum_stats(self, *args):
        stat_final = {}

        for dict_ in args:
            for k in  dict_:
                perc_check = self.check_bonusstat(k, dict_[k])
                if perc_check == True:
                    if f'{k}_bonus' not in stat_final:
                        stat_final[f'{k}_bonus'] = dict_[k]
                    else:
                        stat_final[f'{k}_bonus'] = str(eval(stat_final[f'{k}_bonus'].replace('%', '',1)+'+'+dict_[k].replace('%','',1)))+'%'
                if perc_check == False:
                    if k not in stat_final:
                        stat_final[k] = dict_[k]
                    else:
                        stat_final[k] += dict_[k]
                if perc_check == None:
                    if k not in stat_final:
                        stat_final[k] = dict_[k]
                    else:
                        if type(stat_final[k]) == str:
                            if '%' in dict_[k]:                         
                                stat_final[k] = str(eval(stat_final[k].replace('%', '',1)+'+'+dict_[k].replace('%','',1)))+'%'
                        else:                        
                            stat_final[k] += dict_[k]
        
        return stat_final


