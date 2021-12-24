from os import getcwd, remove
import os
from json import dump,load

import genshinstats as gs
from datetime import datetime
import nextcord
from nextcord.ext.commands import Context
from nextcord.utils import get
from nextcord import Embed, File, TextChannel
from io import BytesIO
from PIL import Image
from core.paimon import Paimon
from base.administration import AdministrationBase
from util.logging import log
import requests
import pytz

class Domains:
    def __init__(self, pmon: Paimon):
        self.admin = AdministrationBase(pmon)
        self.pmon = pmon
        self.file = f'{getcwd()}/assets/domains_message.json'

        self.message_storage_list = []
        self.domains = {}
        self.domain_channel = None
        self.load_message_storage_list()
        self.load_domains()

    def set_domain_channel(self, ctx: Context, channel: TextChannel):
        check = self.admin.role_check(self.pmon.p_bot_config['mod_role'], [r.id for r in ctx.author.roles])
        if check:
            if 'domain_channel' in self.pmon.p_bot_config:
                self.pmon.p_bot_config['domain_channel'] = channel.id
                self.pmon.p_save_config('settings.json')
                self.domain_channel = channel
                self.pmon.reload_extension('extensions.extra.domain')
                return True
            else:
                self.pmon.p_bot_config['domain_channel'] = channel.id
                self.pmon.reload_extension('extensions.extra.domain')
                self.pmon.p_save_config('settings.json')
                return True

    async def load_domain_channel(self, guild):
        if 'domain_channel' in self.pmon.p_bot_config:
            self.domain_channel = guild.get_channel(self.pmon.p_bot_config['domain_channel'])
            log('loaded domain channel', self.domain_channel)
            if os.path.exists(self.file):
                remove(self.file)
            await self.update_event('',self.domain_channel)

            return True
        

    def load_domains(self):
        with open(f'{getcwd()}/assets/domains.json','r') as f:
            self.domains = load(f)
    
    def search_rotation(self,type, domain_id, day):
        day = day.lower()

        search_result = []

        if type in self.domains:
            for domain in self.domains[type]:
                if domain['id'] == domain_id:
                    rewards = domain['rewards']
                    for reward in rewards:
                        days_check = [d.lower() for d in reward['days']]
                        if day in days_check:
                            search_result.append({
                                'domain_name': domain['name'],
                                'area' : domain['area'],
                                'image' : domain['image'],
                                'rotation': reward['name'],
                                'rewards': reward['items'],
                                'type': self.prettify(type)
                            })
        return search_result
        
    def prettify(self, string: str):
        return string.replace('_',' ',99).title()

    def search_domain_for_day(self,day):
        day = day.lower()
        search_result = []
        for type in self.domains:
            for domain in self.domains[type]:            
                rewards = domain['rewards']
                for reward in rewards:
                    days_check = [d.lower() for d in reward['days']]
                    if day in days_check:
                        search_result.append({
                            'domain_name': domain['name'],
                            'area' : domain['area'],
                            'rotation': reward['name'],
                            'rewards': reward['items'],
                            'type': self.prettify(type)
                        })
        return search_result

    def search_for_domain(self, type, nation, day):
        if type in self.domains:
            search_dict = self.domains[type]

            for domain_ in search_dict:
                if nation.lower() in domain_['nation'].lower():
                    if day.lower() in [da.lower() for da in domain_['days']]:
                        return domain_

    def create_image(self, images_list ):
        
        with open(f'{getcwd()}/assets/domain_template_image.json','r') as f:
            template =  load(f)
        new = Image.new(mode='RGBA',size=(template['dimensions']['width'],template['dimensions']['height']))
        images = {}
        for c, i in enumerate(images_list,1):
            images[str(c)] = i
        
        for image in images:
            url = images[image]
            x_pos = template[image]['x']
            y_pos = template[image]['y']
            r = requests.get(url).content        
            paste_ = Image.open(BytesIO(r))
            new.paste(paste_, (x_pos,y_pos))
        buffer = BytesIO()
        new.save(buffer,format='PNG')
        buffer.seek(0)
        return File(buffer, filename='image.png')


    def generate_message_storage_list(self):
        message_lists = [{
                    'nation': 'mondstadt',
                    'type': 'talent_levelup_materials',
                    'message': 0
                },
                {
                    'nation': 'mondstadt',
                    'type': 'weapon_ascension_materials',
                    'message': 0
                },
                {
                    'nation': 'liyue',
                    'type': 'weapon_ascension_materials',
                    'message': 0
                },
                {
                    'nation': 'liyue',
                    'type': 'talent_levelup_materials',
                    'message': 0
                },
                {
                    'nation': 'inazuma',
                    'type': 'weapon_ascension_materials',
                    'message': 0
                },
                {
                    'nation': 'inazuma',
                    'type': 'talent_levelup_materials',
                    'message': 0
                }]
        return message_lists

    def load_message_storage_list(self):
        if os.path.exists(self.file):
            with open(self.file,'r') as f:
                self.message_storage_list = load(f)

    def save_message_storage_list(self):        
        with open(self.file,'w') as f:
            dump(self.message_storage_list,f)

    def create_embed(self, domain_dict, day):
        description = f"**Type:** {self.prettify(domain_dict['type'])}\n**Nation:** {self.prettify(domain_dict['nation'])}\n**Area:** {domain_dict['area']}"
        embed = Embed(title=f"{domain_dict['area']} | {day.title()} Rotation",description=description,color=0xf5e0d0)
        

        embed.add_field(name='Farmed for', value='\n'.join(domain_dict['characters']))
        embed.add_field(name='Item', value=domain_dict['books'])
        image = self.create_image(domain_dict['images'])
        embed.set_image(url=f'attachment://image.png')
        return embed, image

    def map_area_type_to_domain_details(self,day: str = ''):
        if len(self.message_storage_list) == 0:
            self.message_storage_list = self.generate_message_storage_list()
        
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day == '':           

            day = days[datetime.now().weekday()]
        else:
            if day not in days:
                return None
        dict_ = {}

        for message in self.message_storage_list:
            domain = self.search_for_domain(message['type'],message['nation'],day)
            embed, image = self.create_embed(domain, day)
            dict_[f"{message['nation'].title()} {message['type'].replace('_',' ',99).title()}"] = {'embed': embed, 'image': image}
        return dict_


    async def update_event(self, day:str= '' , channel: TextChannel = None):
        time_region = time_region = 'Asia/Karachi'
        now_utc_ = datetime.now(pytz.timezone('UTC'))
            # Convert to Asia/Kolkata time zone
        day_time = now_utc_.astimezone(pytz.timezone(time_region))
        check = None
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day == '':         

            day = days[day_time.weekday()]
        else:
            if day not in days:
                return None
        if day == 'sunday':
            return None
        if channel is None:
            channel = self.domain_channel
        if len(self.message_storage_list)  == 0:
            self.message_storage_list = self.generate_message_storage_list()
            self.save_message_storage_list()
        for message in self.message_storage_list:
            domain = self.search_for_domain(message['type'],message['nation'],day)
            embed, image = self.create_embed(domain,day)

            if message['message'] == 0:
                if channel is not None:                    
                    message_sent = await channel.send(embed=embed, file=image)
                    message['message'] = message_sent.id
                    self.save_message_storage_list()
                    check = True
            else:
                if channel is not None:  
                    try:
                        message_sent = await channel.fetch_message(message['message'])
                    except nextcord.errors.NotFound:
                        message_sent = await channel.send(embed=embed, file=image)
                        message['message'] = message_sent.id
                        self.save_message_storage_list()
                    else:
                        if message_sent is not None:
                            await message_sent.delete()
                        message_sent = await channel.send(embed=embed, file=image)
                        message['message'] = message_sent.id
                        self.save_message_storage_list()
                        check = True
        return check
        

