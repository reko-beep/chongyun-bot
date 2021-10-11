import requests
from bs4 import BeautifulSoup
import os
import random
import json
import string
import time
import datetime
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance
import numpy as np
import io

cwd = os.getcwd()
def anidb_data():
    data = {}
    src = ""
    with open(cwd+"/sources/anidb-mapping.xml","r",encoding="utf-8") as f:
        src = f.read()
    bs = BeautifulSoup(src,'lxml')
    animes = bs.find_all("anime")
    for an in animes:
        temp = {}
        if an.find("title",{"type":"official"}) != None:
            english = an.find("title",{"type":"official"}).text
        else:
            english = "Not found!"
        if an.find("title",{"type":"main"}) != None:
            jap = an.find("title",{"type":"main"}).text
        else:
            jap = "Not found!"
        temp = {"en":english,"jap":jap,'url':f"https://anidb.net/anime/{an.attrs['aid']}"}
        data[an.attrs['aid']] = temp
    return data
def remove_seperators(s):
    sep = ['-','_',':','.',',',')','(']
    for i in sep:
        s = s.replace(i,' ',15)
    return s

def case_insensitive(s):
    s = s.lower()
    return s

def mal_data():
    data = {}
    src = ""
    with open(cwd + "/sources/mal-source.xml", "r", encoding="utf-8") as f:
        src = f.read()
    bs = BeautifulSoup(src, 'lxml')
    animes = bs.find_all("loc")
    print(animes)
    for an in animes:
        temp = {}
        t = an.text
        lists = t.split("/")
        title = remove_seperators(lists[5])
        id = lists[4]
        temp = {'en': title, 'url': t}
        data[id] = temp
    return data

def random_letters():
    letters = string.ascii_letters
    t = (''.join(random.choice(letters) for i in range(10)))
    return t





def map_mal_to_anidb(mal_data,ani_data):
    scraper_id = 0

    data = {'data': []}
    for ma in mal_data:
        t = mal_data[ma]['en']
        scraper_letters = random_letters()
        while scraper_letters in data:
            scraper_letters = random_letters()
        else:
            ci_t = case_insensitive(remove_seperators(t)).split(" ")
            for i in ani_data:
                search = []
                temp = {}
                if case_insensitive(remove_seperators(ani_data[i]['jap'])) != "not found":
                    t_1 = case_insensitive(remove_seperators(ani_data[i]['en']))
                    search.append(t_1)
                if case_insensitive(remove_seperators(ani_data[i]['jap'])) != "not found":
                    t_2 = case_insensitive(remove_seperators(ani_data[i]['jap']))
                    search.append(t_2)
                if len(search) > 0:
                    for search_term in search:
                        map = False
                        s_compute = search_term.split(" ")
                        if len(s_compute) == len(ci_t):
                            for map_index in list(range(len(ci_t))):
                                if ci_t[map_index] == s_compute[map_index]:
                                    map = True
                                else:
                                    map = False
                        else:
                            pass
                        if map == True:
                            id_ = f"{scraper_letters} {scraper_id}"
                            temp = {'anidb': {'id': i, 'url': ani_data[i]['url'], 'en': ani_data[i]['en'],
                                              'jap': ani_data[i]['jap']},
                                    'mal': {'id': ma, 'url': mal_data[ma]['url'], 'en': mal_data[ma]['en']}}
                            data['data'].append(temp)
                            break
                        else:
                            pass


    return data


def package_mal_ids():
    latest_id = 0
    ids_package = []
    dead_ids = []
    d= {}
    l_id = requests.get("https://myanimelist.net/anime.php?o=9&c%5B0%5D=a&c%5B1%5D=d&cv=2&w=1").content
    l_id_ = BeautifulSoup(l_id,'html.parser')
    latest_id = l_id_.find("a",{"class":"hoverinfo_trigger fw-b fl-l"}).attrs['href'].split("/")[4]
    print(f"Last added id: {latest_id}")
    list_ids = list(range(1,int(latest_id),1))
    for i in list_ids:
        link = f"https://myanimelist.net/anime/{i}"
        print(f" {link} | ID: {i}")
        r = requests.get(link).status_code
        time.sleep(5)
        if r != 404:
            print("Working entry.")
            ids_package.append(i)
        else:
            print("Dead entry.")
            dead_ids.append(i)
        if os.path.exists("ids_package.json"):
            os.remove("ids_package.json")
        with open("ids_package.json", "w") as f:
            d['ids'] = ids_package
            d['dead_ids'] = dead_ids
            json.dump(d, f,indent=1)

