from os.path import exists
from os import remove,getcwd
from json import dump, load

from nextcord import Embed,Member




class GenshinQuests:
    def __init__(self):
        self.quests = {}
        self.path = f'{getcwd()}/assets/quests/'
        self.load_quests()

    def load_quests(self):
        if exists(f'{self.path}/quests.json'):
            with open(f'{self.path}/quests.json','r') as f:
                self.quests = load(f)
    
    def save_quests(self):
        if exists(f'{self.path}/quests.json'):            
            remove(f'{self.path}/quests.json')
            with open(f'{self.path}/quests.json','w') as f:
                dump(self.quests,f)
    

    def quest_filter(self, search_string: str, type_: str):
        '''

        filter quests based on search string provided and type
        ---
        args
        ---
        search_string : act or chapter name
        type: act, chapter

        ---
        returns
        ---
        
        search_list [quests]



        '''
        search_list = []
        for quest_key in self.quests:
            if 'chapter' in self.quests[quest_key]:
                if type(self.quests[quest_key]['chapter']) == dict:
                    if bool(self.quests[quest_key]['chapter']):
                        chapter_name =  list(self.quests[quest_key]['chapter'].keys())[0]
                        act = self.quests[quest_key]['chapter'][chapter_name]  
                        
                        if type_ == 'act':
                            if search_string.lower() in act.lower():
                                search_list.append(quest_key)
                        if type_ == 'chapter':
                            if search_string.lower() in chapter_name.lower():                        
                                search_list.append(quest_key)
                    
                else:        
                    chapter_name =  self.quests[quest_key]['chapter']       
                    if type_ == 'chapter':
                        if search_string.lower() in chapter_name.lower():                        
                            search_list.append(quest_key)
        return search_list

    def get_type(self, search_string: str):
        '''

        get type based on string

        ---
        args
        ---
        search_string : any string

        ---
        returns
        ---
        
        chapter or act or quest



        '''
        for quest_key in self.quests:
            if 'chapter' in self.quests[quest_key]:
                if type(self.quests[quest_key]['chapter']) == dict:
                    if bool(self.quests[quest_key]['chapter']):
                        chapter_name =  list(self.quests[quest_key]['chapter'].keys())[0]
                        act = self.quests[quest_key]['chapter'][chapter_name]                          
                        if search_string.lower() in act.lower():
                            return 'act'
                        if search_string.lower() in chapter_name.lower():                        
                            return 'chapter'
                    
                else:        
                    chapter_name =  self.quests[quest_key]['chapter']                   
                    if search_string.lower() in chapter_name.lower():                        
                        return 'chapter'
        return 'quest'


    def get_original_name(self, string: str,type_: str):
        '''

        returns chapter name from a quest_key [returned from (search_quests func)]

        ---
        args
        ---
        quest_key
        type_ : act, chapter

        ---
        returns
        ---
        
        chapter name or act name
        '''
        for quest_key in self.quests:
            if 'chapter' in self.quests[quest_key]:
                if type(self.quests[quest_key]['chapter']) == dict:
                    if bool(self.quests[quest_key]['chapter']):
                        chapter_name =  list(self.quests[quest_key]['chapter'].keys())[0]
                        act = self.quests[quest_key]['chapter'][chapter_name]                          
                        if type_ == 'act': 
                            if string.lower() in act.lower():

                                return act
                        if type_ == 'chapter': 
                            if string.lower() in chapter_name.lower():                                           
                                return chapter_name
                    
                else:        
                    chapter_name =  self.quests[quest_key]['chapter']       
                    if type_ == 'chapter':  
                        if string.lower() in chapter_name.lower():                                       
                            return self.quests[quest_key]['chapter']
        return ''

    def search_quests(self, quest_name:str= ''):
        '''

        searches quest name in data

        ---
        args
        ---
        quest_name: any quest name

        ---
        returns
        ---
        
        search_resuts: list [quest_keys]
        
        for displaying use prettify_quests func.



        '''
        search_results = []
        if quest_name == '':
            for quest in self.quests:                
                search_results.append(quest)
        else:
            to_search = quest_name.lower()
            
            for quest in self.quests:
                if to_search in quest.replace('_',' ',99).lower():
                    print(f'found {quest}')
                    search_results.append(quest)
        return search_results,'quests'

    def search_acts(self, act_name: str):
        '''

        searches quest name in data

        ---
        args
        ---
        act_name: any quest name

        ---
        returns
        ---
        
        tuple :(search_results, type) 
            possible returns: ([acts name], acts) or ([quest_keys], quests)
        
        for displaying quest_keys use prettify_quests func.



        '''
        search_results = []
        type_ = ''
        if act_name == '':
            for quest in self.quests:  
                check = ('chapter' in self.quests[quest])

                if check:   
                    if type(self.quests[quest]['chapter']) == dict:
                        if bool(self.quests[quest]['chapter']):
                            chapter_name =  list(self.quests[quest]['chapter'].keys())[0]
                            act = self.quests[quest]['chapter'][chapter_name]                    
                            if act not in search_results:             
                                search_results.append(act)      
                            type_ = 'acts'       
        else:
            for quest in self.quests:     
                check = ('chapter' in self.quests[quest])

                if check:  
                    if type(self.quests[quest]['chapter']) == dict:
                        if bool(self.quests[quest]['chapter']):
                            chapter_name =  list(self.quests[quest]['chapter'].keys())[0]
                            act = self.quests[quest]['chapter'][chapter_name]
                            if act_name.lower() in act.lower():                                
                                search_results.append(quest)
                                type_ = 'quests'
        return search_results,type_

    def search_chapters(self, chapter_name: str):
        '''

        searches chapter name in data

        ---
        args
        ---
        chapter_name: any quest name

        ---
        returns
        ---
        
        tuple :(search_results, type) 
            possible returns: ([chapters name], chapters) or ([acts names], acts)
        
        for displaying quest_keys use prettify_quests func.



        '''
        search_results = []
        type_ = ''
        if chapter_name == '':
            for quest in self.quests:     
                check = ('chapter' in self.quests[quest])
                if check: 
                    if type(self.quests[quest]['chapter']) == dict:
                        if bool(self.quests[quest]['chapter']):
                            chapter =  list(self.quests[quest]['chapter'].keys())[0]
                            if chapter_name.lower() in chapter.lower():
                                if chapter not in search_results:
                                    search_results.append(chapter)
                                type_ = 'chapters'   
                    else:
                        chapter =  self.quests[quest]['chapter']
                        if chapter_name.lower() in chapter.lower():
                            if chapter not in search_results:
                                search_results.append(chapter)
                            type_ = 'chapters'    
        else:
            for quest in self.quests:     
                check = ('chapter' in self.quests[quest])

                if check: 
                    if type(self.quests[quest]['chapter']) == dict:
                        if bool(self.quests[quest]['chapter']):
                            chapter =  list(self.quests[quest]['chapter'].keys())[0]
                            act = self.quests[quest]['chapter'][chapter] 
                            if chapter_name.lower() in chapter.lower():
                                if act not in search_results:
                                    search_results.append(act)
                                type_ = 'acts'
                   

        return search_results,type_

    def prettify_quest(self, quest_key: str):
        '''
        Prettifies quest_key for name
        '''

        return quest_key.replace('_', ' ', 99).title()

    def simplify_step_dict(self, quest_key: str):

        '''
        simplifies steps dict

        ---
        args
        ---

        quest_key

        ---
        returns 
        ---

        step_dict : dictionary
        '''

        step_dict = {}
        check_steps = ('steps' in self.quests[quest_key])
        
        if check_steps:

            steps = self.quests[quest_key]['steps']
            for step in steps:
                if type(steps[step]) != dict:
                    step_dict[step] = steps[step]
                else:

                    sub_key = list(steps[step].keys())[0]
                    string_text = sub_key.replace('\n','',99)
                    sub_steps_text = f"{string_text}\n"
                    for sub_steps in steps[step][sub_key]:
                        sub_steps_text += f' ◽ {sub_steps}. {steps[step][sub_key][sub_steps]}\n'
                    
                    step_dict[step] = sub_steps_text
        
        return step_dict

    def simplify_rewards(self, quest_key: str):
        '''
        simplifies img key

        ---
        args
        ---

        quest_key

        ---
        returns 
        ---

        rewards_text  : str
        '''


        quest_exists = (quest_key in self.quests)
        rewards_text = ''
        if quest_exists:
            if 'rewards' in self.quests[quest_key]:
                for reward in self.quests[quest_key]['rewards']:

                    rewards_text += f" 🔸 . {reward} **{self.quests[quest_key]['rewards'][reward]}**\n"
                return rewards_text

    
    def simplify_chapter(self, quest_key: str):
        '''
        simplifies img key

        ---
        args
        ---

        quest_key

        ---
        returns 
        ---

        imgs  : list [{'title': '', 'url': ''}]
        '''

        quest_exists = (quest_key in self.quests)

        if quest_exists:

            if 'chapter' in self.quests[quest_key]:
                if type(self.quests[quest_key]['chapter']) == dict:
                    if bool(self.quests[quest_key]['chapter']):
                        chapter = list(self.quests[quest_key]['chapter'].keys())[0]
                        act = self.quests[quest_key]['chapter'][chapter]
                        return {'chapter': chapter, 'act': act}
                else:
                    return {'chapter' : self.quests[quest_key]['chapter']}
        

    def simplify_imgs(self, quest_key: str):
        '''
        simplifies img key

        ---
        args
        ---

        quest_key

        ---
        returns 
        ---

        imgs  : list [{'title': '', 'url': ''}]
        '''

        quest_exists = (quest_key in self.quests)
        imgs = []
        if quest_exists:

            # if quest exists
            # find if img exists in data and the img list is not empty

            if ('imgs' in self.quests[quest_key]) and (len(self.quests[quest_key]['imgs']) != 0):

                for img in self.quests[quest_key]['imgs']:

                    #   loops through img dicts
                    #   removes useless dicts not containing both title and img keys
                    
                    keys_exists = ('title' in img and 'img' in img)
                    if keys_exists:

                        img_dict = {'title' : img['title'], 'url': img['img'][:img['img'].find('/revision')]}
                        imgs.append(img_dict)

                return imgs

    def search(self, search_str: str='', type_: str='', type_specific: bool = False):

        '''
        ---
        args
        ---
        search_list
        type: quests, acts, chapters
        type_specific: False or True

        ---
        returns
        ---

        search_list
        type
        '''
        
        #   keys are the types returned by functions
        #   first func in list returns a search_results of below type if search is provided
        #   second func returns list of same type if no search_str is proved

        type_funcs = {
            'search_quests': ['quests','quests'],
            'search_acts': ['quests', 'acts'],
            'search_chapters' : ['acts','chapters']       
            
        }


        if type_specific:
            strict_check = (search_str != '' and type_ !='')
            low_check = (type_ !='')
            if strict_check:
                type_provided = self.get_type(search_str)
                for func in type_funcs:                   
                    
                    if type_provided in func:
                        if type_ == type_funcs[func][0]:
                            search_result,type = eval(f"self.{func}('{search_str}')")                            
                            return search_result,type
                        if type_ == 'quests':
                            return self.quest_filter(search_str,type_provided),'quests'

               
            else:
                if low_check:
                    for func in type_funcs:
                       if len(type_funcs[func]) == 2:
                           if type_ == type_funcs[func][1]:
                                return eval(f"self.{func}('{search_str}')")
        else:
            type_keys = list(type_funcs.keys())
            for func in type_keys:
                search_result,type = eval(f"self.{func}('{search_str}')")
                if len(search_result) != 0:
                    return search_result,type
                else:
                    pass
        return [],''


    def create_embed_search_pages(self, search_list : list,heading: str, type_: str, author: Member, limit: int):
        '''
        ---
        args
        ---
        search_list
        heading: str
        author: discord Member
        limit: no of items to show on pages

        ---
        returns
        ---
        embeds list
        '''

        count = divmod(len(search_list),limit)
        page_count = count[0]
        if count[1] != 0:
            page_count += 1
        quest_keys = False
        if '_' in search_list[0]:
            quest_keys = True

        main_heading = f'{heading}'

        embeds = []

        for page_index in range(1,page_count+1,1):
            
            start_index = (limit*(page_index-1))
            last_index = (page_index*limit)

            page_description = ''
            
            for item_index in range(len(search_list)):
                if start_index < item_index< last_index:
                    if quest_keys:
                        item_string = self.prettify_quest(search_list[item_index])
                    else:
                        item_string = search_list[item_index]
                    page_description += f'{item_string}\n'

            page = Embed(title=f'{main_heading } ',
                            description=f'**Search results page:** **({page_index}/{page_count})**\n\n{page_description}'
                            ,color=0xf5e0d0)
            page.set_author(name=author.display_name,icon_url=author.avatar.url)
            page.set_footer(text=f'showing {type_}')
            embeds.append(page)
            pass


        return embeds

    def create_quest_embeds(self, author: Member, quest_key: str):
        '''
        ---
        args
        ---
        author: discord Member
        quest_key

        ---
        returns
        ---
        embeds dict
        '''

        check = (quest_key in self.quests)

        if check:
            title = self.prettify_quest(quest_key)
            steps_dict = self.simplify_step_dict(quest_key)

            steps_description = ''
            for step in steps_dict:
                steps_description += f'{step}. {steps_dict[step]}\n'
            
            imgs_list = self.simplify_imgs(quest_key)

            rewards_text = self.simplify_rewards(quest_key)

            omit = ['image','steps','imgs','rewards']

            main_embed = Embed(title=f'{title}'
                                ,color=0xf5e0d0)
            
            for key in self.quests[quest_key]:
                if key not in omit:

                    if key != 'chapter':

                        if type(self.quests[quest_key][key]) == list:
                            value = '**, **'.join(self.quests[quest_key][key])
                        else:
                            value = self.quests[quest_key][key]

                        main_embed.add_field(name=key.capitalize(), value= value)
                    else:

                        chapter = self.simplify_chapter(quest_key)
                        for c_key in chapter:
                            main_embed.add_field(name=c_key.capitalize(), value= chapter[c_key])
            
            if ('image' in self.quests[quest_key]):
                main_embed.set_thumbnail(url=self.quests[quest_key]['image'][:self.quests[quest_key]['image'].find('/revision')])

            main_embed.add_field(name='Rewards', value=rewards_text)
            main_embed.set_author(name=author.display_name,
                                    icon_url=author.avatar.url)

            step_embed = Embed(title=f'{title} Walkthrough',
                                description=steps_description
                                ,color=0xf5e0d0)
            step_embed.set_author(name=author.display_name,
                                    icon_url=author.avatar.url)

            embeds_dict = {'Main Information': main_embed,'Walkthrough': step_embed}
            if imgs_list:
                for img in imgs_list:

                    img_embed = Embed(title=img['title'],
                                    color=0xf5e0d0)
                    img_embed.set_image(url=img['url'])
                    img_embed.set_author(name=author.display_name,
                                        icon_url=author.avatar.url)
                    embeds_dict[f"{img['title']} Image"] = img_embed
            
            return embeds_dict               
