from typing import ItemsView
import requests
from main import Fetcher
from bs4 import BeautifulSoup
import json
from logger import logc
from time import sleep
from json import dump,load

class VoiceOvers(Fetcher):
    def __init__(self):
        super().__init__()

    def fetch_characters(self, type: str = 'Characters/List'):
        list = []
        data = self.get(f'{type}').content
        bs = BeautifulSoup(data,'lxml')
        table_element = [table.find_next_sibling() for table in bs.find_all('p') if 'characters match' in table.text.lower()]
        for t_e in table_element:
            rows = t_e.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                check = (len(columns) >= 2)
                if check:
                    link = columns[1].find('a')

                    if link:
                        link = link.attrs['href'].split('/')[-1]
                        if link not in list:
                            list.append(link)
        logc(f'fetched lists for characters {type}')
        return list

    def fetch_languages(self):
        return ['English','Chinese','Korean','Japanese']

    def fetch_voiceovers(self, character: str, language: str):
        if language == 'English':
            language = ''
        else:
            language = f'/{language}'
        logc(f'fetching voiceovers of character {character} o f language {language}')
        src = self.get(f'{character}/Voice-Overs{language}').content
        bs = BeautifulSoup(src, 'lxml')
        data = {}
        story_voices_span = bs.find('span',{'id':'Story'})
        story_voices_table = None
        if story_voices_span is not None:
            if story_voices_span.parent is not None:
                story_voices_table = story_voices_span.parent.find_next_sibling()
        voices_ = {}
        if story_voices_table is not None:
            story_voices = story_voices_table.find_all('tr')[1:]
            last_key = ''
            for story_voice in story_voices:
                if story_voice.find('th') is not None: 
                    key = story_voice.find('th').text.splitlines()[0].split('(')[0]    
                    if language != '':
                        if len(story_voice.find('th').text.splitlines()[0].split('(')) >= 2:
                            key = story_voice.find('th').text.splitlines()[0].split('(')[1].split(')')[0]  
                        else:
                            key = story_voice.find('th').text.splitlines()[0].split('(')[0]        
                    
                    if key != last_key:
                        last_key = key                        
                        key = story_voice.find('th').text.splitlines()[0].split('(')[0]
                        if language != '':
                            if len(story_voice.find('th').text.splitlines()[0].split('(')) >= 2:
                                key = story_voice.find('th').text.splitlines()[0].split('(')[1].split(')')[0]  
                            else:
                                key = story_voice.find('th').text.splitlines()[0].split('(')[0]        
                audios = story_voice.find_all('a') 
                for audio in audios:
                    if 'href' in audio.attrs:
                        if  audio.attrs['href'].startswith('http'):
                            if key in voices_:
                                voices_[key].append(audio.attrs['href'][:audio.attrs['href'].find('/revision')])
                            else:
                                voices_[key] = [audio.attrs['href'][:audio.attrs['href'].find('/revision')]]
        combat_voices_table = None
        combat_voices_span = bs.find('span',{'id':'Combat'})
        if combat_voices_span is not None:
            if combat_voices_span.parent is not None:
                combat_voices_table = combat_voices_span.parent.find_next_sibling()
        if combat_voices_table is not None:
            combat_voices = combat_voices_table.find_all('tr')[1:]

            last_key = ''
            for combat_voice in combat_voices:
                if combat_voice.find('th') is not None:                 
                    key = combat_voice.find('th').text.splitlines()[0].split('(')[0]    
                    if language != '':
                        if len(combat_voice.find('th').text.splitlines()[0].split('(')) >= 2:
                            key = combat_voice.find('th').text.splitlines()[0].split('(')[1].split(')')[0]  
                        else:
                            key = combat_voice.find('th').text.splitlines()[0].split('(')[0]       
                    if key != last_key:
                        last_key = key
                        key = combat_voice.find('th').text.splitlines()[0].split('(')[0]    
                        if language != '':
                            if len(combat_voice.find('th').text.splitlines()[0].split('(')) >= 2:
                                key = combat_voice.find('th').text.splitlines()[0].split('(')[1].split(')')[0]  
                            else:
                                key = combat_voice.find('th').text.splitlines()[0].split('(')[0]

                audios = combat_voice.find_all('a') 
                for audio in audios:
                    if 'href' in audio.attrs:
                        if  audio.attrs['href'].startswith('http'):
                            if key in voices_:
                                voices_[key].append(audio.attrs['href'][:audio.attrs['href'].find('/revision')])
                            else:
                                voices_[key] = [audio.attrs['href'][:audio.attrs['href'].find('/revision')]]
        logc(f'fetched voiceovers of character {character} of language {language}')        
        return voices_
          