def unpack_anime(slugid):
    link = f"https://myanimelist.net/anime/{slugid}"
    r = requests.get(link).content
    bs = BeautifulSoup(r, 'html.parser')
    info_section = bs.find("td",{"class":"borderClass"})
    info = info_section.find_all("span",{"class":"dark_text"})
    data = {}
    data['title'] = remove_seperators(bs.find("a",{"class":"horiznav_active"}).attrs['href'].split("/")[5])
    imgs = find_images(r,"img,id",data['title'])
    data['images'] = {"sd":imgs['sd'], "hd": imgs['hd']}
    data['relations'] = {"anidb": imgs['id']}
    for i in info:
        full_text = i.parent.text
        if i.parent.find("a") != None:
            temp = []
            key = i.text.replace(":", "", 1).lower()
            if key == "score":
                score = bs.find("span",{"itemprop":"ratingValue"})

                if score != None:
                    data['score'] = score.text
            else:
                if key == "ranked":
                    ranked = bs.find("span",{"class":"numbers ranked"})

                    if ranked != None:
                        tex = ranked.parent.text.replace("Ranked","",1).lstrip().rstrip()
                        data['ranked'] = tex[:tex.find("P")]
                else:
                    if key == 'premiered':
                        tex = i.parent.find("a").text.lstrip().rstrip().replace("\n", "", 99)
                        data['season'] = [tex[:-5], tex[-5:]]
                    else:
                        subs = i.parent.find_all("a")
                        for s in subs:
                            t = s.text.lstrip().rstrip()
                            if t != "":
                                temp.append(t)
                        data[i.text.replace(":", "", 1).lower()] = temp

        else:
            key = i.text.replace(":", "", 1).lower()
            if key == "score":
                score = bs.find("span",{"itemprop":"ratingValue"})
                print(score)
                if score != None:
                    data['score'] = score.text
            else:
                if key == "ranked":
                    ranked = bs.find("span",{"class":"numbers ranked"})
                    print(ranked)
                    if ranked != None:
                        data['ranked'] = ranked.parent.text.replace("Ranked").lstrip().rstrip()
                else:
                    data[key] = full_text.replace(i.text, "", 1).lstrip().rstrip()



    if bs.find("p",{"itemprop":"description"}) != None:
        data['synopsis'] = bs.find("p",{"itemprop":"description"}).text.lstrip().rstrip().replace("[MAL Rewrite]","",1)
        background = bs.find("p",{"itemprop":"description"}).parent
        background.find("p", {"itemprop": "description"}).decompose()
        data['background'] = background.text[background.text.find("Background")+len("Background"):]
    if bs.find("table",{"class":"anime_detail_related_anime"}) != None:
        related = bs.find("table",{"class":"anime_detail_related_anime"})
        related_items = related.find_all("td",{"class":"borderClass"})
        for i in related_items:
            if i.find("a") != None:
                key = i.parent.find("td",{"class":"ar fw-n borderClass"}).text.replace(":","",1).lower()
                data[key] = i.find("a").text.lstrip().rstrip().replace("\n","",99)
    if len(bs.find_all("div",{"class":"detail-characters-list clearfix"})) > 0:
        characters = bs.find_all("div",{"class":"detail-characters-list clearfix"})[0]
        character_items = characters.find_all("table")
        characters_list = []
        for i in character_items:
            temp = {}
            if i.find("h3",{"class":"h3_characters_voice_actors"}) != None:
                character_name = i.find("h3",{"class":"h3_characters_voice_actors"})
                if character_name.find("a") != None:
                    temp['character'] = character_name.find("a").text.lstrip().rstrip().replace("\n","",99)
                    temp['role'] = character_name.parent.text.replace(character_name.find("a").text.lstrip().rstrip(),"",1).replace("\n","",99)
            if i.find("td",{"class":"va-t ar pl4 pr4"}) != None:
                va_name = i.find("td",{"class":"va-t ar pl4 pr4"})
                if va_name.find("a") != None:
                    temp['va'] = va_name.find("a").text.lstrip().rstrip()
                    temp['lan'] = va_name.parent.text.replace(va_name.find("a").text.lstrip().rstrip(),"",1).replace("\n","",99)
            if 'character' in temp:
                characters_list.append(temp)
        data['characters'] = characters_list
    if len(bs.find_all("div", {"class": "detail-characters-list clearfix"})) > 1:
        staff = bs.find_all("div",{"class":"detail-characters-list clearfix"})[1]
        staff_items = staff.find_all("td",{"class":"borderClass"})
        staff_list = []
        for i in staff_items:
            temp= {}
            if i.find("a") != None:
                t = i.find("a").text.lstrip().rstrip()
                role = i.parent.text.replace(t,"",1).lstrip().rstrip()
                temp['staff'] = t
                temp['role'] = role
                if temp['staff'] != "":
                    staff_list.append(temp)
        data['staff'] = staff_list
    #opening and ending themes
    if bs.find("div",{"class":"theme-songs js-theme-songs opnening"}) != None:
        tx = bs.find("div",{"class":"theme-songs js-theme-songs opnening"}).text.lstrip().rstrip()
        list_ = []
        if "#" in tx:
            list_ = tx.split("#")
            list_.pop(0)
        data['op'] = list_

    if bs.find("div",{"class":"theme-songs js-theme-songs ending"}) != None:
        tx = bs.find("div",{"class":"theme-songs js-theme-songs ending"}).text.lstrip().rstrip()
        list_ = []
        if "#" in tx:
            list_ = tx.split("#")
            list_.pop(0)
        data['ed'] = list_
    #preview
    if bs.find("a",{"class":"iframe js-fancybox-video video-unit promotion"}) != None:
        data['preview'] = bs.find("a",{"class":"iframe js-fancybox-video video-unit promotion"}).attrs['href'].replace("embed/","watch?v=",1).replace("?enablejsapi=1&wmode=opaque&autoplay=1","",1)
    return data;


