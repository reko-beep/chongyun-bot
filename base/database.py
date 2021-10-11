import os
from pprint import pprint
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json
import genshinstats as gs
class GenshinDB(dict):
    def __init__(self):
        self.path = os.getcwd()
        self.file = 'genshin.json'
        self.data = {}
        self.allowed = ['eu','na','asia']
        self.ltoken = 'tJLdlousrYagG8jky6vKNJpKWnqS8joxuby1D3mS'
        self.ltuid = 6457775
        self.__load()
        print(self.data)

    def __load(self):
        if os.path.exists('genshin.json'):
            with open('genshin.json','r') as f:
                self.data = json.load(f)
    
    def __save(self):
        if os.path.exists('genshin.json'):
            os.remove('genshin.json')
        with open('genshin.json','w') as f:
            json.dump(self.data,f,indent=1)
    
    def if_multiple(self,id_):
        if id_ in self.data:
            if 'servers' in self.data[id_]:
                if len(self.data[id_]['servers']) > 1:
                    return True
                else:
                    return False
            return None
        return None


    def get_servers(self,id_):
        if id_ in self.data:
            if 'servers' in self.data[id_]:                
                return self.data[id_]['servers']




    def get_uid(self,id_,server): #getting uid for a discord user
        check = self.if_multiple(id_)
        print(check)    
        if server in self.data[id_]['servers']:
            print(self.data[id_]['servers'][server])
            return self.data[id_]['servers'][server]
        else:
            if 'none' in self.data[id_]['servers']:
                return self.data[id_]['servers']['none']        
        return None
    
    def save_server(self,id_,name,uid):
        temp_ = {}
        if id_ in self.data:
            if 'servers' in self.data[id_]:
                if name in self.data[id_]['servers']:
                    self.data[id_]['servers'][name] = uid
                    print(f'server updated, {temp_}')
                else:
                    if name in self.allowed:
                        temp_ = self.data[id_]['servers']
                        temp_[name] = uid
                        self.data[id_]['servers'] = temp_
                        print(f'server added, {temp_}')
            else:
                temp_ = self.data[id_]
                if name in self.allowed:
                    temp_['servers'] = {name: uid}
                    self.data[id_] = temp_
                print(f'server key was not found now added, {temp_}')
        else:            
            if name in self.allowed:
                temp_['servers'] = {name: uid}
                self.data[id_] = temp_
                print(f'ID was not found, {temp_}')
        print(self.data)
        if id_ in self.data:
            return self.data[id_]
                    

    def serveruid(self, id_,string_passed): #to save uids
        temp_ = ''
        strings_ = []
        saved = False
        if '\n' in string_passed:
            strings_ = string_passed.split('\n')
        else:
            strings_ = [string_passed]
        servers = ['eu:europe','asia:asia','na:northamerica']
        check = 0
        for string in strings_:
            print(string)
            if ':' in string:
                temp_ = string.split(':')   
                print(f'temp step {temp_}')     
                for server in servers:
                    print(f'Written server {temp_[0].lstrip().rstrip().lower()}')
                    if temp_[0].lstrip().rstrip().lower() in server.split(':'):
                        print(f"server found {server.split(':')[0]}")
                        serv_ = server.split(':')[0]
                        if temp_[1].lstrip().rstrip().isdigit():
                            uid = int(temp_[1])
                            check = self.save_server(id_,serv_,uid)
                            saved = True
                            break
            else:
                if string.isdigit():
                    print(string)
                    serv_ = 'none'
                    uid = int(string)
                    check = self.save_server(id_,serv_,uid)
                    saved = True
        self.__save()
        return check,saved
            
    def get_uiddata(self,uid): #getting uidata
        data = {}
        try:
            gs.set_cookie(ltuid=self.ltuid,ltoken=self.ltoken)
            data = {}
            if isinstance(uid,int):
                data = gs.get_all_user_data(uid)
            else:
                data = gs.get_all_user_data(uid)
            return data
        except gs.errors.DataNotPublic:
                return None

    
    def get_gstats(self,data):        
        if len(data) > 1:
            stats = data['stats']
            temp_ = {}
            for i in stats:
                if i != 'icon':
                    temp_[i.replace('_'," ",99).title()] = stats[i]
            return temp_,data['characters'][0]['icon']
    
    def get_characters(self, data):
        c_ = 0
        temp_ = []
        weapons_ = []
        id_ = ''
        if len(data) > 1:
            if 'characters' in data:
                for i in data['characters']:
                    temp__ = {}
                    for c in i:  
                        if c == 'id':
                            id_ = i[c]  
                        else:
                            if c == 'weapon':
                                weapons_.append(i[c])
                            else:                       
                                temp__[c] = i[c]           
                    
                    temp_.append(temp__) 
                
                return temp_,weapons_
                

    def create_stats_embed(self, uid_data:dict):
        if len(uid_data) > 1:
            stats,icon = self.get_gstats(uid_data)
            embed = discord.Embed(title=f'Genshin Impact Profile stats',description="",color=0xf5e0d0)
            for i in stats:
                embed.add_field(name=f'{i}',value=f'{stats[i]}',inline=True)
            embed.set_thumbnail(url=icon)
            return embed

    def create_characters_embed(self,uid_data:dict):
        embeds = {}
        if len(uid_data) > 1:
            characters_,weapons = self.get_characters(uid_data)
            print(range(0,len(characters_),1))
            for no in range(0,len(characters_),1):
                print(characters_[no])   
                print('weapon')
                print(weapons[no])               
                embed_char = discord.Embed(title=f"{characters_[no]['name']}",color=0xf5e0d0)
                embed_weapon = discord.Embed(title=f"{characters_[no]['name']} {weapons[no]['name']}",color=0xf5e0d0)
                characters_[no].pop('name')
                weapons[no].pop('name')
                for i in characters_[no]:
                    if i != 'icon'and i != 'artifacts' and i != 'image' and i != 'constellations' and i != 'outfits':
                        print(f'{i} added')
                        embed_char.add_field(name=f"{i.replace('_',' ',99).title()}",value=characters_[no][i],inline=True)
                for i in weapons[no]:
                    if i != 'icon':
                        embed_weapon.add_field(name=f"{i.replace('_',' ',99).title()}",value=weapons[no][i],inline=True)
                embed_char.set_thumbnail(url=f"{characters_[no]['icon']}")
                embed_char.set_image(url=f"{characters_[no]['image']}")
                embed_weapon.set_thumbnail(url=f"{weapons[no]['icon']}")
                embeds[str(no)] = {'character': embed_char,'weapon': embed_weapon}
        if len(embeds) > 1:
            emojis = ['⬅️','➡️','⚔️']
        else:
            emojis = ['⚔️']
        return embeds,emojis
        


        






        
