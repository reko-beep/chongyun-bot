import logging

from .compute import V, v
from .event import Event

from .util import get_opponent
from .GrpgCharacter import GrpgCharacter

class Kaeya(GrpgCharacter):
    
    def __init__(self, level=1):
        
        # inherent parameters, not tweakable.   
        inherent = {
            'Level': level,
            'Element': 'cryo',
            'Stats': {
                    'Base HP': {1: 976, 20: 2506, 20.5: 3235, 40: 4846, 40.5: 5364, 50: 6170, 50.5: 6860, 60: 7666, 60.5: 8184, 70: 8989, 70.5: 9507, 80: 10312, 80.5: 10830, 90: 11636},
                    'Base ATK': {1: 19, 20: 48, 20.5: 62, 40: 93, 40.5: 103, 50: 118, 50.5: 131, 60: 147, 60.5: 157, 70: 172, 70.5: 182, 80: 198, 80.5: 208, 90: 223},
                    'Base DEF': {1: 66, 20: 171, 20.5: 220, 40: 330, 40.5: 365, 50: 420, 50.5: 467, 60: 522, 60.5: 557, 70: 612, 70.5: 647, 80: 702, 80.5: 737, 90: 792},
                    'Energy Recharge': {0: 0, 20: 0, 20.5: 0, 40: 0, 40.5: 0.067, 50: 0.067, 50.5: 0.133, 60: 0.133, 60.5: 0.133, 70: 0.133, 70.5: 0.20, 80: 0.20, 80.5: 0.267, 90: 0.267},
                    'ATK': {},
                    'Crit Rate': {1: 0.05, 20: 0.05, 20.5: 0.05, 40: 0.05, 40.5: 0.05, 50: 0.05, 50.5: 0.05, 60: 0.05, 60.5: 0.05, 70: 0.05, 70.5: 0.05, 80: 0.05, 80.5: 0.05, 90: 0.05},
                    'Crit DMG': {1: 0.5, 20: 0.5, 20.5: 0.5, 40: 0.5, 40.5: 0.5, 50: 0.5, 50.5: 0.5, 60: 0.5, 60.5: 0.5, 70: 0.5, 70.5: 0.5, 80: 0.5, 80.5: 0.5, 90: 0.5}
            },
            'Talents': {
                'auto': {
                    'DMG': { 
                        1: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        2: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        3: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        4: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        5: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        6: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        7: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        8: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        9: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                        10: [0.5375,  0.5813,  0.625,  0.6875,  0.7313],
                    },
                    'Level': 1
                },
                'charge': {
                    'DMG': {1: 0.5375, 2: 5813, 3: 0.625, 4: 0.6875, 5: 0.7313, 6: 0.7813, 7: 0.85, 8: 0.9188, 9: 0.9875, 10: 5.0625},
                    'Stamina Cost': {1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20, 10: 20},
                    'Level': 10

                },
                'skill': {
                    'DMG': {1: 0.5375, 2: 5813, 3: 0.625, 4: 0.6875, 5: 0.7313, 6: 0.7813, 7: 0.85, 8: 0.9188, 9: 0.9875, 10: 1.0625},
                    'CD': {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
                    'Level': 1
                },
                'burst': {
                    'DMG': {1: 0.5375, 2: 5813, 3: 0.625, 4: 0.6875, 5: 0.7313, 6: 0.7813, 7: 0.85, 8: 0.9188, 9: 0.9875, 10: 0.10625},
                    'CD': {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
                    'Duration': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8},
                    'Energy Cost': {1: 60, 2: 60, 3: 60, 4: 60, 5: 60, 6: 60, 7: 60, 8: 60, 9: 60, 10: 60},
                    'Level': 1
            
                }
            }
            
        }
       


        super().__init__(inherent)




    def invoke_auto(self):

        #SECTION: auto attack configs
        AOE = False

        #END

        talent = self.get_talent('auto')

        # record auto attack streak (decides the damage multiplier to use)
        # TODO: getting interrupted or using other talents should reset the streak.
        if self.auto.get('streak') is None:
            self.auto['streak'] = 0
        else:
            self.auto['streak'] += 1
        
        # pick the damange multiplier based on streak.
        #  (1-hit dmg, 2-hit dmg, etc.,)
        mulitplier_list = talent['DMG']
        i = self.auto['streak'] % len(mulitplier_list) 
        xer = mulitplier_list[i]
        logging.info(f"{self}: invoking auto {i} with dmg scale: {xer}")



        # TODO: apply remove/buffs debuffs on self and/or enemies, if any
        
        # calculate output dmg
        auto_dmg_out = self.stats.stats['ATK'] * xer


        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        chara = opponent['party'][opponent['on_chara']]
        bonk = {'element': 'physical', 'dmg': auto_dmg_out}
        chara.get_hit(bonk)


        
    #TODO: decorators to get common values would be good.
    def invoke_charge(self):
        #SECTION: auto attack configs
        AOE = True

        #END

        
        talent = self.get_talent('charge')

        if self.current_stamina < talent['Stamina Cost']:
            # not enough stamina
            return

        self.current_stamina -= talent['Stamina Cost']

        logging.info(f"{self}: invoking charge attack with xer: {talent['DMG']}")




        # TODO: apply remove/buffs debuffs on self and/or enemies
        
        # calculate output dmg
        auto_dmg_out = self.stats.stats['ATK'] * talent['DMG']

        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        for chara in opponent['party']:
            bonk = {'element': 'physical', 'dmg': auto_dmg_out}
            chara.get_hit(bonk)
            if not AOE: break


    def invoke_skill(self):
        pass

    def invoke_burst(self):
        pass

  