def anidb_search(s):
    base_url = f"https://anidb.net/anime/?adb.search={s}&do.search=1"
    r = requests.get(base_url,headers={"authority":"anidb.net","method":"GET",'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'})

    bs = BeautifulSoup(r.content,'html.parser')
    items = bs.find_all("td",{"class":"thumb anime"})
    data = {}
    list = []
    for i in items:
        temp = {}
        if i.find("a") != None:
            temp['id'] = i.find("a").attrs['href'].split("/")[2]
        if i.find("img") != None:
            temp['title'] = i.find("img").attrs['alt']
            temp['img'] = i.find("img").attrs['src'].replace("-thumb.jpg","",1)
        list.append(temp)

    data['data'] = list
    return data






def scrape_anime():
    data = {}
    anime_data = {}
    with open("ids_package.json", "r") as f:
        data = json.load(f)

    for i in data['ids']:
        d = unpack_anime(i)
        print(f"Scraping ID {i} | Title {d['english']}")
        anime_data[i] = d
        time.sleep(5)

        print(anime_data)
        if os.path.exists("anime_package.json"):
            os.remove("anime_package.json")
        with open("anime_package.json", "w") as f:
            json.dump(anime_data, f, indent=1)


def find_images(src,args,title=""):
    r = src
    img_first = ""
    if title != "":
        t = title
    else:
        t = ""
    data_ = {}
    bs = BeautifulSoup(r, 'html.parser')
    img = bs.find("img",{"itemprop":"image"})
    if img != None:
        t = img.attrs['alt']
        img_first = img.attrs['data-src']
        data_['sd'] = img_first
        
    else:
        img_first = 'Not found!'
        data_['sd'] = img_first
    if t != "":
        ani_db = {}
        s = anidb_search(t)
        if len(s['data']) > 0:
            data = s['data'][0]
            a = args.split(",")
            for i in a:
                if i in data:
                    if i == 'img':
                        ani_db['hd'] = data[i]
                    else:
                        ani_db[i] = data[i]
            if 'hd' not in ani_db:
                ani_db['hd'] = "Not Found!"
            data_.update(ani_db)
        else:
            data_['hd'] = "Not Found!"
            data_['id'] = 'Could not be found in ANIDB!'


    else:
        if title != "":
            t = title
            ani_db = {}
            s = anidb_search(t)
            data = s[0]
            if len(s['data']) > 0:
                a = args.split(",")
                for i in a:
                    if i in data:
                        if i == 'img':
                            ani_db['hd'] = data[i]
                        else:
                            ani_db[i] = data[i]
                if 'hd' not in ani_db:
                    ani_db['hd'] = "Not Found!"
                data_.update(ani_db)
            else:
                data_['hd'] = "Not Found!"
                data_['id'] = 'Could not be found in ANIDB!'
        else:
            data_['hd'] = "Not found!"

    print(data_)
    return data_


def last_anime_id(dict):
        keys = []
        for i in dict.keys():
            keys.append(int(i))

        top_ = max(keys)
        return top_




