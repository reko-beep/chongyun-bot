import os
import nextcord as discord
from nextcord.ext import commands,tasks
import json
import requests
from bs4 import BeautifulSoup
import pprint

class GenshinEvents:
    def __init__(self,bot):
        self.last = ''
        self.current = ''
        self.url = 'https://genshin-impact.fandom.com/wiki/Events#Current'
        self.events = {}
        self.bot = bot
        self._load()

    def _load(self):
        if os.path.exists('events.json'):
            with open('events.json','r') as f:
                self.last = json.load(f)['last_id']


    def fetch(self,str_:str):
        r = requests.get(self.url).content
        bs = BeautifulSoup(r,'lxml')
        heading = bs.find_all('h2')
        table = 0
        for i in heading:
            if i.text.lower() == str_:
                table = i.findNextSibling()        
        if table != 0:    
            events = table.find_all('tr')                      
            elements = ['name','duration','type']
            for ev in events[1:]:
                temp_ = {'name':'','image':'','link':'','duration':'','duration':''}                
                data = ev.find_all('td')   
                print()
                if events[len(events)-1] != None:
                    if events[len(events)-1].find_all('td')[0] != None:
                        check = events[len(events)-1].find_all('td')[0].find('a').attrs['title'].replace(' ','_',99).replace('-','',99).replace("'","",99).lower()
                print(check,self.last)    
                if check != self.last:    
                    for i in range(0,len(data),1):                    
                        if data[i].find('a') != None:
                            self.current = data[i].find('a').attrs['title'].replace(' ','_',99).replace('-','',99).replace("'","",99).lower()
                            temp_['link'] = f"https://genshin-impact.fandom.com/{data[i].find('a').attrs['href'] }"
                            temp_['name'] = data[i].find('a').attrs['title']    
                            if data[i].find('img') != None:
                                if 'data-src' in data[i].find('img').attrs:
                                    temp_['image'] = data[i].find('img').attrs['data-src'][:data[i].find('img').attrs['data-src'].find('/revision')]  
                        else:                    
                            temp_[elements[i]] = data[i].text                
                    if self.current != self.last:
                        if self.current not in self.events:
                            self.events[self.current] = temp_
                            self.last = self.current
                    else:
                        break
            self.events['last_id'] = self.last            
            with open('events.json','w') as f:
                json.dump({'last_id': self.last},f)
            return self.events

    def create_embed(self,data):
        embed = discord.Embed(title=f"{data['name']}",description=f"[Link]({data['link']})\n\n**Duration:**\n {data['duration']}\n\n**Type:**\n{data['type']}",color=0xf5e0d0)
        file = discord.File(f'{os.getcwd()}/guides/paimon/happy.png',filename='happy.png')        
        embed.set_author(name='Paimon brings you event',icon_url=self.bot.user.avatar.url)
        if 'image' in data:
            if data['image'].startswith('http'):
                embed.set_image(url=f"{data['image']}")   
        embed.set_thumbnail(url=f'attachment://happy.png')
        return embed,file
           
        

