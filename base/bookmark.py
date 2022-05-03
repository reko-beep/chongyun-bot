from calendar import c
from json import dump, load
from queue import Empty
from this import d
from base.resource_manager import ResourceManager

from nextcord import Member, Embed, Message
from os.path import exists
from os import getcwd

class Bookmarer:
    def __init__(self, bot):
        self.bot = bot
        self.resm : ResourceManager = bot.resource_manager
        self.bm_data = {

        }
        self.load()
    

    def load(self):
        file = self.resm.db.format(path='bm.json')
        if exists(file):
            with open(file, 'r') as f:
                self.bm_data = load(f)

    def save(self):
        file = self.resm.db.format(path='bm.json')        
        with open(file, 'w') as f:
            dump(self.bm_data, f, indent=1)

    def add_bookmark(self, member: Member, message: Message, category: str):

        discord_id = str(member.id)
        if discord_id not in self.bm_data:
            self.bm_data[discord_id] = []   

        category = category if category != '' else 'No Category'

        embeds = self.bookmark_pattern(member, message, category)
        self.bm_data[discord_id] += embeds
        self.save()
        return True


    def bookmark_pattern(self, member: Member,  message: Message, category: str):

        embeds = []

        embeded = (len(message.embeds) != 0)
        attachments = (len(message.attachments) != 0)
        if embeded:
            for embed in message.embeds:
                pattern = {
                'owner': member.id,
                'author': str(message.author),
                'category': category,
                'fields': [],
                'content': message.content,
                'image': '',
                'message_link': message.jump_url,
                'message_time' : message.created_at.strftime('%c')
                }   
                pattern['fields'] = [{'name': e['name'],'value': e['value']} for e in embed.fields]
                print(embed.image.url)
                if embed.image.url is not Embed.Empty:
                    pattern['image'] = embed.image.url
                embeds.append(pattern)
        else:
            if attachments:
                for attach in message.attachments:
                    pattern = {
                    'owner': member.id,
                    'author': str(message.author),
                    'category': category,
                    'fields': [],
                    'content': message.content,
                    'image': '',
                    'message_link': message.jump_url,
                    'message_time' : message.created_at.strftime('%c')
                }
                    if attach.url.endswith("jpg") or attach.url.endswith("png") or attach.url.endswith("jpeg"):
                        pattern['image'] = attach.url
                    
                    embeds.append(pattern)
            else:
                pattern = {
                    'owner': member.id,
                    'author': str(message.author),
                    'category': category,
                    'fields': [],
                    'content': message.content,
                    'image': '',
                    'message_link': message.jump_url,
                    'message_time' : message.created_at.strftime('%c')
                }
                embeds.append(pattern)

        return embeds       

    def get_bookmarks(self, member: Member, category: str):

        discord_id = str(member.id)
        
        bookmarks_specific = []

        if discord_id in self.bm_data:

            bookmarks = self.bm_data[discord_id]

            for index, bm in enumerate(bookmarks):
                cat = category.lower().split(" ")
                for c in cat:
                    if c in bm['category'].lower():
                        bookmarks_specific.append({
                            **bm,
                            **{'index': index}
                        })

        return bookmarks_specific
    
    def if_bookmark_exists(self,member: Member, index:int):
        discord_id = str(member.id)        
         

        if discord_id in self.bm_data:
            if len(self.bm_data[discord_id]) >= index:
                return True
            else:
                return True



    def remove_bookmark(self, member: Member, index: int):
        discord_id = str(member.id)        
      

        if discord_id in self.bm_data:

            if len(self.bm_data[discord_id]) >= index:
                self.bm_data[discord_id].pop(index)
                self.save()
                return True


    def create_bookmark_embed(self,member: Member, data: dict):
        
        desc = '*N/A*' if data['content'] == '' else '*'+data['content']+'*'
        embed = Embed(title=f"Category - "+ data['category'], description=desc, color=self.resm.get_color_from_image(member.avatar.url))
        embed.set_author(name=f"{member.display_name} - Bookmark #{data['index']}", icon_url=member.avatar.url)
        if len(data['fields']) > 0:
            for f in data['fields']:

                embed.add_field(name=f['name'], value=f['value'])
        
        if data['image'] !='':
            embed.set_image(url=data['image'])
        
        embed.add_field(name='Jump to', value=data['message_link'])
        embed.set_footer(text=f"Message created at {data['message_time']} - {data['author']}")
        return embed

    def set_bookmark_category(self, member: Member, index: int, category: str):

        discord_id  = str(member.id)
        if discord_id in self.bm_data:

            if len(self.bm_data[discord_id]) >= index:
                self.bm_data[discord_id][index]['category'] = category
                self.save()
                return True




