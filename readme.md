![Logo](https://github.com/reko-beep/paimon-bot/blob/dev/logo.png?raw=true)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/reko-beep/)
# Paimon Bot [DEV]

> Dev version , features are added as per need, there might be some bot breaking bugs

# Currently Working on
 ```
  Nothing

  adding multiple guild supports and 
  sql or some json based db
  (not soon)

 ```

# How to Set Up

 Config file is located in **db** folder.
> db/config.json
  ```  
    {
        "token": "",
        "site": "",
        "uid_channel": 0, 
        "coop_channel": 0,
        "coop_roles": [], 
        "cookies": {"ltuid": "", "ltoken": ""}, 
        "admin_roles": [],
        "approve_role": 0, 
        "member_role": 0,
        "approve_channel": 0, 
        "teamcomp_role": 0, 
        "scrutiny": true, 
        "liben": false, 
        "art_channel": 0, 
        "leak_channel": 0, 
        "owner_bot": 0, 
        "nuke_enabled": false
    }
 ```

  ### Setting up approve 
  Scrutiny is set to true when you want to manually approve members.
  ```js
  {
      approve_role: ID of the role which user will be given when they join
      member_role: ID of the role which a approved or normal member of user will have
      scrutiny: bool | true | false


  }
  ```

  ### Setting up channels

  ```js
  {
    uid_channel: ID of the channel where user will drop their uids, and bot will link them
    approve_channel: ID of the channel where new members will get pinged to answer the  question
    art_channel : ID of the channel where user share arts, helpful if you want to have high quality images posted instead of a discord pixiv preview
    leak_channel: ID of the channel where leakers post leaks helpful to prevent chatting there
    coop_channel: ID of the channel where users will ping carry roles
  }
  ```
   ##### NOTE
    > You can bypass text filter by using ``>>`` in your text

  ### Setting up Carry Roles
  ##### NOTE
    > Carry roles must contain EU, NA, Asia in their names

  ```js
  {
    coop_roles: [
      ID of Carry roles, seperated by commas
    ]
  }
  ```

  ### Liben Module

  > Liben module is helpful in marvelous merchandise event, see bot commands for further info


  ### Setting up genshin api

  ```js
  {
    cookies: 
    {
      ltuid: ltuid value here
      ltoken: ltoken value here
    }
  }
  ```
  #### Get cookies for your bot
    go to hoyolab.com
    login to your account
    press F12 to open inspect mode (aka Developer Tools)
    go to Application, Cookies, https://www.hoyolab.com.
    copy ltuid and ltoken
    use set_cookie(ltuid=..., ltoken=...) in your code
 
 ### Miscellaneous roles

 ```js
 {
  admin_roles: [IDs of admin roles seperated by commas] #required for some admin limited commands

  teamcomp_role: ID of role who theorycrafts or add teamcomps to bot
  best_cooper: ID of the role that will be given to users who comes out on top at coop leader board

  comms_in_hr: hr in 24 format when ur comms reset 

 }

 > NOTE: change your bot vps timezone according to it
 ```

  ### Bot Settings

  ```js
  {
    owner_bot: bot owner ID
    token: Discord bot Token
    site: if you have a site specific for bot, redirected to bot vps ip
  }
  ```


# Help in documenting commands

  If you are willing to document commands,
  > edit .py files in cog for this

  ```py
  @commands.command(aliases=['cpp'], description='cpp (user)\n user argument is optional\nshows the coop profile of the user who invoked the command or the mentioned user', brief='shows user coop profile')
  async def cpp(self, ctx, user: Member=None)
    ......
  ```



# Contribution

    Fork and commit to dev branch.