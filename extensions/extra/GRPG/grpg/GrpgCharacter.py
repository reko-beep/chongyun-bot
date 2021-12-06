import logging
from .stats import StatsManager
from .compute import v
from .event import Event

from .GrpgCharacterBase import GrpgCharacterBase


class GrpgCharacter(GrpgCharacterBase):

    def __init__(self, inherent):
        super().__init__()
        
        # character's state in the game.
        self.weapon = None
        self.domain = None
        self.player_name = None
        self.current_hp = None
        self.current_stamina = 225
        self.alive = True

        self.stats = StatsManager(self, inherent)

        
        # player talents' action data.
        self.auto = {}
        self.charge = {}
        self.skill = {}
        self.burst = {}



    def set_player(self, party_name: str):
        """set which party the character belongs to"""
        self.player_name = party_name

    def set_domain(self, domain):
        """set the domain the character is in."""
        self.domain = domain

    def set_weapon(self, weapon: dict):
        """Set's the character's weapon"""
        self.weapon = weapon

    def __str__(self):
        """provides a meaningful name for logging."""
        return f'({self.party_pos}{self.player_name})' 



    def prepare(self):
        """prepare before entering the domain"""
        logging.info(f"{self}: preparing")
        self.stats.prepare()
        self.reset_hp()



   

    def reset_hp(self):
        """restore character's full hp"""
        logging.info(f"{self}: resetting hp to {self.stats.stats['Max HP']}")
        self.current_hp = v(self.stats.stats['Max HP'])


 


    
     

    @property
    def party_pos(self):
        """gives the character's position in party. (int)"""
        for pos, chara in enumerate(self.domain.players[self.player_name]['party']):
            if chara is self:
                return pos
        return '?'

    def take_field(self):
        "do stuff where chara takes the field here"
        logging.info(f'{self}: taking field')



    def leave_field(self):
        "do stuff when chara leaves field here"
        logging.info(f'{self}: leaving field')
        pass


    def get_hp(self):
        return self.current_hp




    def get_hit(self, bonk):
        """get hit by a bonk """
        elem = bonk['element']
        #TODO: do elemental reaction stuff and get dmg. tuple

        logging.info(f"{self} got hit with {bonk['dmg']}")

        
        dmg_taken = bonk['dmg'].get()

        # damage taken is above hp, so character dies. also emit event.
        if dmg_taken >= self.current_hp:
            self.alive = False
            self.domain.game.events.append(Event(Event.CHARA_FALL, self.party_pos))
            self.current_hp = 0

            # see if all party members died and emit game over event
            game_over = True
            for chara in self.domain.players[self.player_name]['party']:
                if chara.alive:
                    game_over = False
                    break
            if game_over:
                self.domain.game.events.append(Event(Event.GAME_OVER, self.player_name))
        
        else:
            self.current_hp = self.current_hp -  v(bonk['dmg'])
            logging.info(f"dmg taken: {bonk['dmg']}, hp: {self.current_hp}/{self.stats.stats['Max HP']}")




    def is_onfield(self):
        """checks whether player is on field"""
        player = self.domain.players[self.player_name]
        if self.party_pos == player['on_chara']:
            return True
        return False


    def tick(self):
        """update character state every turn here"""
        logging.info(f"{self}: ticking")
        self.current_stamina += 10


    def get_stats(self):
        """returns all the necessary character's state for debugging"""
        return f"""{self}>> hp: {self.get_hp()}/{self.stats.stats['Max HP']}, stamina: {self.current_stamina}/ {self.stats.stats['Max Stamina']} """
        


    def get_talent(self, talent_name: str):
        
        if talent_name not in ['auto', 'charge', 'skill', 'burst']:
            raise Exception('Invalid talent_name')

        level = self.stats.inherent['Talents'][talent_name]['Level']
        talent = self.stats.inherent['Talents'][talent_name]

        data = dict()
        for k, v in talent.items():
            if isinstance(v, dict):
                data[k] = v[level]
            elif isinstance(v, (int, float, str)):
                data[k] = v

        return data