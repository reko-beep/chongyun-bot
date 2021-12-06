from grpg.util import get_opponent
from grpg.Game import Game
from grpg.event import Event
import logging


# setup game
game = Game()
game.pick_domain("Zhou")
game.domain.add_player("A", "kaeya", "kaeya")
game.domain.add_player("B", "kaeya", "kaeya")

game.main_loop().__next__()




while True:
    key = input("enter value:")
    if key == 'a':
        game.events.append(Event(Event.ACTION_AUTO))
    elif key == 'c':
        game.events.append(Event(Event.ACTION_CHARGE))
    elif key == '0':
        game.events.append(Event(Event.ACTION_SWITCH, 0))
    elif key == '1':
        game.events.append(Event(Event.ACTION_SWITCH, 1))


    game.main_loop().__next__()

    logging.info("...................")
    party = game.domain.players[game.player]['party']
    for chara in party:
        logging.info(chara.get_stats())
    opponent = get_opponent(game.player)
    party = game.domain.players[opponent]['party']
    for chara in party:
        logging.info(chara.get_stats())
    
    logging.info(f"game over?: {game.game_over} {game.winner if game.game_over else ''}")
    logging.info("...................")