def search_page(search):
    url = f'https://myanimelist.net/anime.php?q={search}&cat=anime'
    r = requests.get(url).content
    bs = BeautifulSoup(r,'lxml')
    items = bs.find_all("img")
    for i in items:
        if i.parent != None:
            if i.attrs['alt'] != "MAL App":
                url = i.parent.attrs['href']
                print(url)
                if url.startswith('https://myanimelist.net/anime/'):
                    slug = url.split("/")[4]
                    return slug,url
    return None,None


def airing_anime():
    r = requests.get('https://myanimelist.net/anime/season/schedule').content
    bs = BeautifulSoup(r, 'html.parser')

    weekday = datetime.date.today().weekday()
    print(f"Weekday in number {weekday}")
    days = ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']
    print(f"Day {days[weekday - 1]}")
    key = f"js-seasonal-anime-list-key-{days[weekday]}"
    print(f"Key to find: {key}")
    weekanime = bs.find('div', {'class': key})
    data = {}
    anime_list = weekanime.find_all('div', {'class': 'seasonal-anime js-seasonal-anime'})
    if anime_list != None:
        for c, i in enumerate(anime_list, 1):
            text = i.find('div', {'class': 'title'}).h2.text.rstrip().lstrip()
            inf = i.find('div', {'class': 'info'}).text.replace("\n", "", 99).rstrip().lstrip()
            time = inf[inf.find("(JST)") - 6:inf.find("(JST)") - 1]
            if ":" in time:
                calc = time.split(":")
                print(f"Dict calc {calc}")
                pak_calc = abs(int(calc[0]) - 4)
                if pak_calc > 12:
                    pak_calc = abs(pak_calc - 12)
                    pak_time = f"{pak_calc}:{calc[1]} PM PKT"
                else:
                    if int(calc[0])-4 < 0:
                        pak_calc = (int(calc[0])-4)+12
                        pak_time = f"{pak_calc}:{calc[1]} PM PKT"
                    else:
                        pak_time = f"{pak_calc}:{calc[1]} AM PKT"

            else:
                pak_time = "N/A"
            data[f"id{c}"] = {'title': text, 'airing': inf, 'converted': pak_time}
        return data

def userstats(user):
    url = f"https://myanimelist.net/profile/{user}"
    r = requests.get(url).content
    bs = BeautifulSoup(r,'lxml')
    items = bs.find_all("span",{"class":"user-status-title di-ib fl-l fw-b"})
    user_stats = {}
    for i in items:
        if i.parent.find("span",{"class":"user-status-data di-ib fl-r"}) != None:
            user_stats[i.text.lstrip().rstrip().replace(":","",9)] = i.parent.find("span",{"class":"user-status-data di-ib fl-r"}).text.lstrip().rstrip()
    img = bs.find("div",{"class":"user-image mb8"})
    if img != None:
        if img.find("img") != None:
            link = img.find("img").attrs['data-src']
            user_stats['img'] = link
        else:
            user_stats['img'] = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
    else:
        user_stats['img'] = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
    anime_stats = {}
    anim = bs.find("div",{"class":"stats anime"})
    stats = anim.find_all("li",{"class":"clearfix mb12"})
    manga_stats = {}
    for st in stats:   
        if st.find("a") != None:
            if st.find("span") != None:
                key = st.find("a").text.lstrip().rstrip().replace(":","",1)
                value = st.find("span").text.lstrip().rstrip().replace(":","",1)
                anime_stats[key] = value
    man = bs.find("div",{"class":"stats manga"})
    stats = man.find_all("li",{"class":"clearfix mb12"})
    manga_stats = {}
    for st in stats:   
        if st.find("a") != None:
            if st.find("span") != None:
                key = st.find("a").text.lstrip().rstrip().replace(":","",1)
                value = st.find("span").text.lstrip().rstrip().replace(":","",1)
                manga_stats[key] = value        
    animes_ = {}
    url += "?status="
    url = url.replace("profile","animelist",1)
    titles = ['watching','completed','hold','dropped','plantowatch']
    airing = ['','Airing','Finished Airing!','Finished Airing']
    for s_ in range(1,8,1):        
        r = requests.get(f"{url}{s_}").content
        bs = BeautifulSoup(r,'lxml')
        data = bs.find("table",{"class":"list-table"}).attrs['data-items']        
        d_ = json.loads(data)  
        ac = 0              
        temp_ = {}
        temp_[str(ac)] = {}        
        for ci in d_:   
            i = ci        
            _temp = {}
            _temp['score'] = i['score']
            _temp['title'] = i['anime_title']
            air = int(i['anime_airing_status'])            
            _temp['airing'] = airing[air]
            _temp['episodes_watched'] = i['num_watched_episodes']
            _temp['episodes'] = i['anime_num_episodes']
            _temp['type'] = i['anime_media_type_string']
            temp_[str(ac)] = _temp
            ac += 1
        animes_[str(s_)] = temp_
        
             
    return user_stats,anime_stats,manga_stats,animes_

