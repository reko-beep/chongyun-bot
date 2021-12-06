import json
import genshinstats as gs
from json import load, dump
from os import getcwd,listdir
from os.path import isfile, join, exists
from nextcord import Embed, Message

gs.set_authkey('https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?im_out=true&sign_type=2&auth_appid=im_ccs&authkey_ver=1&win_direction=portrait&lang=en&device_type=pc&ext=%7b%22loc%22%3a%7b%22x%22%3a2135.71142578125%2c%22y%22%3a236.3440704345703%2c%22z%22%3a-1646.5523681640625%7d%2c%22platform%22%3a%22WinST%22%7d&game_version=OSRELWin2.3.0_R5102609_S5082883_D5109732&plat_type=pc&authkey=g1HzKWxZwl%2bENsH9i1aRd8vdsFSxtGOVps6x28TeBvdof5GWdNcwaE%2b9qEthcuDwUpILKvPXycmemAdbyffYYe2niptZ9Xq2FZvxyWuetVXD6PDr9I6l3ftjrvLNgS8sCVVD1pIxifPXFFLfA6wlL%2b07wOz03x54K610tdomsBtB2u8h55Zc0BSJHppGVIYahVC1evkD9xZXuMt%2bgdHiO8qxQ1cbp9rlcDYfOAeqFzBvQquugY7wmk15rqNy1FVHT7XrqSbaMf%2fnRHqoBrNwZ4uRfJJfo9ucjxKgkR4t0W%2fPa73cqJFR%2fz8hzHbyXMYNjoPYwyIGVKzYJAXP5GUHInfdxVUEKRU%2f5pz4fDrzhZfJTawGxeyM6h9PeJltlEEuYrHReNnwvEumyGOLTSMd0NXGXDe2W84zDAHtZzGyAN8ld8Q9seXfFFXrvgVkJcfqF2LKCHvCEiVrEaxExDL9Fcnau9QlhjL%2bWf69a%2bgzJ3K5iYHQaKcq057CuIzFq%2b5iu6VLWzGnMF4ZOpfsGLeYz24nLiTJpJVRkK9JRPTdaE%2fi%2fxJ3aKyx0oZiz4IqaDFNZxSYOra1Fk3xUSX1mymxSP5A82qgdR0G%2b4d3srOlsylrmU9pCU4BjjBp6zbPxYz%2bzD1J0rZeNjyPvEZOlsHiLR9ymKWbQGywGOgodJu%2bfYzaFbUhseTLsi9DLQ52UsDFfI6nbgMEV6Cv5eahDa9RyLwwovvEr6oDYqLW0gRZCLgdVxk1F%2fjFtwKtr3dMukCxvcUKg%2fPuFoZUINmI1PAIdMb4OvlmIyXyocQahs%2blvlrMSVYdidxPz9KUNzk38yyRg1m%2fu2vAfTjklA7Tk6OppPzH9A%2fh1XhLRBW6l7U2vVuWLcP1wL%2fnLPZ5CXt4DToCR4sIp92GpSStSqBm99ezSrB7XGV6nozfi4aLL7vJbcn83gt6SL9Bi5oltjMd%2bhYQkLPZaqaAnSKh315ALM5XzLwzWLF0aAEDdEr3TdaHHtjX5cDVjsY3t05IeY4I5sgegP7Vd9aIHR2lMzles4FVC7%2flzD4vEugnwXJjKaspZ%2ftnCD5%2fHmQ7aZ4JfdbEiFkmn6ZGW3rC%2f6JlXNDS2LbbcUim41bLKWnvrTBet8Tg%2fhZ6Bt3f%2fUW3qAOUh7zltBhymtT4OUn%2bKk1e4kzSOnlm6l9v6xwLan9fgO9PJcxn0wT9wd%2bKo2dYxL6TOumoXUaZlRNTAXSnTI8lePl4g90PlGC%2fyog64eKrLcVyq8LzmIxWJsL5PQE4RHpKq4pjXvJvkOHT0pohkIn1C5rhsnoJjSydgSzEYDPfsqopkAt0dGyDQDHzrvw%2fTq1bmimbHc87%2bCYCfAjxKVhIvLj7bXjkOg%3d%3d&game_biz=hk4e_global#/')


