# paimon-bot
 

![Logo](https://github.com/reko-beep/paimon-bot/blob/main/logo.gif?raw=true)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/reko-beep/)


Paimon bot created for discord community of Pakistan Genshin Impact server, you are free to use it, if you want!
it contains

    🔸 Paimon soundboard! (sounds provided)
    🔸 Support for build and ascension commands (you need to add yours own in the respective folder)
    🔸 Paimon quotes (taken from paimonquotes twitter handle!)
    🔸 Quests with chapters and acts. (Guides taken from Genshin Impact fandom page!)
    🔸 An anime command, cuz felt the need for server.
    🔸 Shows genshin stats from hoyolab (api wrapper by thesadru on github)

# Setting up the bot
 
 Change the **settings.json** file according to your needs!

 **announce_channel** is where paimon bot will make announcements!

**announcement.json** is file containing a sample announcement, it will post that announcement in announcement channel, when the bot starts!
setting **announce** to **true** will post the announcement if bot is restarted, and **false** will not.

 **dropuid_channel** is the one where users will post their uids along with region, so bot will automatically link it.

 Linking Format:
 ```
 eu: uid
 asia: uid
 na: uid
 ```

 **bump_channel** is the one where disboard bump commands will be, so bot can respond to the successful bump!

 **NOTE**: if you want to disable it just change it to 0.

 **events_channel** is the one where bot will post upcoming channels!

 **NOTE**: if you want to disable it just change it to 0.

 **approve_role** is the role given, when user has verified!
 **scrutiny_role** is the role which would be given to a new user, if scrutiny is turned on.
 **verify_channel** is the channel where paimon will post a sample of question which you want to ask!

 **NOTE**: change it in on_member_join function!

 **mod_role** is the role for mod commands! like scrutiny.
 
 **lobbycreatevc** is the voice channel which will create custom lobbies when a user joins it.
 **NOTE**: if you want to disable it just change it to 0.

# Guides setup

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
 