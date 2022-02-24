# paimon-bot
 

![Logo](https://github.com/reko-beep/paimon-bot/blob/main/logo.gif?raw=true)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/reko-beep/)

![END](https://emoji.gg/assets/emoji/1235-paimon-cry.png)

Paimon bot was mainly created for discord community of Pakistan Genshin Impact server, to cater the needs of genshin players there.

### Bot is Discontinued 

    The reason being, I got busy in real life stuff and I cannot manage it.

    you are free to fork and customise this.

# Features

    🧡 Ability to add **Builds** | **Ascension** to bot.
    🧡 Resin Reminder
    🧡 Domain Schedule
    🧡 Fetch basic information of characters and weapons , artifacts along with their ascension.
    🧡 Quests Walkthrough
    🧡 Co-op system with a leaderboard.
    🧡 Fishing Points
    🧡 Wish history [It can fetch wish history and save it, tho code in base/wishhistory.py might be obselete after 2 concurrent banners]
    🧡 Team comps
    🧡 Voicelines of characters
    🧡 Saving Transaction logs or primogems etc
    🧡 OSTS and some more...

# Teamcomps

    Files in : 

        > /assets/teamcomps.json
     Change the owner id from 0 to a discord ID of user for first startup
     
    Images in :

        > /assets/thumbnails/
     are used to create images on the fly

    
    

# Updating database

    Scripts are provided in :

        > /database_maintainer/
    
    They scrape data from genshin fandom to be used by bot.

    See examples.py for quick run.


# Setting up the bot
 
 Change the **settings.json** file according to your needs!
 Basic hints are given there, on how to set up the bot for first run!

 If you need any help, drop a message at reko#2564.


# How can I get my cookies?
**Taken from thesadru/genshinstats github**
1. go to [hoyolab.com](https://www.hoyolab.com/genshin/)
2. login to your account
3. press `F12` to open inspect mode (aka Developer Tools)
4. go to `Application`, `Cookies`, `https://www.hoyolab.com`.
5. copy `ltuid` and `ltoken`
6. use `set_cookie(ltuid=..., ltoken=...)` in your code
> It is possible that ltuid or ltoken are for some reason not avalible in your cookies (blame it on mihoyo).
> In this case there are probably the old `account_id` and `cookie_token` cookies, so use those with `set_cookie(account_id=..., cookie_token=...)`.


# Guides setup

**Delete** delete_this_file.txt in builds and ascension_talents folder.

**Adding new characters**

    Adding folders name for additional characters in characters.json, will add them to bot!

**File Naming**

    builds folder should have character builds whether in jpg or png.
        Naming should be like this for build.

            sub_dps.jpg, its title would translate to Sub DPS in discord embeds.
            main_dps.jpg, its title would translate to Main DPS in discord embeds.
            support.jpg, its title would translate to Support in discord embeds.
            healer.jpg etc, its title would translate to Healer in discord embeds.

    ascension files can be named as you want as their titles are not translated in discord embeds.

 
 
**Guides found on Net**
[GDrive](https://drive.google.com/drive/folders/1482z0uMPGM__NXoThBYboShYEodiXOwT?usp=sharing)

**NOTE**: These were made by world.of.teyvat on instagram, be sure to follow him. No copyrights reserved.
 
