from typing import ItemsView
from nextcord.embeds import Embed
from nextcord.errors import NotFound

import requests
from main import Fetcher
from bs4 import BeautifulSoup
import json
from logger import logc
from time import sleep
from json import dump,load
from nextcord import TextChannel, Guild
from datetime import datetime, timedelta
import re
import pytz

class Events(Fetcher):
    def __init__(self):
        self.types = ['Current', 'Upcoming','Permanent']
        super().__init__()

    def fetch_data(self, type: str):
        src = self.get('Events').content
        bs = BeautifulSoup(src, 'lxml')
        print(bs.find('span', {'id': type}).parent)
        table = bs.find('span', {'id': type}).parent
        events = []
        if table is not None:
            table = table.find_next_sibling()
            rows = table.find_all('tr')

            for row in rows[1:]:

                columns = row.find_all('td')

                check = (len(columns) == 3)
                if check:

                    name = columns[0].find('a').attrs['title']
                    link = columns[0].find('a').attrs['href']
                    img = self.find_image(columns[0].find('img'))
                    datetime_obj = columns[1].attrs['data-sort-value']
                    if len(self.extract_datetimes(datetime_obj)) != 0:
                        start, end = self.extract_datetimes(datetime_obj)
                    else:
                        start, end = 'N/A','N/A'
                    type_ = columns[2].text.strip()
                    status, time_stamp = self.get_status(start, end)
                    events.append( {
                        'name': name,
                        'link': f'https://genshin-impact.fandom.com/{link}',
                        'img': img,
                        'type': type_,
                        'start': start,
                        'end': end,
                        'status': status,
                        'timestamp': time_stamp,
                        'id': self.generate_key(name)
                    })
        return events

    def get_status(self, start, end):
        status = ''
        time_stamp = ''        
        time_region = 'Asia/Shanghai'
        now_utc_ = datetime.now(pytz.timezone('UTC'))
        current_time = now_utc_.astimezone(pytz.timezone(time_region))
        if start == end == 'N/A':
            status = start
            time_stamp = {'eu': 'N/A', 'asia': 'N/A', 'na': 'N/A'}
        else:
            start_obj = datetime.strptime(f'{start} +0800', '%Y-%m-%d %H:%M:%S %z')
            end_obj = datetime.strptime(f'{end} +0800', '%Y-%m-%d %H:%M:%S %z')
            if current_time < start_obj:
                status = 'Upcoming'
                time_stamp = self.region_times(start_obj, end_obj, current_time)
            if start_obj < current_time < end_obj:
                status = 'Ongoing'
                time_stamp = self.region_times(start_obj, end_obj, current_time)
            if current_time > end_obj:
                status = 'Ended'
                time_stamp= self.region_times(start_obj, end_obj, current_time) 

        return status, time_stamp
            
    def region_times(self, start_obj, end_obj, current_obj):
        eu_timestamp = ''
        na_timestamp = ''
        asia_timestamp = ''
        if current_obj < start_obj:
            eu_time = datetime.strptime(str(start_obj + timedelta(hours=7)), '%Y-%m-%d %H:%M:%S%z').timestamp()
            na_time = datetime.strptime(str(start_obj + timedelta(hours=13)), '%Y-%m-%d %H:%M:%S%z').timestamp()                     
            asia_time = start_obj.timestamp()   
            eu_timestamp  = f"starts <t:{str(eu_time).split('.')[0]}:R>"
            na_timestamp  = f"starts <t:{str(na_time).split('.')[0]}:R>"
            asia_timestamp  = f"starts <t:{str(asia_time).split('.')[0]}:R>"  
            
        if start_obj < current_obj < end_obj:
            eu_time = datetime.strptime(str(end_obj + timedelta(hours=7)), '%Y-%m-%d %H:%M:%S%z').timestamp()
            na_time = datetime.strptime(str(end_obj + timedelta(hours=13)), '%Y-%m-%d %H:%M:%S%z').timestamp()                     
            asia_time = end_obj.timestamp()    
            eu_timestamp  = f"ends <t:{str(eu_time).split('.')[0]}:R>"
            na_timestamp  = f"ends <t:{str(na_time).split('.')[0]}:R>"
            asia_timestamp  = f"ends <t:{str(asia_time).split('.')[0]}:R>"
        if current_obj > end_obj:
            eu_time = datetime.strptime(str(end_obj + timedelta(hours=7)), '%Y-%m-%d %H:%M:%S%z').timestamp()
            na_time = datetime.strptime(str(end_obj + timedelta(hours=13)), '%Y-%m-%d %H:%M:%S%z').timestamp()                     
            asia_time = end_obj.timestamp()  
            eu_timestamp  = f"ended<t:{str(eu_time).split('.')[0]}:R>"
            na_timestamp  = f"ended <t:{str(na_time).split('.')[0]}:R>"
            asia_timestamp  = f"ended <t:{str(asia_time).split('.')[0]}:R>"
        return {'eu': eu_timestamp, 'na':  na_timestamp, 'asia' : asia_timestamp}

        

        
    def extract_datetimes(self, str_):
        return re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str_)

               

    async def map_ids_message(self, fetch_list, existing_list, channel: TextChannel):
        list_ = []
        if len(existing_list) == 0:
            for item in fetch_list:
                embed = Embed(title=f"{item['name']}",url=f"{item['link']}")
                embed.add_field(name='Type',value=f"{item['type']}")
                embed.add_field(name='Status',value=f"{item['status']}")
                embed.add_field(name='Start',value=f"{item['start']}")
                embed.add_field(name='End',value=f"{item['end']}")
                embed.add_field(name='Asia',value=f"{item['timestamp']['asia']}")
                embed.add_field(name='EU',value=f"{item['timestamp']['eu']}")
                embed.add_field(name='NA',value=f"{item['timestamp']['na']}")
                embed.set_image(url=f"{item['image']}")                
                msg = await channel.send(embed=embed)
                item['message'] = msg.id
            existing_list = fetch_list
        else:
            list_ = []
            statuses = [i['status'] for i in fetch_list]
            ids = [i['id'] for i in fetch_list]
            for exist in existing_list:
                if exist in ids:
                    if statuses[ids.index(exist)] != exist['status']:
                        item = fetch_list[ids.index(exist)]
                        embed = Embed(title=f"{item['name']}",url=f"{item['link']}")
                        embed.add_field(name='Type',value=f"{item['type']}")
                        embed.add_field(name='Status',value=f"{item['status']}")
                        embed.add_field(name='Start',value=f"{item['start']}")
                        embed.add_field(name='End',value=f"{item['end']}")
                        embed.add_field(name='Asia',value=f"{item['timestamp']['asia']}")
                        embed.add_field(name='EU',value=f"{item['timestamp']['eu']}")
                        embed.add_field(name='NA',value=f"{item['timestamp']['na']}")
                        embed.set_image(url=f"{item['image']}")
                        if item['message'] != 0:
                            try:
                                await channel.fetch_message(item['message'])
                            except NotFound:
                                msg = await channel.send(embed=embed)
                                item['message'] = msg.id
                                exist = item
                            else:
                                await channel.edit(embed=embed)
                                exist = item
                            list_.append(exist)
                else:
                    try:
                        msg = await channel.fetch_message(item['message'])
                    except NotFound:
                        pass
                    else:
                        await msg.delete()
            
            # recursive

            ids = [i['id'] for i in list_]    

            for fetch in fetch_list:
                if fetch['id'] in ids:
                    pass
                else:
                    item = fetch
                    embed = Embed(title=f"{item['name']}",url=f"{item['link']}")
                    embed.add_field(name='Type',value=f"{item['type']}")
                    embed.add_field(name='Status',value=f"{item['status']}")
                    embed.add_field(name='Start',value=f"{item['start']}")
                    embed.add_field(name='End',value=f"{item['end']}")
                    embed.add_field(name='Asia',value=f"{item['timestamp']['asia']}")
                    embed.add_field(name='EU',value=f"{item['timestamp']['eu']}")
                    embed.add_field(name='NA',value=f"{item['timestamp']['na']}")
                    embed.set_image(url=f"{item['image']}")
                    if item['message'] != 0:
                        try:
                            await channel.fetch_message(item['message'])
                        except NotFound:
                            msg = await channel.send(embed=embed)
                            item['message'] = msg.id
                            exist = item
                        else:
                            await channel.edit(embed=embed)
                            exist = item
                        list_.append(exist)
                    else:
                        msg = await channel.send(embed=embed)
                        item['message'] = msg.id
                        fetch = item
            existing_list = list_

        
                  
                    



    


        



test = Events()
data = test.fetch_data('Current')
