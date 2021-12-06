import logging
from . import log_config

from collections import deque
from .event import Event
from .util import get_opponent

from .zhou import Zhou

class Game:
    """Represents and holds the entire state of the game."""
    
    def __init__(self):
        logging.info("starting game")
        self.player = "A"

        self.domain = None
        self.swap_turn = False
        self.events = deque([])

        self.game_over = False
        self.winner = None


    def pick_domain(self, name):
        """select a domain (arena) for the game"""
        self.domain = Zhou(self)



    def try_swap_turn(self):
        """
        swap player turns if swap_turn is True\n
        returns true if swap succeeded
        """
        if self.swap_turn:
            self.player = 'A' if self.player == 'B' else "B"
            self.swap_turn = not self.swap_turn
            logging.info(f"it's {self.player}'s turn now, {get_opponent(self.player)} is idle.")
            return True

        return False

    def main_loop(self):
        """
        Game's mainloop
        processes all game events, handles inputs, and makes everything else work
        note: each loop doesnt mean a turn.
        """
        while not self.game_over:
            self.handle_events()

            if self.try_swap_turn():
                self.domain.tick()

            yield

        yield

    def handle_events(self):
        """handle all game events"""

        
        # process all events until queue is empty.
        while len(self.events) != 0:
            e = self.events.popleft()


            player = self.domain.players[self.player]
            active_chara = player['party'][player['on_chara']]
                
            ## HANDLE INPUTS            
            # handle auto attack input
            if e.type == Event.ACTION_AUTO:
                active_chara.invoke_auto()
                self.swap_turn = True
                

            # handle charge attack input 
            elif e.type == Event.ACTION_CHARGE:
                active_chara.invoke_charge()
                self.swap_turn = True

            # handle elemental skill input
            elif e.type == Event.ACTION_SKILL:
                active_chara.invoke_skill()
                self.swap_turn = True

            # handle elemental burst input
            elif e.type == Event.ACTION_BURST:
                active_chara.invoke_burst()
                self.swap_turn = True

            # handle character switch input 
            # (change onfield character)
            elif e.type == Event.ACTION_SWITCH:
                player['on_chara'] = e.val
                
                # emit focus and blur events for all characters in party.
                for i in range(len(player['party'])):
                    if i == player['on_chara']:
                        self.events.append(Event(Event.CHARA_TAKES_FIELD, i))
                    else:
                        self.events.append(Event(Event.CHARA_LEAVES_FIELD, i))


            elif e.type == Event.CHARA_TAKES_FIELD:
                focus_target = e.val
                player['party'][focus_target].take_field()

            elif e.type == Event.CHARA_LEAVES_FIELD:
                blur_target = e.val
                player['party'][blur_target].leave_field()

            elif e.type == Event.GAME_OVER:
                self.winner = get_opponent(e.val)
                self.game_over = True
        
        