class Logs:
    def __init__(self, pmon):
        self.pmon = pmon
        self.ids = []
        self.path = f'{getcwd()}/assets/logs/'
        self.ltuid = self.pmon.p_bot_config['ltuid']
        self.ltoken = self.pmon.p_bot_config['ltoken']
        self.load_ids()
        pass

    def load_ids(self):
        self.ids = [id_.split('.')[0] for id_ in listdir(self.path) if isfile(join(self.path,id_))]

    def array_dif(self, prev_array, new_array):
        array_diff = []
        for array in new_array:
            if array not in prev_array:
                array_diff.append(array)
        return array_diff

    def create_status_embed(self, message: str):
        embed = Embed(title=f' Fetching status', description=f'{message}', color= 0xf5e0d0)
        embed.set_thumbnail(url='https://64.media.tumblr.com/7a2c8a4e95b83266f60bf8f44e074926/9e53aa2b8d88992a-cc/s400x600/a8fbcb8815eb9df66451d89261a220c2381eb025.gif')
        return embed
      
    async def fetch_alllogs(self, authkey, message: Message):
        gs.set_cookie(ltuid="6457775",ltoken="tJLdlousrYagG8jky6vKNJpKWnqS8joxuby1D3mS")
        gs.set_authkey(authkey)
        save_data = {}
        data = list(gs.get_primogem_log())
        uid = data[0]['uid']
        await message.edit(embed=self.create_status_embed('Fetched primogems history!'))
        save_data['primogem'] = data
        data = list(gs.get_artifact_log())
        save_data['artifact'] = data
        await message.edit(embed=self.create_status_embed('Fetched Artifacts history!'))
        data = list(gs.get_crystal_log())
        save_data['crystal'] = data
        await message.edit(embed=self.create_status_embed('Fetched Crystals history!'))
        data = list(gs.get_resin_log())
        save_data['resin'] = data
        await message.edit(embed=self.create_status_embed('Fetched Resins history!'))
        temp_data = {}
        if exists(f'{self.path}/{uid}.json'):
            with open(f'{self.path}/{uid}.json','r') as f:
                temp_data = load(f)
        
        keys = ['primogem','artifacts','crsytal','resin']
        for key in keys:
            if key in save_data:
                if key in temp_data:
                    diff = self.array_dif(temp_data[key],save_data[key])
                    save_data[key] += diff
        
        with open(f'{self.path}/{uid}.json','w') as f:
                dump(save_data,f)
        if uid not in self.ids:
            self.ids.append(uid)
        await message.edit(embed=self.create_status_embed(f'**UID:**\n{uid}\nAll done!\n'))

    def check_uid(self, uid):
        if uid in self.ids:
             return f'{self.path}/{uid}.json'

    def get_data(self, key, uid):
        
        check_ = self.check_uid(uid)

        if check_ is not None:

            with open(f'{self.path}/{uid}.json','r') as f:
                data = load(f)
                if key in data:
                    return data[key]

    def get_image(self, key):
        images = {'artifacts': 'https://rerollcdn.com/GENSHIN/Gear/lucky_dog.png',
                'primogems': 'https://static.wikia.nocookie.net/gensin-impact/images/5/52/Item_Primogem_Old_CBT1.png',
                'resins': 'https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png',
                'crystals': 'https://static.wikia.nocookie.net/gensin-impact/images/4/44/Item_Genesis_Crystal.png'}
        if key in images:
            return images[key]

    def create_pages( self, list, limit, member, type):

        count = divmod(len(list),limit)
        page_count = 0
        if count[1] != 0:
            page_count = count[0]+ 1 
        embeds = {}
        for page in range(1, page_count+ 1,1):
            description = ''
            max_ = page*limit
            if max_ > len(list):
                max_ = len(list)
            min_ = max_-limit
            if min_ < 0:
                min_ = 0
            if min_ == 0:
                list_iter = list[:max_]
            else:
                list_iter = list[min_:max_]
            embed = Embed(title=f'{member.display_name} {type.title()} logs', description = description, color= 0xf5e0d0)
            for item in list_iter:
                if 'name' in item:
                    if item['amount'] in [-1, 1]:
                        value = "Gained" if item['amount'] == 1 else "Used"
                    else:
                        value = item['amount']
                    embed.add_field(name=item['name'], value=f"{value}\nReason: {item['reason']}")
                else:
                    embed.add_field(name=f"{item['amount']} {type.title()}", value=f"Reason: {item['reason']}")
                        
            image = self.get_image(type)
            if image is not None:
                embed.set_thumbnail(url=image)
            
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embeds[f'Page {page}'] = embed
        return embeds

    def create_artifact_embed(self, ctx, uid):

        data = self.get_data('artifact', uid)

        if data is not None:

            embeds = self.create_pages(data, 10, ctx.author, 'artifacts')

            return embeds

    def create_primogem_embed(self, ctx, uid):
    
        data = self.get_data('primogem', uid)

        if data is not None:

            embeds = self.create_pages(data, 10, ctx.author, 'primogems')

            return embeds

    def create_crystal_embed(self, ctx, uid):
        
        data = self.get_data('crystal', uid)

        if data is not None:

            embeds = self.create_pages(data, 10, ctx.author, 'crystals')

            return embeds

    def create_resin_embed(self, ctx, uid):
        
        data = self.get_data('resin', uid)

        if data is not None:

            embeds = self.create_pages(data, 10, ctx.author, 'resins')

            return embeds
        

            