def change_color(im,color_tuple):
    r2 = color_tuple[0]
    g2 = color_tuple[1]
    b2 = color_tuple[2]
    data = np.array(im)
    r1, g1, b1 = 167, 67, 163 # Original value    
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]
    im = Image.fromarray(data)
    return im

def generate_bar(list_):
    intrepreted = {}
    colors = {'Watching':(42,160,53),'Reading':(42,160,53),'Completed':(36,63,130),'On-Hold':(226,192,80),'Dropped':(146,44,46),'Plan to Watch':(177,177,177),'Plan to Read':(177,177,177)}
    y = []
    y_ = 0
    for i in list_:
        temp_ = {}
        sort_orders = {}            
        complete = 0
        for c in list_[i]:
            complete += int(list_[i][c])
        if complete == 0:
            for c in list_[i]:                
                perc = 0
                temp_[c] = perc  
            sort_orders = temp_       
        else:
            for c in list_[i]:
                perc = int(list_[i][c])/complete
                temp_[c] = perc    
            sort_orders = dict(sorted(temp_.items(), key=lambda x: x[1], reverse=True))    
        intrepreted[i]= sort_orders
        y_ += 350
        y.append(y_)
                
    print("Intrepreted percentages",intrepreted)
    main = Image.new('RGBA', (1920, 1080))
    r = 'bg.png'
    bg = Image.open(r)
    main.paste(bg, (0, 0))
    pos = 0    
    for items in intrepreted:            
        bar = Image.new('RGBA', (1000, 55))
        bg_ = ImageDraw.Draw(bar)
        bg_.rectangle((0,0, 1000, 55),fill=(167,67,163)) 
        prev_ = 0                
        for c in intrepreted[items]:              
            print("X",prev_,"Width",int(1000*intrepreted[items][c]))
            bg_.rectangle([(int(prev_),0),(prev_+int(1000*intrepreted[items][c]), 55)],fill=colors[c])
            prev_ += int(1000*intrepreted[items][c])                           
        
        dra = ImageDraw.Draw(main)
        fnt = ImageFont.truetype("lithunoa.ttf", 40)
        dra.text((250,y[pos]-55),items.capitalize(),font=fnt,fill=(255,255,255,128))
        main.paste(bar,(250,y[pos]))
        pos += 1

    buffer = io.BytesIO()
    main.save(buffer, format="PNG")
    return buffer

def daily_monogatri_posts():
    link = 'https://www.reddit.com/r/araragi/search.rss?q=flair:%22Fanart%22&restrict_sr=on&sort=new&t=all'
    headers_ = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    r = requests.get(link,headers=headers_).content    
    bs = BeautifulSoup(r,'lxml')
    print(bs.prettify())
    items = bs.find_all("content",{"type":"html"})    
    images_ = []
    for i in items:      
        text_ = i.text                     
        parser = text_
        print("Parser",parser)
        while "href" in parser:
            s = str(find_href(parser))
            parser = parser.replace("href","",1)            
            s = s.strip('"')
            if '.jpg' in s:
                images_.append(s)
                print(f"Found {s}")
            else:
                if '.png' in s:
                    images_.append(s)
                    print(f"Found {s}")              
        print(images_)
    if os.path.exists("monogatri-posts.json"):
        os.remove("monogatri-posts.json")   
        with open("monogatri-posts.json","w") as f:
            d = datetime.datetime.today().weekday()
            day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']            
            data = {'monogatari-posts': [],'day':day_name[d]}
            data['monogatari-posts'] = images_
            json.dump(data,f)
    else:
        with open("monogatri-posts.json","w") as f:
            d = datetime.datetime.today().weekday()
            day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']            
            data = {'monogatari-posts': [],'day':day_name[d]}
            data['monogatari-posts'] = images_
            json.dump(data,f)


    


def find_href(text):
    s = text.find("href")+len("href=")
    t_s = text[s:]
    t_s_s = t_s.find(">")
    t_s_s_s = t_s[:t_s_s]
    return t_s_s_s


