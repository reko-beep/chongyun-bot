from core.paimon import Paimon

import logging

logger = logging.getLogger('nextcord')
logger.setLevel(logging.ERROR)

# client: Bot and paimon: Paimon (subclass of Bot) are same
pmon = Paimon(config_file="settings.json")
settings_data = pmon.get_config()



# start paimon bot.  
pmon.p_start()