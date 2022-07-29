from dis import disco
from json import load, dump
from base.resource_manager import ResourceManager
import random

from nextcord import Guild, Member, Embed
from nextcord.utils import get
from os.path import exists
from os import getcwd
from datetime import datetime
from nextcord.ext.commands import Context
class LibenManager:
    def __init__(self, bot):

        self.bot = bot
        self.res : ResourceManager = bot.resource_manager
        self.enabled = self.bot.b_config.get('liben')
        self.lb_data = self.load()        
    
    def load(self):

        path = self.res.db.format(path='liben.json')

        if exists(path):
            with open(path, 'r') as f:
                return load(f)
        return {}

    def save(self):
    
        path = self.res.db.format(path='liben.json')
        
        with open(path, 'w') as f:
            dump(self.lb_data, f, indent=1)
  
    def get_server_region(self, **kwargs):
        from_uid = kwargs.get("uid", -1)
        region_str = kwargs.get("region", '').lower()
        print(region_str)
        if from_uid != -1:
            uid = from_uid
            if type(from_uid) == int:
                uid = str(from_uid)
            
            if uid[0] == '8':
                return 'asia'
            if uid[0] == '7':
                return 'eu'
            if uid[0] == '6':
                return 'na'
           
        if region_str != '':
            allowed :list = ['asia','asia','eu','europe','na','northamerica']
            
            try:
                index = allowed.index(region_str)
                print('index found', index)
            except ValueError:                
                pass
            else:              
                if index % 2 != 0:                    
                    return allowed[index-1]
                else:
                    return allowed[index]

    def add_box(self,member: Member, uid: str, box:str):
        allowed = ['pyro', 'geo', 'electro', 'anemo', 'cryo', 'hydro', 'dendro']
        region = self.get_server_region(uid=uid)
        box = box.lower()
        if region is not None:
            discord_id = str(member.id)
            if discord_id not in self.lb_data:
                if box in allowed:
                    self.lb_data[discord_id] = {
                        'box' : box,
                        'uid': uid,
                        'region' : region,
                        'claimed' : [],
                        "users": []

                    }
            else:
                if self.lb_data[discord_id]['box'] != box:
                    self.lb_data[discord_id]['claimed'] = []
                    self.lb_data[discord_id]['users'] = []
                self.lb_data[discord_id]['box'] = box
                self.lb_data[discord_id]['uid'] = uid
                self.lb_data[discord_id]['region'] = region
            self.save()
            return True
        return None

           

        
    
    def get_boxes(self, member: Member, region:str, box:str):

        allowed = ['eu','asia','na']
        region = region.lower()
        box = box.lower()
        boxes = []
        if region in allowed:
            for id_ in self.lb_data:
                if self.lb_data[id_]['box'] == box and self.lb_data[id_]['region'] == region:
                    if member.id not in self.lb_data[id_]['users']:                    
                        boxes.append({**self.lb_data[id_], **{'member': id_}})

        return boxes if len(boxes) > 0 else None


                
    
    def get_timestamp(self):

        now_time = str(datetime.now().timestamp()).split('.')[0]

        return "<t:"+now_time+":R>"

    def add_claimed(self, emoji,  member: Member, region:str, box:str, user_claimed: Member):
        region = region.lower()
        box = box.lower()
        box_fetched = self.get_boxes(user_claimed, region, box)       
        box_final = [f['member'] for f in box_fetched if f['member'] == str(member.id)][0] if len([f['member'] for f in box_fetched if f['member'] == str(member.id)])> 0 else None       
        if box_final is not None:
            self.lb_data[box_final]['claimed'].append(emoji+" "+self.get_timestamp())
            self.lb_data[box_final]['users'].append(user_claimed.id)
            self.save()
            return True


    def remove_box(self, member):
        discord_id = member
        if discord_id in self.lb_data:
            self.lb_data.pop(discord_id)
            self.save()
            return True


    def get_random_box_embed(self,guild: Guild, box:dict):
        
      

        user = get(guild.members, id=int(box['member']))
        desc_ = f"**UID**\: *{box['uid']}*\n**Region:**: *{box['region'].upper()}*"
        embed = Embed(title=f"{box['box'].title()} box", description=desc_, color=self.res.get_color_from_image(user.display_avatar.url))
        emoji = self.bot.inf.res_handler.search(box['box'],self.bot.inf.res_handler.goto('images/elements').get('files'))

        
        print(emoji)
        if emoji is not None:
            gen = self.bot.inf.res_handler.convert_to_url(self.bot.inf.res_handler.genpath('images/elements', emoji.replace(' ','%20',99)), True)
            print(gen)
            embed.set_thumbnail(url=gen)
      
        
        if len(box['claimed']) != 0:
            claim = box['claimed']
            if len(box['claimed']) > 5:
                claim = box[-4:]
            claimed_text = '\n'.join(claim)
        else:
            claimed_text = 'No one has claimed from this user yet!'
        embed.add_field(name='Claimed', value=claimed_text)
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.set_footer(text='please confirm from the user before for element box!')

        return embed




