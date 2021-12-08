import logging
from typing import List
from .GrpgCharacter import GrpgCharacter

from .domain import Domain

class Zhou(Domain):

    def __init__(self, game):

       
        self.fullname = "Hidden Palace of Zhou Formula"
        self.description = "favourite but also cursed domain."
        self.fbuffs = {'ATK': 3000}
        self.pbuffs = {}

        super().__init__(game)



    def tick(self):
        """
        update domain state every turn here
        """
        
        logging.info('ticking')
        current_party: List[GrpgCharacter] = self.players[self.game.player]['party']

        for chara in current_party:
            chara.tick()





