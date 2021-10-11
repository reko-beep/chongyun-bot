import os
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json
import random

class GenshinQuotes:
    def __init__(self):
        self.quotes = {
            
        }
        self.__load()

    def __load(self):
        if os.path.exists('quotes.json'):
            with open('quotes.json','r') as f:
                self.quotes = json.load(f)
    
    def __save(self):
        if os.path.exists('quotes.json'):
            os.remove('quotes.json')
        with open('quotes.json','r') as f:
            json.dump(self.quotes,f)

    def add_quote(self,quote):
        if quote != "":
            self.quotes['quotes'].append(quote)
            self.__save()
    
    def get_random_quote(self):
        if 'quotes' in self.quotes:
            return random.choice(self.quotes['quotes'])
