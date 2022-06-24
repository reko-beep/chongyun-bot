
from nextcord import Embed, Guild
from nextcord.utils import get
from nextcord.ext.commands import Bot
from dev_log import logc

def paginator(bot: Bot, guild: Guild, data:dict, title:str, field_str: str, limit:int):
        keys_ = list(data.keys())
        pages = 0
        pages_ = divmod(len(keys_), limit)
        embeds = []
        pages = pages_[0]
        if pages_[1] != 0:
            pages  = pages_[0]+1
        print(pages ,len(keys_))
        for pag in range(1, pages +1, 1):
            
            descrip = ''
            for itm in range(1, len(keys_) + 1, 1):

                index = itm-1
                if (pag*limit)-limit < itm < pag*limit:
                    user = None
                    key = ''
                    if keys_[index].isdigit():
                        user = get(guild.members, id=int(keys_[index]))                

                    value = data[keys_[index]]

                    if user is not None:
                        key = user.display_name
                    else:
                        key = keys_[index]
                    descrip += f"{field_str.format(key=key, value=value)}\n"
            if descrip == '':
                descrip = 'Such Emptiness'
            color = bot.resource_manager.get_color_from_image(bot.user.avatar.url)
            embed = Embed(title=title,description=descrip, color=color)
            embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embeds.append(embed)
        
        return embeds

def get_ordered_dicts(dictionary: dict):
        sort_orders = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
        return sort_orders