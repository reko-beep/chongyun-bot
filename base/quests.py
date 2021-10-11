import os
from pprint import pprint
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json


class GenshinQuests:
    def __init__(self):
        self.quests = {}
        self.keys = {}
        self._load()
        self.prettify_keys()        
        pass

    def _load(self):
        if os.path.exists('all_quests.json'):
            with open('all_quests.json','r') as f:
                self.quests = json.load(f)
    
    def prettify(self,str_):
        if '_s_' in str_:
            str_ = str_.replace('_s_','_',1)
        str_ = str_.replace('_',' ',99)
        return str_.title()
    
    def prettify_keys(self):
        for i in self.quests:
            pr = ''
            if '_s_' in i:
                pr = i.replace('_s_','_',1)
            if pr != '':
                pr = pr.replace('_',' ',99)
            else:
                pr = i.replace('_',' ',99)
            self.keys[pr.title()] = i

    def remove_seperators(self,str_):
        keys = [';',':',"'",'-','\\','.',',','/','!']
        for i in keys:
            str_ = str_.replace(i,'',99)
        return str_

    def get_prettified_from_keys(self,key):        
        for x in self.keys:            
            if self.keys[x] == key:
                return {x:self.keys[x]}
       


    def chapter_keys(self,chapter_name):
        splited = chapter_name.lower().split(' ')              
        search_dict = {}
        chapter = ''
        for i in self.quests:            
            if 'chapter' in self.quests[i]:
                add = False
                key = ''
                if type(self.quests[i]['chapter']) == dict:     
                    if len(self.quests[i]['chapter'].keys()) >= 1:              
                        key = self.remove_seperators(list(self.quests[i]['chapter'].keys())[0].lower())                   
                else:
                    key = self.remove_seperators(self.quests[i]['chapter'])
                if key != '':
                    key_split = key.split(' ')
                    if len(key_split) > len(splited):
                        for check in range(0,len(splited),1):
                            if splited[check] == key_split[check]:
                                add = True   
                                chapter = key
                            else:
                                add = False
                                break                     
                    else:
                        for check in range(0,len(key_split),1):
                            if splited[check] == key_split[check]:
                                add = True
                                chapter = key  
                            else:
                                add = False
                                break
                    if add == True:
                        if chapter in search_dict:
                            #print(f'To find key {i}')
                            dict_ = self.get_prettified_from_keys(i)
                            #print(dict_)
                            search_dict[chapter].append(dict_)
                        else:
                            search_dict[chapter] = [self.get_prettified_from_keys(i)]
        if chapter_name == '':
            for i in self.quests:            
                if 'chapter' in self.quests[i]:
                        chapter = ''
                        if type(self.quests[i]['chapter']) == dict:     
                            if len(self.quests[i]['chapter'].keys()) >= 1:              
                                chapter = self.remove_seperators(list(self.quests[i]['chapter'].keys())[0].lower())                   
                        else:
                            chapter = self.remove_seperators(self.quests[i]['chapter'])
                        if chapter in search_dict:
                            #print(f'To find key {i}')
                            dict_ = self.get_prettified_from_keys(i)
                            #print(dict_)
                            search_dict[chapter].append(dict_)
                        else:
                            search_dict[chapter] = [self.get_prettified_from_keys(i)]
                    

        return search_dict
                
    def quests_keys(self,quest_name):
        splited = quest_name.lower().split(' ')    
        print(splited)
        search_dict = {}
        if quest_name != '':
            for i in self.keys:
                add = False
                title = i
                splitted_title = title.lower().split(' ')
                if len(splitted_title) > len(splited):
                    for check in range(0,len(splited),1):
                        print(splited[check],splitted_title[check])
                        if splited[check] == splitted_title[check]:
                            add = True
                            print('Found', splited[check], splitted_title[check])
                            break
                        else:
                            add = False
                            break
                else:
                    for check in range(0,len(splitted_title),1):
                        if splited[check] == splitted_title[check]:
                            add = True
                            print('Found', splited[check], splitted_title[check])                        
                        else:
                            add = False
                            break    
                if add == True:
                    search_dict[i] = self.keys[i]
            return search_dict
        else:
            for i in self.keys:
                search_dict[i] = self.keys
            return search_dict


                




    def acts_keys(self,chapter_name):
        splited = chapter_name.lower().split(' ')              
        search_dict = {}
        chapter = ''
        for i in self.quests:            
            if 'chapter' in self.quests[i]:
                add = False
                key = ''
                if type(self.quests[i]['chapter']) == dict:                  
                    if len(self.quests[i]['chapter'].keys()) >= 1:                              
                        key_ = list(self.quests[i]['chapter'].keys())[0]   
                        key = self.remove_seperators(self.quests[i]['chapter'][key_].lower())                
                if key != '':
                    key_split = key.split(' ')
                    if len(key_split) > len(splited):
                        #print('provided len smaller than original')
                        for check in range(0,len(splited),1):                            
                            if splited[check] == key_split[check]:
                                add = True   
                                chapter = key  
                                print(splited[check],key_split[check],add)    
                            else:
                                add = False 
                                break                           
                                          
                    else:
                        #print('provided len greater than original')
                        for check in range(0,len(key_split),1):                            
                            if splited[check] == key_split[check]:
                                add = True
                                chapter = key  
                                #print(splited[check],key_split[check],add)   
                            else:
                                add = False
                                break                         
                #print(f'End results to add {add}')
                if add == True:
                    if chapter in search_dict:                        
                        dict_ = self.get_prettified_from_keys(i)
                        #print(dict_)
                        search_dict[chapter].append(dict_)
                    else:
                        search_dict[chapter] = [self.get_prettified_from_keys(i)]
        if chapter_name == '':
            for i in self.quests:            
                if 'chapter' in self.quests[i]:
                        chapter = ''
                        if type(self.quests[i]['chapter']) == dict:     
                            if len(self.quests[i]['chapter'].keys()) >= 1:              
                                key_ = list(self.quests[i]['chapter'].keys())[0]   
                                chapter = self.remove_seperators(self.quests[i]['chapter'][key_].lower())                        
                        if chapter in search_dict and chapter != '':
                            #print(f'To find key {i}')
                            dict_ = self.get_prettified_from_keys(i)
                            #print(dict_)
                            search_dict[chapter].append(dict_)
                        else:
                            search_dict[chapter] = [self.get_prettified_from_keys(i)]
                    

        return search_dict

    def get_quest_content(self,quest_dict:dict):
        if type(quest_dict) == dict:
            name = list(quest_dict.keys())[0]
            key = ''
            if name in self.keys:
                key = self.keys[name]
            if key != '':
                if key in self.quests:                    
                    dict_ = self.quests[key]
                    dict_['name'] = name
                    return dict_
            


    def type_keys(self,type_):
        allowed = ['story','world','archon']
        search_dict = {}
        if type_ != '':
            if type_ in allowed:
                for i in self.quests:                    
                    if 'type' in self.quests[i]:
                        print(type_,self.quests[i]['type'])
                        if type_ in self.quests[i]['type'].lower():
                            dict_ = self.get_prettified_from_keys(i)
                            if type_ in search_dict:
                                search_dict[type_].append(dict_)
                            else:
                                search_dict[type_] = [self.get_prettified_from_keys(i)]
        else:
            for c in allowed:
                for i in self.quests:                
                    if 'type' in self.quests[i]:
                        print(type_,self.quests[i]['type'])
                        if c in self.quests[i]['type'].lower():
                            dict_ = self.get_prettified_from_keys(i)
                            if c in search_dict:
                                search_dict[c].append(dict_)
                            else:
                                search_dict[c] = [self.get_prettified_from_keys(i)]
        return search_dict
    

    def get_rewards(self,quest_name):
        if quest_name in self.quests:
            if 'rewards' in self.quests[quest_name]:
                return self.quests[quest_name]['rewards']

    def chapter_rewards(self,chapter_name):
        chapters = self.chapter_keys(chapter_name)
        print(chapters)
        chapter_rewards = {}        
        for chapter in chapters:
            temp = {}
            for quests in chapters[chapter]:
                dict_ = quests
                key = dict_[list(dict_.keys())[0]]
                rewards = self.get_rewards(key)
                if rewards != None:
                    for reward in rewards:                        
                        correct = rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99)
                        if correct.isdigit():
                            #print(reward,'exists in temp',reward in temp)
                            if reward in temp:
                                print(reward,temp[reward],rewards[reward])
                                temp[reward] += int(rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99))
                            else:
                                temp[reward] = int(rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99))                           
                        else:
                            temp[reward] = rewards[reward]
            chapter_rewards[chapter] = temp                                   
        return chapter_rewards

    def acts_rewards(self,chapter_name):
        chapters = self.acts_keys(chapter_name)   
        print(chapters)    
        chapter_rewards = {}        
        for chapter in chapters:
            temp = {}
            for quests in chapters[chapter]:
                dict_ = quests
                key = dict_[list(dict_.keys())[0]]
                rewards = self.get_rewards(key)
                print(rewards)
                if rewards != None:
                    for reward in rewards:                        
                        correct = rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99)
                        if correct.isdigit():
                            #print(reward,'exists in temp',reward in temp)
                            if reward in temp:
                                #print(reward,temp[reward],rewards[reward])
                                temp[reward] += int(rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99))
                            else:
                                temp[reward] = int(rewards[reward].replace(' ','',99).replace(',','',99).replace('×','',99))                           
                        else:
                            temp[reward] = rewards[reward]
            chapter_rewards[chapter] = temp                                   
        return chapter_rewards

    def chapter_acts(self,chapter_name):
        splited = chapter_name.lower().split(' ')              
        search_dict = {}
        chapter = ''
        for i in self.quests:            
            if 'chapter' in self.quests[i]:
                add = False
                key = ''
                print(type(self.quests[i]['chapter']),self.quests[i]['chapter'])
                if type(self.quests[i]['chapter']) == dict:     
                    if len(self.quests[i]['chapter'].keys()) >= 1:              
                        key = self.remove_seperators(list(self.quests[i]['chapter'].keys())[0].lower())                   
                else:
                    key = self.remove_seperators(self.quests[i]['chapter'])
                if key != '':
                    key_split = key.split(' ')
                    if len(key_split) > len(splited):
                        for check in range(0,len(splited),1):
                            if splited[check] == key_split[check]:
                                add = True   
                                chapter = key
                            else:
                                add = False
                                break                     
                    else:
                        for check in range(0,len(key_split),1):
                            if splited[check] == key_split[check]:
                                add = True
                                chapter = key  
                            else:
                                add = False
                                break
                    if add == True:
                        added_ = ''
                        if chapter in search_dict:   
                            if type(self.quests[i]['chapter'])  == dict:
                                if len(self.quests[i]['chapter'].keys()) >= 1:                                           
                                    added_ = self.remove_seperators(self.quests[i]['chapter'][list(self.quests[i]['chapter'].keys())[0]])
                                    print(chapter,added_)                                
                                    if added_ in search_dict[chapter]:
                                        pass
                                    else:
                                        search_dict[chapter].append(added_)
                            else:
                                search_dict[chapter] = []
                        else:  
                            if type(self.quests[i]['chapter'])  == dict:                          
                                if len(self.quests[i]['chapter'].keys()) >= 1:                                                                  
                                    added_ = self.remove_seperators(self.quests[i]['chapter'][list(self.quests[i]['chapter'].keys())[0]])  
                                    print(chapter,added_)                               
                                    search_dict[chapter]= [added_]
                            else:
                                search_dict[chapter] = []
        if chapter_name == '':
            for i in self.quests:            
                if 'chapter' in self.quests[i]:
                        chapter = ''
                        if type(self.quests[i]['chapter']) == dict:     
                            if len(self.quests[i]['chapter'].keys()) >= 1:                                           
                                chapter = self.remove_seperators(list(self.quests[i]['chapter'].keys())[0])                   
                        else:
                            chapter = self.remove_seperators(self.quests[i]['chapter'])
                        if chapter in search_dict:   
                            if type(self.quests[i]['chapter'])  == dict:
                                if len(self.quests[i]['chapter'].keys()) >= 1:                                                  
                                    added_ = self.remove_seperators(self.quests[i]['chapter'][list(self.quests[i]['chapter'].keys())[0]]) 
                                    print(chapter,added_)                                
                                    if added_ in search_dict[chapter]:
                                        pass
                                    else:
                                        search_dict[chapter].append(added_)
                            else:
                                search_dict[chapter] = []
                        else:  
                            if type(self.quests[i]['chapter'])  == dict:                          
                                if len(self.quests[i]['chapter'].keys()) >= 1:                                                                       
                                    added_ = self.remove_seperators(self.quests[i]['chapter'][list(self.quests[i]['chapter'].keys())[0]])  
                                    print(chapter,added_)                               
                                    search_dict[chapter]= [added_]
                            else:
                                search_dict[chapter] = []
                    

        return search_dict



    def search(self,type_='',chapters_='',acts_='',quests_=''):       
        search = ''
        if len(self.quests) !=0:
            if type_ != '':
                search = self.type_keys(type_)
            else:
                if chapters_ != '' :
                    search = self.chapter_keys(chapters_) 
                else:
                    if acts_!='':
                        search = self.acts_keys(acts_)


        return search

    def create_chapter_embeds(self,chapter_name):
        chapter_keys_ = self.chapter_acts(chapter_name)
        print(chapter_keys_)
        emojis = []
        if len(chapter_keys_) > 1:
            emojis = ['⬅️','➡️']
        else:
            emojis = []
        if chapter_keys_ != None:
            embeds = []        
            for i in chapter_keys_:
                name_chapter = i.replace('_',' ',99).title()
                acts_text = ''
                rewards = self.chapter_rewards(i)
                print(rewards)
                c = 0
                rewards_text = ''
                for quests in chapter_keys_[i]:
                    c+= 1
                    name = quests
                    acts_text += f'{c}. {name}\n'
                i = i.lower()
                if i in rewards:
                    for reward in rewards[i]:                    
                        if str(rewards[i][reward]).isdigit():
                            rewards_text += f'🔸 {reward} : {rewards[i][reward]} '
                        else:                                             
                            if str(reward) == str(rewards[i][reward]):
                                rewards_text += f'🔸 Character: {reward} '
                            else:
                                rewards_text += f'🔸 {reward} {rewards[i][reward]} '
                print(acts_text)                 
                print(rewards_text)
                embed = discord.Embed(title=f'{name_chapter}',description=f'**Acts:**\n\n{acts_text}\n**Rewards:**\n{rewards_text}',color=0xf5e0d0)
                embed.set_image(url='https://i.pinimg.com/originals/73/f6/ef/73f6ef60b8aca0bc7840ca3f4271802b.jpg')
                embeds.append(embed)                
            return embeds,emojis
    
    def create_acts_embeds(self,chapter_name):
        chapter_keys_ = self.acts_keys(chapter_name)
        print(chapter_keys_)
        emojis = []
        if len(chapter_keys_) > 1:
            emojis = ['⬅️','➡️']
        else:
            emojis = []
        if chapter_keys_ != None:
            embeds = []        
            for i in chapter_keys_:
                name_chapter = i.replace('_',' ',99).title()
                acts_text = ''
                rewards = self.acts_rewards(i)
                print(rewards)
                c = 0
                rewards_text = ''
                for quests in chapter_keys_[i]:
                    c+= 1
                    name = list(quests.keys())[0]
                    acts_text += f'{c}. {name}\n'
                print(rewards)
                for reward in rewards[i]:                    
                    if str(rewards[i][reward]).isdigit():
                        rewards_text += f'🔸 {reward} : {rewards[i][reward]}  '
                    else:                                             
                        if str(reward) == str(rewards[i][reward]):
                            rewards_text += f'🔸 Character: {reward}  '
                        else:
                            rewards_text += f'🔸 {reward} {rewards[i][reward]}  '
                print(acts_text)                 
                print(rewards_text)
                embed = discord.Embed(title=f'{name_chapter}',description=f'**Quests:**\n\n{acts_text}\n**Rewards:**\n{rewards_text}',color=0xf5e0d0)
                embed.set_image(url='https://i.pinimg.com/originals/73/f6/ef/73f6ef60b8aca0bc7840ca3f4271802b.jpg')
                embeds.append(embed)                
            return embeds,emojis

    def create_quest_embed(self,quest_name):
        quest_keys_ = self.quests_keys(quest_name)
        keys_ = list(quest_keys_.keys())
        embeds = []
        emojis = ['⬅️','➡️']
        if quest_name == '':
            count_ = divmod(len(quest_keys_),10)
            count = int(count_[0])
            if count_[1] == 0:
                pass
            else:
                count += 1
            limit = 10
            for i in range(1,count,1):
                text_ = ''                
                for c in range(0,len(quest_keys_),1):
                    if (i*limit-limit) < c < i*limit:
                        text_ += f'**{c}**. {keys_[c]}\n'
                embed = discord.Embed(title=f'Quests ({i}\{count})',description=text_,color=0xf5e0d0)
                embed.set_image(url='https://i.pinimg.com/originals/73/f6/ef/73f6ef60b8aca0bc7840ca3f4271802b.jpg')
                embeds.append(embed)
            return embeds,emojis
        if len(quest_keys_) > 1 and quest_name != '':
            desp_ = ''
            for i in quest_keys_:
                desp_ += f'{i}\n'
            embed = discord.Embed(title=f'{quest_name.title()} Quest suggestions',description=f'{desp_}',color=0xf5e0d0)
            embeds.append(embed)
        else:
            name = list(quest_keys_.keys())[0]
            desp_ = ''
            content = self.get_quest_content(quest_keys_)
            for i in content:                    	    
                if i != 'image' and i != 'steps' and i !='imgs':                    
                    if type(content[i]) == list:                        
                        desp_ += f"**{i.title()}:**\n{','.join(content[i])}\n"
                    else:
                        if type(content[i]) == dict:                            
                            if len(content[i]) >= 1:      
                                if i == 'rewards':
                                    rewards_text = ''
                                    for c in content['rewards']:
                                        if str(content['rewards'][c]).isdigit():
                                            rewards_text += f"🔸 {c} : {content['rewards'][c]}  "
                                        else:                                             
                                            if str(c) == str(content['rewards'][c]):
                                                rewards_text += f'🔸 Character: {c}  '
                                            else:
                                                rewards_text += f"🔸 {c} {content['rewards'][c]}  "                                    
                                    desp_ += f'**{i.title()}**\n{rewards_text}\n'    
                                else:

                                    desp_ += f'**{i.title()}**\n{list(content[i].keys())[0]}\n**Act:**\n{content[i][list(content[i].keys())[0]]}\n'
                        else:                           
                            desp_ += f'**{i.title()}**\n{content[i]}\n'
            embed_main = discord.Embed(title=f'{name} details!',description=desp_,color=0xf5e0d0)
            if 'image' in content:
                embed_main.set_thumbnail(url=f"{content['image']}")          
            steps_text = ''
            if 'steps' in content:
                embed_main.set_footer(text=f'react ➡️ to see walkthrough!')
                for i in content['steps']:
                    further_steps = ''
                    step_ = ''
                    if type(content['steps'][i]) == dict:
                        temp_ = content['steps'][i][list(content['steps'][i].keys())[0]]
                        for fur in temp_:                            
                            further_steps += f"   🔸. __{temp_[fur]}__\n"
                        step_ = list(content['steps'][i].keys())[0]
                    else:
                        step_ = content['steps'][i]
                    if further_steps == '':
                        steps_text += f'**{i}**. {step_}\n'
                    else:
                        steps_text += f'**{i}**. {step_}\n{further_steps}\n'
                    
                pprint(steps_text)  
            embed_step = discord.Embed(title=f'{name} Walkthrough',description=steps_text,color=0xf5e0d0)
            if 'image' in content:
                embed_step.set_thumbnail(url=f"{content['image']}")  
            embeds = [embed_main,embed_step]
            if len(content['imgs']) > 1:
                embed_step.set_footer(text=f'react ➡️ to see locations images!')
                for i in content['imgs']:
                    if 'img' in i:
                        if 'title' in i:
                            embed = discord.Embed(title=f'{name}',description=f"**{i['title']}**",color=0xf5e0d0)
                            if i['img'].startswith('http'):
                                embed.set_image(url=f"{i['img'][:i['img'].find('/revision')]}")
                            if 'image' in content:
                                embed.set_thumbnail(url=f"{content['image']}")  
                            embeds.append(embed)
                        else:
                            embed = discord.Embed(title=f'{name}')
                            if i['img'].startswith('http'):
                                embed.set_image(url=f"{i['img'][:i['img'].find('/revision')]}")
                            if 'image' in content:
                                embed.set_thumbnail(url=f"{content['image']}")  
                            embeds.append(embed)  
                              
        if len(embeds) >= 1:
            return embeds,emojis
        else:
            return None,None


