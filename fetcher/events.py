from typing import ItemsView, Text
from nextcord.embeds import Embed
from nextcord.errors import NotFound

import requests
from fetcher.main import Fetcher
from bs4 import BeautifulSoup
import json
from time import sleep
from json import dump,load
from nextcord import TextChannel, Guild, message
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
                        'name': name.split('/')[0],
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

               





    async def update_event_list(self, channel):
        local_events = self.load_data()

        # fetch events from upstream. (ongoing and upcoming)
        upstream_ongoing_data = self.fetch_data('Current')
        upstream_upcoming_data = self.fetch_data('Upcoming')
        upstream_event_data = upstream_ongoing_data + upstream_upcoming_data
      
        upstream_ongoing = set([event['id'] for event in upstream_ongoing_data])
        upstream_upcoming = set([event['id'] for event in upstream_upcoming_data])
      

        # filter new data
        new_upcoming = upstream_upcoming - set(local_events['upcoming'].keys())

        # send messages for new data
        for event_id in new_upcoming:
            event = next(filter(lambda edata: edata['id'] == event_id, upstream_event_data), None)
            msg_id = await self.create_event_msg(event, channel)
            local_events['upcoming'][event_id] = msg_id


        # update messages for new data (upcoming > ongoing)
        new_ongoing = upstream_ongoing - set(local_events['ongoing'].keys())
        
        for event_id in new_ongoing:
            
            event = next(filter(lambda edata: edata['id'] == event_id, upstream_event_data), None)

            try:
                # new_ongoing event means its moved from upcoming to ongoing.
                msg_id = local_events['upcoming'][event_id]
                del local_events['upcoming'][event_id]
                local_events['ongoing'][event_id] = msg_id

                # edit message status from upcoming to ongoing
                await self.update_event_msg(event, msg_id, channel)
            
            except Exception:
                # keyerror implies first run, just populate the ongoing list.
                msg_id = await self.create_event_msg(event, channel)
                local_events['ongoing'][event_id] = msg_id  


        # remove old ongoing data.
        old_ongoing = set(local_events['ongoing'].keys()) - upstream_ongoing
        for event_id in old_ongoing:
            msg_id = local_events['ongoing'][event_id]
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
            del local_events['ongoing'][event_id]

    
        self.save_data(local_events)


    async def create_event_msg(self, event, channel: TextChannel):
        """
        creates an event message for the given event\n
        returns the message's ID
        """
        embed = self.create_embed(event)
        msg = await channel.send(embed=embed)
        return msg.id

    

    async def update_event_msg(self, event, msg_id, channel: TextChannel):
        """
        updates an event message for the given event
        """
        embed = self.create_embed(event)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(embed=embed)

    def create_embed(self, event):
        embed = Embed(title=f"{event['name']}",url=f"{event['link']}",color=0xf5e0d0)
        embed.add_field(name='Type',value=f"{event['type']}")
        embed.add_field(name='Status',value=f"{event['status']}")
        embed.add_field(name='Start',value=f"{event['start']}")
        embed.add_field(name='End',value=f"{event['end']}")
        embed.add_field(name='Asia',value=f"{event['timestamp']['asia']}")
        embed.add_field(name='EU',value=f"{event['timestamp']['eu']}")
        embed.add_field(name='NA',value=f"{event['timestamp']['na']}")
        embed.set_image(url=f"{event['img']}")
        return embed
    
    def load_data(self):
        with open('genshin_events_list.json','r') as f:
            return json.load(f)
    
    def save_data(self, data):
        with open('genshin_events_list.json', 'w') as f:
            json.dump(data, f)

