from bs4 import builder

from nextcord import Member, Embed
from nextcord.ext.commands.context import Context 

from json import dump, load

from os.path import exists
from os import remove, getcwd

class GuidesNotes:
    def __init__(self):
        self.notes = {}        
        self.file = 'notes.json'

        self.characters = [
                "Albedo",
                "Aloy",
                "Amber",
                "Barbara",
                "Beidou",
                "Bennett",
                "Chongyun",
                "Diluc",
                "Diona",
                "Eula",
                "Fischl",
                "Ganyu",
                "HuTao",
                "Itto",
                "Jean",
                "Kazuha",
                "Kaeya",
                "Ayaka",
                "Keqing",
                "Klee",
                "Sara",
                "Lisa",
                "Mona",
                "Ningguang",
                "Noelle",
                "Qiqi",
                "Raiden",
                "Razor",
                "Rosaria",
                "Sayu",
                "Sucrose",
                "Childe",
                "Traveler",
                "Venti",
                "Xiangling",
                "Xiao",
                "Xingqiu",
                "Xinyan",
                "Yanfei",
                "Yoimiya",
                "Zhongli",
                "Dainsleif",
                "Gorou",
                "Kokomi",
                "Thoma",
                "Yae",
                "Gorou"
                ]
        self.load()

   
    def get_character(self, name: str):
        '''

        Gets characters from case insensitive name
        
        '''
        if name.title() in self.characters:
            return self.characters[self.characters.index(name.title())]
    
    def load(self):
        '''

        Loads notes 
        
        '''
        if exists(self.file):               
            with open(self.file, 'r') as f:
                self.notes = load(f)

    def save(self):
        '''

        Saves notes 

        '''
        if exists(self.file):
            remove(self.file)

        with open(self.file, 'w') as f:
            dump(self.notes,f)


    def add_note(self, user: Member, character_name:str, note: str):
        '''

        Saves note for character
        
        '''
        user_id = str(user.id)
        character = self.get_character(character_name)
        if character != None:

            # If character is found from characters list
            

            if character in self.notes:
                if user_id in self.notes[character]:

                    # add note in existing  character database

                    self.notes[character][user_id].append(note)
                else:

                    # creates a new character key in database

                    self.notes[character] = {user_id : [note]}     
            else:
                 self.notes[character] = {user_id : [note]}   
            self.save()      
        return None
    
    def remove_note(self,user: Member,character_name: str, note:str):
        '''
        Removes note of a user User: discord.User, for character name and note provided

        returns:
            true if note removed else false
        '''
        user_id = str(user.id)
        character = self.get_character(character_name)
        if character != None:

             if character in self.notes:
                if user_id in self.notes[character]:
                    if note in self.notes[character][user_id]:

                        print(note in self.notes[character][user_id])
                        print(self.notes[character][user_id].index(note))
                        self.notes[character][user_id].pop(self.notes[character][user_id].index(note))  
                        self.save()
                        return True              
        return False
    
    def get_notes(self,user: Member, character_name:str):
        '''
        Dynamic fetch

            1. returns notes if user and character name both exists in database
            2. returns users who have added notes if only character name is provided
            3. returns characters for whom user have written notes if only character name is provided
            3. returns characters for whom notes are written if nothing is provided

        returns:
            text_list: for use in embed
            type: users, characters, notes
        '''

        if user != None:
            user_id = str(user.id)
        else:
            user_id = ''

        if character_name != '':
            character = self.get_character(character_name)
            if character != None:

                # If character is found from characters list

                if character in self.notes:

                    data = self.notes[character]
                    if data != None:
                        if user_id != '':  
                            if user_id in data:                    
                                text_list = [f'**{c}**. {note}' for c,note in enumerate(data[user_id])]
                                return text_list,'notes'
                        else:
                            text_list = [f'**{c}**. <@!{user}>' for c,user in enumerate(data)]
                            return text_list, 'users'                        
        else:
            if user_id != '':
                text_list = []
                c = 0
                for character in self.notes:
                    if user_id in self.notes[character]:
                        text_list.append(f'**{c}**. {character}')
                        c += 1
                return text_list,'characters'
            else:
                text_list = []
                text_list = [f'**{c}**. {character}' for c,character in enumerate(self.notes)]
                return text_list, 'characters'
        return None,None

    def get_selected_note(self, notes: list, selected_number: int):
        '''
        Gets note string from notes list at number selected_number

        returns:
            note: string
            None if not found!
        '''
        if len(notes) >= selected_number:
            return notes[selected_number][notes[selected_number].find('**.')+len('**.'):].strip()            
        return None

    def create_embed_pages(self,notes:list, limit: int,member_name:str,character:str, type_:str):
        '''

        creates embeds pages from notes list

        limit: each page contains how much items
        member_name: user who invoked the command
        character: character name if provided
        type: if provided [users, characters,notes]

        returns: 
            embeds: list[Embed,Embed]
            emojis: list[str,str]
        '''

        pages_count = 0
        pages = divmod(len(notes),limit)
        pages_count = pages[0]
        embeds = []
        emojis = ['⬅️','➡️'] 

        if pages[1] == 0:            
            pass
        else:
            pages_count += 1

        for page in range(1,pages_count+1,1):
            if type_ == 'notes' and character != "":
                if member_name != '':
                    description_ = f'**{member_name}** written notes for {character} to complement the added builds to bot!\n\n'
                else:
                    description_ = f'User written notes for {character} to complement the added builds to bot!\n\n'
            else:
                description_ = f'User written notes for {character} to complement the added builds to bot!\n\n'    
            print(len(notes))        
            for note in range(0,len(notes)+1,1):
                if page*limit-limit-1 < note < page*limit+1:
                    print(note)
                    if len(notes)-1 >= note:
                        print(note)
                        print(notes[note])
                        description_ += f'{notes[note]}\n'

            embed = Embed(title=f'Notes ({page}/{pages_count})'
                , description=description_
                , color=0xf5e0d0)

            embeds.append(embed)

        return embeds,emojis

    def create_status(self,ctx: Context,member: Member, type_: str):
        '''
        Provides a statement based on what is being shown in embed

        returns:
            statement: string
        '''
        if member == ctx.author:
            if type_ == 'notes':
                return 'You can remove only your notes by using !rn (charactername) (number from here)'
            if type_ == 'characters':
                return 'You only have notes added for these characters!'
            if type_ == 'users':
                return 'You only have notes added for these characters!'
        else:
            if member != None:
                if type_ == 'notes':
                    return f' Notes added by {member.display_name}'
                if type_ == 'characters':
                    return 'Only these characters have notes added!'
                if type_ == 'users':
                    return 'These users have added quote for this character!!'
            
