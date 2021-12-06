from os import name
import nextcord as discord
from nextcord.ext import commands,tasks
import json
import os
def find_uids(message,data): 
    temp_ = {}
    text = message.content
    author_ = message.author
    list_ = text.split('\n')
    servers_ = ['asia','eu:europe','hk:honkkong','na:northamerica']
    save = False 
    for i in list_:                       
        print(f'Author {author_}\n Line {i}')
        if ':' in i:
            users = i.split(":")
            print(f' Found --> (:)  list {users}')            
            for serv_ in servers_:
                check_list = serv_.split(':')
                if users[0].lower() in check_list:
                    if users[1].lstrip().rstrip().isdigit():
                        print(f'Found server {users[0]} : UID {users[1]}')
                        temp_[users[0].lower()] = int(users[1].lstrip().rstrip())
                        save = True
        else:
            if i.isdigit():
                print(f'Found No Server but UID {i}')
                temp_['none'] = int(i)
                save = True
    print(temp_)
    if save == True:
        if str(author_.id) in data:
            temp__ = {}
            temp__['name'] = author_.display_name
            temp__['servers'] = temp_             
            if 'servers' in data[str(author_.id)]:                    
                data[str(author_.id)]['servers'] = temp_ 
            else:
                data[str(author_.id)] = temp__
        else:
            data[str(author_.id)] = {'servers':temp_}

def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json','r') as f:
            return json.load(f)
