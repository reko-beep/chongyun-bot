from copy import deepcopy

from .kaeya import Kaeya

class Domain:
    """
    Reprsents a Domain as defined by Genshin.
    Acts as an Environment/Stage where parties join and fight.
    Influences the battle by buffing/debuffing characters.
    """
    def __init__(self, game):

        self.game = game
        
        # stores party charas and party meta data.
        # this should have been self.parties instead and only store the party info
        # while other info should have been handled by the game but meh, works
        # for now
        player_data = {
            "party": [],
            "on_chara": 0,
            # "uses": {
            #     "auto": 0,
            #     "charge": 0,
            #     "skill": 0,
            #     "burst": 0
            # }
        }
        self.players = {
            "A": deepcopy(player_data),
            "B": deepcopy(player_data)
        }
    

    def add_player(self, player_name, *party):
        """adds a player with given party of characters"""

        if player_name not in ['A', 'B']:
            raise Exception("invalid party_name name")



        for chara in party:
            # validate team member
            
            chara = Kaeya(level=90)
            chara.set_domain(self)
            chara.set_player(player_name)
            chara.set_weapon({'Base ATK': 200})
            chara.prepare()

            self.players[player_name]['party'].append(chara)
    
    