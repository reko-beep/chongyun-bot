from genericpath import exists
from bs4 import builder

from nextcord import Member, Embed, Guild
from nextcord.ext.commands.context import Context 
from nextcord.utils import get

from core.paimon import Paimon

from json import dump, load

from os.path import exists
from os import remove, getcwd

class GuidesNotes:
    def __init__(self, pmon: Paimon):
        self.notes = {}        
        self.file = 'notes.json'
        self.pmon = pmon
        self.load()
        

       

   
    def get_character(self, name: str):
        '''

        Gets characters from case insensitive name
        
        '''
        for char in self.pmon.p_bot_config['characters']:
            if char.lower() in name.lower():
                return char
    
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
            dump(self.notes,f,indent=1)

    def get_available_characternotes(self):
        '''
        gets all available characters   for whom the notes are written
        '''
        return list(self.notes.keys())
    
    def get_available_usernotes(self, character_name: str):
        '''
        gets all available user who has written note for character_name  
        '''
        character = self.get_character(character_name)
        if character is not None:
            users = list(self.notes[character].keys())
            return users
        return []

    def get_available_notes(self, character_name: str, user_id: str):
        '''
        gets all available note for character_name written by user with user_id 
        '''
        character = self.get_character(character_name)
        if character is not None:
            if user_id in self.notes[character]:
                return self.notes[character][user_id]
        return []
    
    def remove_note(self, character_name: str, user_id: str, note_index: int):
        '''
        removes note for character_name written by user with user_id and at note_index
        '''

        character = self.get_character(character_name)
        if character is not None:
            if user_id in self.notes[character]:
                if note_index < len(self.notes[character][user_id]):
                    self.notes[character][user_id].pop(note_index)
                    self.save()
                    return True

    def add_note(self, character_name: str, user_id: str, note: str):
        '''
        add note note for character_name written by user with user_id
        '''
        character = self.get_character(character_name)
        if character is not None:
            if character in self.notes:
                if user_id in self.notes[character]:                
                    self.notes[character][user_id].append(note)
                    self.save()
                    return True
                else:
                    self.notes[character][user_id] = [note]
                    self.save()
            else:
                self.notes[character] = {user_id: [note]}
                self.save()

    
    def get_note_index(self, character_name: str, user_id: str, note: str):
        '''
        gets note_index for note of character_name written by user with user_id 
        '''

        character = self.get_character(character_name)
        try:
            if character is not None:
                if user_id in self.notes[character]:             
                    return self.notes[character][user_id].index(note)
        except ValueError:
            return None

    def get_note(self, character_name: str, user_id: str, note_index: int):
        '''
        gets note for character_name written by user with user_id and at note_index
        '''
        character = self.get_character(character_name)
        if character is not None:
            if user_id in self.notes[character]:   
                if note_index < len(self.notes[character][user_id]):
                    return self.notes[character][user_id][note_index]

    def create_note_embed(self, character_name: str, user: str, note_index: int):
        '''
        creates an embed for note

        '''
        note = self.get_note(character_name,user,note_index)
        if note is not None:
            user = get(self.pmon.guilds[0].members,id=int(user))
            embed = Embed(title=f'{user.display_name} written note for {character_name}',description=note,color=0xf5e0d0)  
            embed.set_author(name=user.display_name,
                            icon_url=user.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/NnFetya.gif')
            return embed

    def delete_note_embed(self, character_name: str, user: str, note_index: int):
        '''
        creates an embed for note

        '''
        note = self.get_note(character_name,user,note_index)
        if note is not None:
            user = get(self.pmon.guilds[0].members,id=int(user))
            embed = Embed(title=f'{user.display_name} written note for {character_name} is deleted!',description=note,color=0xf5e0d0)  
            embed.set_author(name=user.display_name,
                            icon_url=user.avatar.url)
            embed.set_thumbnail(url='https://i.imgur.com/JvBHvXD.gif')
            return embed