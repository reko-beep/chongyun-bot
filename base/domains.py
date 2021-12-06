from os import getcwd
import os
from json import dump,load

import genshinstats as gs
from datetime import datetime

from nextcord import TextChannel
import nextcord
from nextcord.ext.commands import Context
from nextcord.utils import get
from nextcord import Embed

from core.paimon import Paimon
from base.administration import AdministrationBase


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

    def load_domain_channel(self):
        if 'domain_channel' in self.pmon.p_bot_config:
            self.domain_channel = self.pmon.guilds[0].get_channel(self.pmon.p_bot_config['domain_channel'])
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

    def generate_message_storage_list(self):
        message_lists = []
        for type in self.domains:
            for domain in self.domains[type]:
                message_lists.append({
                    'id': domain['id'],
                    'type': type,
                    'message': 0
                })
        return message_lists

    def load_message_storage_list(self):
        if os.path.exists(self.file):
            with open(self.file,'r') as f:
                self.message_storage_list = load(f)

    def save_message_storage_list(self):
        with open(self.file,'w') as f:
            dump(self.message_storage_list,f)

    def create_embed(self,domain_data: list, day: str):
        dict_data = domain_data[0]
        description = f"\n**Area:**\n{dict_data['area']}\n**Rotation:**\n{dict_data['rotation']}\n**Type:**\n{dict_data['type']}\n**Rewards:**\n"
        if len(dict_data['rewards']) != 0:
            for reward in dict_data['rewards']:
                description += f"{('⭐' * reward['rarity'] )} {reward['name']}\n"
        embed = Embed(title=f"{dict_data['domain_name']} | {day.title()} Rotation",description=description,color=0xf5e0d0)
        if dict_data['image'] != '':
            embed.set_thumbnail(url=dict_data['image'])
        return embed

    async def embeds_list(self, day:str= '' , channel: TextChannel = None):
        check = None
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day == '':           

            day = days[datetime.now().weekday()]
        else:
            if day not in days:
                return None
        if channel is None:
            channel = self.domain_channel

        if len(self.message_storage_list)  == 0:
            self.message_storage_list = self.generate_message_storage_list()
            self.save_message_storage_list()
        embeds = {}
        for message in self.message_storage_list:
            domain = self.search_rotation(message['type'],message['id'],day)
            embed = self.create_embed(domain,day)
            embeds[message['id'].replace('_',' ',99).title()] = embed
        return embeds



    async def update_event(self, day:str= '' , channel: TextChannel = None):
        check = None
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day == '':           

            day = days[datetime.now().weekday()]
        else:
            if day not in days:
                return None
        if channel is None:
            channel = self.domain_channel

        if len(self.message_storage_list)  == 0:
            self.message_storage_list = self.generate_message_storage_list()
            self.save_message_storage_list()
        for message in self.message_storage_list:
            domain = self.search_rotation(message['type'],message['id'],day)
            embed = self.create_embed(domain,day)

            if message['message'] == 0:
                if channel is not None:                    
                    message_sent = await channel.send(embed=embed)
                    message['message'] = message_sent.id
                    self.save_message_storage_list()
                    check = True
            else:
                if channel is not None:  
                    try:
                        message_sent = await channel.fetch_message(message['message'])
                    except nextcord.errors.NotFound:
                        message_sent = await channel.send(embed=embed)
                        message['message'] = message_sent.id
                        self.save_message_storage_list()
                    else:
                        if message_sent is not None:
                            await message_sent.edit(embed=embed)
                            check = True
        return check
        

