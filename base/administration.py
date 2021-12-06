from json import dump
from nextcord import Member, Role , Embed, TextChannel, Guild, CategoryChannel, VoiceChannel
from nextcord.ext.commands import Context
from nextcord.utils import get
from core.paimon import Paimon

class AdministrationBase:
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        self.approve_role: Role = None
        self.scrutiny_role: Role = None
        self.scrutiny_channel : TextChannel = None
        

        pass

    def role_check(self, check_roles: list, user_roles: list):
        check = (len(set(check_roles).intersection(user_roles)) != 0)
        return check


    def get_scrutiny(self):
            return self.pmon.p_bot_config['scrutiny']
            

    def toggle_scrutiny(self, ctx: Context):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['scrutiny'] = not self.pmon.p_bot_config['scrutiny']
            self.pmon.p_save_config('settings.json')
            return self.pmon.p_bot_config['scrutiny']

  
    def set_scrutiny_role(self, ctx : Context,role: Role):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['scrutiny_role'] = role.id
            self.scrutiny_role = role
            self.pmon.p_save_config('settings.json')
            return True

    def get_essentials(self, guild : Guild):
        if self.scrutiny_role is None:
            if self.pmon.p_bot_config['scrutiny_role'] != 0:
                self.scrutiny_role = get(guild.roles,id=self.pmon.p_bot_config['scrutiny_role'])
        if self.approve_role is None:
            if self.pmon.p_bot_config['approve_role'] != 0:
                self.approve_role = get(guild.roles,id=self.pmon.p_bot_config['approve_role'])
        if self.scrutiny_channel is None:
            if self.pmon.p_bot_config['scrutiny_channel'] != 0:
                self.scrutiny_channel = get(guild.roles,id=self.pmon.p_bot_config['scrutiny_channel'])
        return True

    def get_scrutiny_channel(self):        
        if self.pmon.p_bot_config['scrutiny_channel'] != 0:
            if self.scrutiny_channel == None:
                self.scrutiny_channel =self.pmon.guilds[0].get_channel(self.pmon.p_bot_config['scrutiny_channel'])
            return self.scrutiny_channel

    def get_lobby_channel(self):        
        if self.pmon.p_bot_config['lobby_createvc'] != 0:            
            return self.pmon.guilds[0].get_channel(self.pmon.p_bot_config['lobby_createvc'])
            

    def get_lobby_category(self):        
        if self.pmon.p_bot_config['lobby_category'] != 0:            
            return self.pmon.guilds[0].get_channel(self.pmon.p_bot_config['lobby_category'])
            

    def set_scrutiny_channel(self, ctx : Context,channel: TextChannel):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['scrutiny_channel'] = channel.id
            self.scrutiny_channel = channel
            self.pmon.p_save_config('settings.json')
            return True

    def set_event_channel(self, ctx : Context,channel: TextChannel):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['events_channel'] = channel.id
            self.pmon.reload_extension('extensions.extra.genshin_events_list')
            self.pmon.p_save_config('settings.json')
            with open('genshin_event_msgs.json','w') as f:
                dump({},f)
            return True

    def get_event_channel(self, ctx : Context):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            channel = get(self.pmon.guilds[0].channels,id=self.pmon.p_bot_config['events_channel'])
            if channel is not None:
                return channel
            

    def set_approve_role(self, ctx : Context,role: Role):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['approve_role'] = role.id
            self.pmon.p_save_config('settings.json')
            return True
    
    def add_mod_role(self, ctx : Context,role: Role):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            if role.id not in self.pmon.p_bot_config['mod_role']:
                self.pmon.p_bot_config['mod_role'].append(role.id)
                self.pmon.p_save_config('settings.json')
                return True

    def remove_mod_role(self, ctx : Context,role: Role):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            if role.id in self.pmon.p_bot_config['mod_role']:
                self.pmon.p_bot_config['mod_role'].pop(self.pmon.p_bot_config['mod_role'].index(role.id))
                self.pmon.p_save_config('settings.json')
                return True

    async def kick_member(self,ctx: Context, member: Member, reason: str = ''):        
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            await member.kick(reason=reason)

    async def ban_member(self,ctx: Context, member: Member, reason: str = ''):        
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            await member.ban(reason=reason)

    async def assign_role(self, member: Member):        
        if self.pmon.p_bot_config['scrutiny']:
            await member.add_roles(self.scrutiny_role)
            return True
        else:
            await member.add_roles(self.approve_role)
            return True

    async def approve_member(self, ctx: Context, member: Member):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            if self.scrutiny_role is None:
                self.scrutiny_role = get(self.pmon.guilds[0].roles,id=self.pmon.p_bot_config['approve_role'])
            await member.edit(roles=[])
            await member.add_roles(self.approve_role)
            return True

    def add_questions(self, ctx: Context, question: str):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            if 'questions' in self.pmon.p_bot_config:
                self.pmon.p_bot_config['questions'].append(question)
            else:
                self.pmon.p_bot_config['questions'] = [question]
            self.pmon.p_save_config('settings.json')
            return True
    
    def clear_questions(self, ctx: Context):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            if 'questions' in self.pmon.p_bot_config:
                self.pmon.p_bot_config['questions'] = []
                self.pmon.p_save_config('settings.json')
                return True

    def create_question_embed(self, member: Member):
        main_statement = 'Please answer the following questions!'
        questions = '\n'.join(self.pmon.p_bot_config['questions'])

        embed = Embed(title=main_statement,
                        description=questions,
                        color=0x5238a3)
        embed.set_author(name=member.display_name,
                            icon_url=member.avatar.url)
        embed.set_thumbnail(url='https://i.imgur.com/mAnIY9E.gif')
        return embed
    
    def set_booster_role(self, ctx: Context, role: Role):
        user_roles = [r.id for r in ctx.author.roles]
        if self.role_check(self.mod_role,ctx.author.roles,user_roles):
            self.pmon.p_bot_config['booster_role'] = role.id
            self.pmon.p_save_config('settings.json')

    def booster_check(self, member: Member):
        if self.pmon.p_bot_config['booster_role'] != 0:
            user_roles = [r.id for r in member.roles]
            return self.role_check([self.pmon.p_bot_config['booster_role']],user_roles)
    
    def get_mod_roles(self):
        roles = self.pmon.p_bot_config['mod_role']
        roles_ = []
        for role in roles:
            role_get = get(self.pmon.guilds[0].roles,id=role)
            if role_get is not None:
                roles_.append(role_get.mention)
        return roles_
    
    
    
    def set_voicecreate_channel(self, ctx : Context, channel: VoiceChannel):
        if self.role_check(self.pmon.p_bot_config['mod_role'],[r.id for r in ctx.author.roles]):
            self.pmon.p_bot_config['lobby_createvc'] = channel.id
            if channel.category is not None:
                self.pmon.p_bot_config['lobby_category'] = channel.category.id
            self.pmon.reload_extension('extensions.extra.lobby')
            self.pmon.p_save_config('settings.json')
            return True