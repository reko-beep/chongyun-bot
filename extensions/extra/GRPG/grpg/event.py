class Event:
    """
    Defines all types of game events handled by the event handler \n
    
    Input to the game should be given only by Events.
    Events are also created internally by the game to broadcast any event occured
    
    """

    # event constants.
    ACTION_AUTO = 0x001
    ACTION_CHARGE = 0x002
    ACTION_SKILL = 0x003
    ACTION_BURST = 0x004
    ACTION_SWITCH = 0X009
    ACTION_PLUNGE = 0x00A
    CHARA_TAKES_FIELD = 0x005
    CHARA_LEAVES_FIELD = 0x006
    CHARA_FALL = 0x007
    CHARA_REVIVE = 0x008
    GAME_OVER = 0x0B

    def __init__(self, type, val=None):
        self.type = type
        self.val = val
        

