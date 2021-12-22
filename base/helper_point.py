from nextcord import Member, Role, Embed 
from nextcord.ext.commands import Context
from core.paimon import Paimon
from nextcord.utils import get
from os import getcwd
from os.path import exists

from json import load, dump

class HelperBase:
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        self.path = f'{getcwd()}/assets/helper_points.json'
        self.helper_points = {}
        self.load()

    def load(self):
        if exists(self.path):
            with open(self.path, 'r') as f:
                self.helper_points = load(f)

    def save(self):        
        with open(self.path, 'w') as f:
            dump(self.helper_points, f,indent = 1)


    def add_helper_point(self, ctx: Context, member: Member):
        asker_id = ctx.author.id
        if asker_id in self.pmon.p_bot_config['asker_id']:
            id_ = str(member.id)
            if id_ in self.helper_points:
                self.helper_points[id_] += 1
            else:
                self.helper_points[id_] = 1
            self.pmon.p_bot_config['asker_id'].pop(self.pmon.p_bot_config['asker_id'].index(ctx.author.id))
            self.pmon.p_save_config('settings.json')
            self.save()
            return True
    
    def reset_lb(self, ctx):
        r = [r.id for r in ctx.author.roles]
        
        if len(set(r).intersection(self.pmon.p_bot_config['mod_role'])) != 0:
            for key in self.helper_points:
                self.helper_points[key] = 0
            self.save()
            return True
    

    def add_asker(self , member: Member, roles_list):
        r = [r.id for r in roles_list]
        if len(set(r).intersection(self.pmon.p_bot_config['carry_roles'])) != 0:
            if member.id not in self.pmon.p_bot_config['askers_banned']:
                self.pmon.p_bot_config['asker_id'].append(member.id)
                self.pmon.p_save_config('settings.json')
                return True
            return False
            
    def get_ordered_dicts(self):
        sort_orders = dict(sorted(self.helper_points.items(), key=lambda x: x[1], reverse=True))
        return sort_orders




    def create_lbpages(self, limit):
        embeds = {}
        dict_ = self.get_ordered_dicts()
        count = divmod(len(list(dict_.keys())), limit)        
        keys = list(dict_.keys())
        if len(keys) == 0:
            embed = Embed(title=f'Co-op leaderboard', description='Such emptiness!', color=0xf5e0d0) 
            embed.set_thumbnail(url='https://i.imgur.com/CDYa78r.png')
            embeds['Page 1'] = embed
        else:
            page_count = count[0]
            if count[1] != 0:
                page_count += 1
            emoji = get(self.pmon.guilds[0].emojis, name="coop")
            for page_index in range(1, page_count+1 , 1):
                
                description = ''
                for index in range(len(keys)):
                    if (page_index * limit)-limit-1 < index < ( page_index* limit):
                        id_ = int(keys[index])
                        member = get(self.pmon.guilds[0].members, id=id_)
                        value = self.helper_points[keys[index]]
                        if member is not None:
                            description += f" {index+1}. **{member}** - {value} {emoji}\n"
                embed = Embed(title=f'Co-op leaderboard ({page_index}/{page_count})', description=description, color=0xf5e0d0) 
                embed.set_thumbnail(url='https://i.imgur.com/CDYa78r.png')
                embeds[f'Page {page_index}'] = embed
        return embeds

    def get_coopoint(self, member: Member):
        id_ = str(member.id)
        if id_ in self.helper_points:
            value = self.helper_points[id_]
            embed = Embed(title=f'{member.display_name} Co-op Points!',description=f'Has {value} co-op points!',color=0xf5e0d0) 
            embed.set_author(name=member.display_name,icon_url=member.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/CDYa78r.png')
            return embed

    def get_eligible_points(self, member: Member):
        id_ = member.id
        count = self.pmon.p_bot_config['asker_id'].count(id_)
        return count

    def remove_eligible_points(self, ctx, member: Member):
        id_ = member.id
        r = [r.id for r in ctx.author.roles]
        
        if len(set(r).intersection(self.pmon.p_bot_config['mod_role'])) != 0:
            print(self.pmon.p_bot_config['asker_id'])
            list_ = [i for i in self.pmon.p_bot_config['asker_id'] if i != id_]
            print(list_)
            self.pmon.p_bot_config['asker_id'] = list_
            self.pmon.p_save_config('settings.json')
            return True
        
    def ban_asker(self, ctx, member: Member):
        id_ = member.id
        r = ctx.author.id        
        if r in self.pmon.p_bot_config['owner_id']:            
            self.pmon.p_bot_config['askers_banned'].append(id_)
            self.pmon.p_save_config('settings.json')
            return True

    def removeban_asker(self, ctx, member: Member):
        id_ = member.id
        r = ctx.author.id        
        if r in self.pmon.p_bot_config['owner_id']:     
            list_ = [r_ for r_ in self.pmon.p_bot_config['askers_banned'] if r_ != id_]       
            self.pmon.p_bot_config['askers_banned'] = list_
            self.pmon.p_save_config('settings.json')
            return True

