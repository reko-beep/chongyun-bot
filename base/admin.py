from json import load, dump
from nextcord import Member, Embed, File, TextChannel, Attachment
from nextcord.utils import get
from dev_log import logc
from nextcord.ext.commands import Context
from requests import Session
from os import listdir
from os.path import isfile, join, getsize, islink
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from bs4 import BeautifulSoup
import requests

from saucenao_api import SauceNao
class Administrator:
    def __init__(self, bot):
        self.bot  = bot
        self.approve_role = None
        self.member_role = None
        self.approve_channel = None
        self.scrutiny = self.bot.b_config.get("scrutiny", True)
        self.saucenao = SauceNao('41c00808668a6fd17a551801c087cdf4d6e3b3bf')
    

    def check_admin(self, ctx: Context):
        if ctx.author.id == self.bot.b_config.get('owner_bot'):
            return True
        else:
            r = [i.id for i in ctx.author.roles]
            return len(set(r).intersection(self.bot.b_config.get("admin_roles"))) != 0

    def load_roles_channels(self, guild):
        if self.member_role is None:
                self.member_role = get(guild.roles, id=self.bot.b_config.get("member_role"))
        if self.approve_role is None:
                self.approve_role = get(guild.roles, id=self.bot.b_config.get("approve_role"))
                print("roles loaded", self.approve_role, self.member_role)
        if self.approve_channel is None:
            self.approve_channel = get(guild.channels, id=self.bot.b_config.get('approve_channel'))        
            print("channels loaded", self.approve_channel)


    async def send_approve_message(self, member:Member):

        embed = Embed(title='Please answer these questions!', description='1. Where are you from?\n2.Where did you get the invite from?\n\n*our mods will approve as soon as possible*\n\n**Gender roles are not self assignable\n contact mods if you want em**\n', color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        if self.approve_channel is not None:
            await self.approve_channel.send(member.mention, embed=embed)


    async def approve_member(self, ctx: Context, member: Member):

        if self.check_admin(ctx):
            if self.member_role is None:
                self.member_role = ctx.guild.get_role(self.bot.b_config.get("member_role"))
            await member.edit(roles=[self.member_role])
            return True

    async def member_role_check(self, member: Member):
        print(self.scrutiny)
        if self.scrutiny:     
            print('role', self.approve_role)
            if self.approve_role is not None:  
                logc('scrutiny is set to', self.scrutiny, '\n', 'role to give', str(self.approve_role))     
                await member.add_roles(self.approve_role)
                await self.send_approve_message(member)
        else:
            print('role', self.member_role)
            if self.member_role is not None:   
                logc('scrutiny is set to', self.scrutiny, '\n', 'role to give', str(self.member_role))     
                await member.add_roles(self.member_role)

    
    def search_url(self, search_str: str, channel: TextChannel, page: str):
        tag = False
        if search_str.strip().startswith('t:'):
            tag = True
        tag_check = None
        filter_ = '&mode=safe'
        if channel.is_nsfw():
            filter_ = '&mode=all'
        if tag:
            return f"https://www.pixiv.net/ajax/search/artworks/{search_str.replace('t:','',1).strip()}?s_mode=s_tag{filter_}&order=popular_d&p={page}"
        else:
            return f"https://www.pixiv.net/ajax/search/artworks/{search_str}{filter_.replace('&','?',1)}&order=popular_d&p={page}"

    def pixiv_search(self, search:str, channel: TextChannel, page):
        LINK = self.search_url(search, channel, page)
        print('search url', LINK)
        session = Session()
        headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "referer": "https://pixiv.net/"
        }
        if '/artworks/' in search and 'pixiv.net' in search:
            data = session.get(f"http://pixiv.net/ajax/illust/{search.split('/')[-1]}", headers=headers).json()
            if len(data['body']) != 0:
                return [data['body']]
        
        else:
        
            data = session.get(LINK, headers=headers).json()
            if 'illustManga' in data['body']:
                return data['body']['illustManga']['data']
        

    def get_pixiv_local(self):
        local = []
        base_path = self.bot.resource_manager.path.format(path='pixiv/')
        ids = [f.split('.')[0] for f in listdir(base_path) if isfile(join(base_path, f))]
        print('ids', ids)
        for id in ids:            
            local += [{'id': id, 'title': f'PIXIV ID - {id}', 'tags': ['N/A']}]
        
        return local





    def pixiv_embeds(self, data: list, footer:str='Pixiv'):
        embeds = []
        for pic in data:
            if pic.get("id", None) != None:
                user = f"by *{pic.get('userName', 'N/A')}*"
                embed = Embed(title=pic.get('title', 'No title'),description=f"{user}\n{pic.get('description', 'No description')}", url=f"https://pixiv.net/en/artworks/{pic['id']}")
                img_link = self.bot.resource_manager.site.replace('/assets',f"/pixiv/{pic['id']}",1)
                print(img_link)
                embed.set_image(url=img_link)
                tags = '*'+',*'.join(pic.get('tags', ['N/A']))
                embed.add_field(name='Tags', value=tags)
                embed.add_field(name='Download', value=f"[click here](http://178.62.90.249:80/pixiv/{pic.get('id')})")
                embed.set_footer(text=footer)
                embeds.append(embed)
        return embeds

    def get_original_pixiv_image(self, link):
        LINK = "https://pixiv.net/ajax/illust/{id}"


        session = Session()
        headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "referer": "https://pixiv.net/"
        }

        provided_link = link.split("/")[-1]
        print('provided link', LINK.format(id=provided_link))


        links = session.get(LINK.format(id=provided_link), 
                    headers=headers)
        data = links.json()
        image = data['body']['urls']['original']
        title = data['body']['title']
        username = data['body']['userName']
        
        
        print('original image link', image)
        with session.get(image, headers=headers, cookies=links.cookies) as u:
            
            return { 'title': title, 'username': username, 'file': File(BytesIO(u.content), filename='image.png')}

    def create_code_image(self, code: str):
    
        path = self.bot.resource_manager.path.format(path='/misc/code.png')
        font = self.bot.resource_manager.path.format(path='/misc/font.otf')

        f = ImageFont.truetype(font, 95)
        img = Image.open(path, 'r').convert('RGBA')

        ImageDraw.Draw(img).text((250, 430), code, fill=(255,255,255), font=f)
        bytes_ = BytesIO()
        img.save(bytes_, 'PNG')
        bytes_.seek(0)
        return bytes_
    
    def create_code_embed(self, code:str):

        embed = Embed(title='Announcement', description=f'\n\n**CODE:**\n```css\n{code.upper()}\n```', color=0x196a87)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='Link for redeeming code', value=f'https://genshin.hoyoverse.com/en/gift?code={code.upper()}')
        embed.set_image(url='attachment://code.png')
        file = File(self.create_code_image(code.upper()), filename='code.png')

        return embed, file



    def zerochan_search(self, search: str, page:int=1):
    
        Link = f'https://www.zerochan.net/{search}?p={page}'
        headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "referer": "https://www.zerochan.net/"
        }
        session = Session()
        src = session.get(Link, headers=headers).content
        bs = BeautifulSoup(src, 'lxml')

        images = bs.find_all('li')
        if len(images) > 0:
            images_links = []
            for img in images:
                link = img.find("p")
                if link is not None:
                    if link.find('a') is not None:
                        images_links.append(link.find('a').attrs['href'])
        
            return images_links

    def zerochan_embeds(self, member: Member, title_:str, links: list):

        embeds = []

        for link in links:
            if len(link.split('/')[-1].split('.')) > 3:
                link_ = f"https://zerochan.net/"+link.split('/')[-1].split('.')[-2]
                embed = Embed(title=f'{title_.title()} images', description=f"[Source Link]({link_})", color=self.bot.resource_manager.get_color_from_image(member.avatar.url))
                embed.set_image(url=link)
                embed.set_author(name=member.display_name, icon_url=member.avatar.url)

                embed.set_footer(text=f"{title_.title()} - search results")
                embeds.append(embed)
        
            
        return embeds

    def danborou_search_tag(self, search: str, page:int=1):
    
        SEARCH_TAG_NSFW = f'https://danbooru.donmai.us/autocomplete.json?search[query]={search.replace(" ", "_", 99)}&search[type]=tag_query&limit=10'
        session = Session()
        
        URL = SEARCH_TAG_NSFW
        REFERER = URL[:URL.find(URL.split('/')[2])+len(URL.split('/')[2])+1]
        headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "referer": REFERER
        }

        tags = session.get(URL, headers=headers).json()
        print(URL, tags)
        tags_search = []
        if len(tags) > 0:
            for t in tags:
                if '(' in t['label']:
                    tags_search.append(t['label'].replace('_',' ', 99).lower().split('(')[0])
                else:
                    tags_search.append(t['label'].replace('_',' ', 99).lower())
        if len(tags_search) == 0:
            tags_search = None   
        LINK_NSFW = f'https://danbooru.donmai.us/posts?page={page}&tags=&z=2' if page != 1 else f'https://danbooru.donmai.us/posts?tags=&z=2'
        LINK =  LINK_NSFW
        if tags_search is not None:

            for c, tag in enumerate(tags_search):
                if search.lower() in tag.lower():
                    return LINK.replace('tags=', 'tags='+tags[c]['value'], 1), session

    def danbooru_source(self, post_id: str):
        LINK = f'https://danbooru.donmai.us/posts/{post_id}?variant=tooltip&preview=false'
        print(LINK)
        src = requests.get(LINK).content
        bs = BeautifulSoup(src, 'lxml')

        source = bs.find('a', {'class': 'post-tooltip-source'})
        if source is not None:
            return source.attrs['href']

    def danborou_images_links(self, link: tuple, safe: bool=True):

        if type(link) == tuple:

            session = Session()
            session : Session = link[1]

            src = session.get(link[0]).content
            nsfw_filters = ['1girl', 'absurdres', 'blush', 'breasts', 'convenient_censoring', 'covered_nipples', 'medium_breasts', 'mole', 'mole_under_eye', 'nude', 'open_mouth', 'spread_legs', 'sweat',  'all_fours', 'areolae', 'ass',  'blindfold', 'breasts', 'cum', 'cum_on_body', 'cum_pool', 'hanging_breasts', 'large_breastsnipples', 'onsen', 'see-through']
            bs = BeautifulSoup(src, 'lxml')
            images = bs.find_all("article")
            links = []
            for link in images:
                if safe:
                    print(list(link.attrs.keys()))
                    if link.attrs['data-rating'] == 's':
                        link_img = link.find("a").find("img").attrs['src'] if link.find("a") is not None else ''

                        if link_img is not None and link_img != '':                            
                            links.append({"img" : link_img.split("/")[-1], "src" : "https://danbooru.donmai.us"+link.find("a").attrs['href']})
                else:
                    link_img = link.find("a").find("img").attrs['src'] if link.find("a") is not None else ''
                    if link_img is not None and link_img != '':
                        links.append({"img" : link_img.split("/")[-1], "src" : "https://danbooru.donmai.us"+link.find("a").attrs['href']})

            return links

    def danbooru_post_id(self, link:str):
        
        LINK = 'https://danbooru.donmai.us/posts/{post_id}?variant=tooltip&preview=false'
        if '/post/' in link or '/posts/' in link and 'danbooru.donmai.us' in link and 'http' in link:
            session = Session()

            src = session.get(LINK.format(post_id=link.split("/")[-1])).content
            bs = BeautifulSoup(src, 'lxml')
            data = []
            if bs.find('a', {'class': 'post-tooltip-dimensions'}) is not None:
                src = 'https://danbooru.donmai.us/posts/{post_id}'.format(post_id=link.split("/")[-1])
                image_file = bs.find('a', {'class': 'post-tooltip-dimensions'}).attrs['href'].split('/')[-1]
                data.append({'img': image_file, 'src': src})
                return data

        

    def danbooru_embeds(self,member: Member, search:str,page:int=1, sfw:bool=True):
       
        search_obj = self.danborou_search_tag(search, page)
        print('danbooru direct link', search.startswith('https://danbooru.donmai.us/posts/'))
        if '/posts/' in search or '/post/' in search and 'danbooru.donmai.us' in search and 'http' in search:
            data = self.danbooru_post_id(search)
        else:
            data = self.danborou_images_links(search_obj, sfw)
        embeds = []
        if data is not None:
            if len(data) > 0:
                color = self.bot.resource_manager.get_color_from_image(member.avatar.url)
                for img in data:
                    if '/posts/' in search or '/post/' in search and 'danbooru.donmai.us' in search and 'http' in search:
                        
                        embed = Embed(title=f"{search.split('/')[-1]} ID - Danbooru Image", url=img['src'],  color=color)
                    else:

                        embed = Embed(title=f'{search.title()} Danbooru Image', url=img['src'],  color=color)
                    embed.set_author(name=member.name, icon_url=member.avatar.url)
                    img_link = self.bot.resource_manager.site.replace('/assets',f"/danbooru/{img['img']}",1)
                    id_ = img['src'].split('/')[-1][:img['src'].split('/')[-1].find('?')]

                    src = self.danbooru_source(id_)
                    if src is not None:
                        embed.add_field(name='Source', value=f"[click here]({src})")
                    embed.set_image(url=img_link)
                    if '/posts/' in search or '/post/' in search and 'danbooru.donmai.us' in search and 'http' in search:
                        
                        embed.set_footer(text=f"{search.split('/')[-1]} ID - Danbooru Images")
                    else:
                        embed.set_footer(text=f'{search.title()} Danbooru Images')
                    embeds.append(embed)
                return embeds

    def danbooru_local(self, member: Member):
        base_path = self.bot.resource_manager.path.format(path='danbooru/')
        ids = [f for f in listdir(base_path) if isfile(join(base_path, f))]
        size = 0
        for f in listdir(base_path):
            if isfile(join(base_path, f)):
                if not islink(join(base_path, f)):
                        size += getsize(join(base_path, f)) >> 20

        print('ids', ids)
        embeds = []
        color = self.bot.resource_manager.get_color_from_image(member.avatar.url)
        for id in ids:            
            embed = Embed(title=f'Danbooru Image', color=color)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            img_link = self.bot.resource_manager.site.replace('/assets',f"/danbooru/{id}",1)
            print(img_link)
            embed.set_image(url=img_link)
            embed.set_footer(text=f'Danbooru Images - Files {len(ids)} - Size {size} MB')
            embeds.append(embed)
        
        return None if len(embeds) == 0 else embeds
    
    def saucenao_embed(self, img: str):
        img_url = img        
        
        results = self.saucenao.from_url(img_url)
        if bool(results):
            embeds = []
            for i in range(len(results)):
                print({k : results[i].__dict__[k] for k in results[i].__dict__})
                site_name = None
                url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                if bool(results[i].urls):
                    site_name = results[i].urls[0].split('/')[2].split('.')[-2]
                    url = results[i].urls[0]
                thumbnail = results[i].thumbnail
                title = str(results[i].title)
                author = str(results[i].author)
                limit = f'Remaining sauce search limit {results.short_remaining} (per 30 seconds limit) {results.long_remaining} (per day limit)'

                embed = Embed(title=title, color=self.bot.resource_manager.get_color_from_image(thumbnail))
                embed.add_field(name='Source', value=f"[{site_name}]({url})")
                embed.set_thumbnail(url=thumbnail)
                embed.set_author(name='Author: '+author)
                embed.set_footer(text=limit)

                embeds.append(embed)



            return embeds if len(embeds) > 0 else None
