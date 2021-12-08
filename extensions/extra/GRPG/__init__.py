#TODO: too ugly but not a priority right now

import nextcord
from nextcord.emoji import Emoji
from nextcord.enums import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from nextcord.interactions import Interaction

from .grpg.event import Event
from .grpg.Game import Game

class GRPG(commands.Cog):
    def __init__(self, pmon):
        self.pmon = pmon

        self.game = None
        self.embed = None
        self.view = None
        self.players = {}

        self.message = None

    
    @commands.command()
    async def g(self, ctx: Context):

        
        # start a game if there's none or complain
        if self.game is not None:
            await ctx.send("Game is already running!")


        self.players['A'] = {'on_chara': 0, 'user': ctx.author}
        self.players['B'] = {'on_chara': 0, 'user': ctx.message.mentions[0]}

        
        # setup game
        game = Game()
        game.pick_domain("Zhou")
        game.domain.add_player("A", "kaeya", "kaeya")
        game.domain.add_player("B", "kaeya", "kaeya")
        game.main_loop().__next__()

        self.game = game

        embeds, view = self.render(ctx)




        # send or update message.
        if not self.message:
            self.message = await ctx.send(embeds=embeds, view=view)
        else:
            await self.message.edit(embeds=embeds, view=view)



    def render(self, ctx):

        if self.game is None:
            raise Exception('game not init' )
            


        #SECTION: prepare assets.


        # hprf = nextcord.utils.find(lambda e: e.name == 'right_full', ctx.guild.emojis)
        


        # # chara icons
        # kaeya = nextcord.utils.find(lambda e: e.name == 'kaeya', ctx.guild.emojis)
        # mona = nextcord.utils.find(lambda e: e.name == 'mona', ctx.guild.emojis)

        # embed / game screen

        embeds = []

        embedA = nextcord.Embed(title=self.players['A']['user'].name)
        embedA.set_thumbnail(url='https://genshin.honeyhunterworld.com/img/char/kaeya.png')

        for chara in self.game.domain.players['A']['party']:
            chara_name = f"{chara.name} {'*' if chara.is_onfield() else ''}"
            content = (f"❤️ {self.render_hp(ctx, chara.get_hp()/chara.stats.stats['Max HP'].val)}\n"
                      f"{self.render_debuffs(ctx, chara)}.")
            embedA.add_field(name=chara_name, value=content)

    
        embedB = nextcord.Embed(title=self.players['B']['user'].name, color=0x888888)
        embedB.set_thumbnail(url='https://genshin.honeyhunterworld.com/img/char/kaeya.png')
        
        
        for chara in self.game.domain.players['B']['party']:
            chara_name = f"{chara.name} {'*' if chara.is_onfield() else ''}"
            content = (f"❤️ {self.render_hp(ctx, chara.get_hp()/chara.stats.stats['Max HP'].val)}\n"
                      f"{self.render_debuffs(ctx, chara)}.")
            embedB.add_field(name=chara_name, value=content)


        embedC = nextcord.Embed()
        embedC.add_field(name='Comments', value='Nothing to see here yet.')

        embeds = [embedA, embedB, embedC]


        # view / game controls

        controls_view = nextcord.ui.View(timeout=15)


        # buttons

        auto = nextcord.ui.Button(
            style=ButtonStyle.green,
            label='Attack'
        )  
        
        charge = nextcord.ui.Button(
            style=ButtonStyle.green,
            label='Charge'
        )

        swap = nextcord.ui.Button(
            style=ButtonStyle.blurple,
            label='Swap',
            
        )


        # plunge = nextcord.ui.Button(
        #     style=ButtonStyle.gray,
        #     label='Plunge'
        # )



        # skill = nextcord.ui.Button(
        #     style=ButtonStyle.green,
        #     label='Skill'
        # )

        # burst = nextcord.ui.Button(
        #     style=ButtonStyle.green,
        #     label='Burst',
        #     disabled=True
        # )


        # plunge = nextcord.ui.Button(
        #     style=ButtonStyle.blurple,
        #     label='plunge',
            
        # )


        # button handlers

        async def a(i: Interaction):
            
            self.game.events.append(Event(Event.ACTION_AUTO))
            self.game.main_loop().__next__()
            embeds, view = self.render(ctx)
            await self.message.edit(embeds=embeds, view=view)
            pass
        

        async def c(i: Interaction):
            self.game.events.append(Event(Event.ACTION_CHARGE))
            self.game.main_loop().__next__()
            embeds, view = self.render(ctx)
            await self.message.edit(embeds=embeds, view=view)
            pass


        # async def e(i: Interaction):
        #     pass

        # async def q(i: Interaction):
        #     pass

        # async def p(i: Interaction):
        #     pass


        async def s(i: Interaction):
            onfield_chara = self.players[self.game.player]['on_chara']
            onfield_chara = 1 if onfield_chara == 0 else 0

            self.game.events.append(Event(Event.ACTION_SWITCH, onfield_chara))
            self.players[self.game.player]['on_chara'] = onfield_chara            

            self.game.main_loop().__next__()
            embeds, view = self.render(ctx)
            await self.message.edit(embeds=embeds, view=view)
            pass


        charge.callback = c
        auto.callback = a
        swap.callback = s
        # skill.callback = e
        # burst.callback = q
        # plunge.callback = p
  
        controls_view.add_item(auto)
        controls_view.add_item(charge)
        controls_view.add_item(swap)
        # controls_view.add_item(plunge)
        # controls_view.add_item(skill)
        # controls_view.add_item(burst)

        return embeds ,controls_view
        

    def render_hp(self, ctx, fraction):

        max_size = 10
        
        # health bar emotes
        hple = nextcord.utils.find(lambda e: e.name == 'left_empty', ctx.guild.emojis)
        hpll = nextcord.utils.find(lambda e: e.name == 'left_low', ctx.guild.emojis)
        hplf = nextcord.utils.find(lambda e: e.name == 'left_full', ctx.guild.emojis)
        hpls = nextcord.utils.find(lambda e: e.name == 'left_sat', ctx.guild.emojis)

        hpme = nextcord.utils.find(lambda e: e.name == 'middle_empty', ctx.guild.emojis)
        hpml = nextcord.utils.find(lambda e: e.name == 'middle_low', ctx.guild.emojis)
        hpmf = nextcord.utils.find(lambda e: e.name == 'middle_full', ctx.guild.emojis)
        hpms = nextcord.utils.find(lambda e: e.name == 'middle_sat', ctx.guild.emojis)

        hpre = nextcord.utils.find(lambda e: e.name == 'right_empty', ctx.guild.emojis)
        hprl = nextcord.utils.find(lambda e: e.name == 'right_low', ctx.guild.emojis)
        hprf = nextcord.utils.find(lambda e: e.name == 'right_full', ctx.guild.emojis)


        hp_bar = ''
        hp_units = round(fraction * max_size)

        # BRUH MOMENT
        if hp_units == 0:
            hp_bar += f"{hple}{hpme}{hpme}{hpme}{hpre}"
        elif hp_units == 1:
            hp_bar += f"{hpll}{hpme}{hpme}{hpme}{hpre}"
        elif hp_units == 2:
            hp_bar += f"{hplf}{hpme}{hpme}{hpme}{hpre}"
        elif hp_units == 3:
            hp_bar += f"{hpls}{hpml}{hpme}{hpme}{hpre}"
        elif hp_units == 4:
            hp_bar += f"{hpls}{hpmf}{hpme}{hpme}{hpre}"
        elif hp_units == 5:
            hp_bar += f"{hpls}{hpms}{hpml}{hpme}{hpre}"
        elif hp_units == 6:
            hp_bar += f"{hpls}{hpms}{hpmf}{hpme}{hpre}"
        elif hp_units == 7:
            hp_bar += f"{hpls}{hpms}{hpms}{hpml}{hpre}"
        elif hp_units == 8:
            hp_bar += f"{hpls}{hpms}{hpms}{hpmf}{hpre}"
        elif hp_units == 9:
            hp_bar += f"{hpls}{hpms}{hpms}{hpms}{hprl}"
        elif hp_units == 10:
            hp_bar += f"{hpls}{hpms}{hpms}{hpms}{hprf}"
    
        return hp_bar


    def render_debuffs(self, ctx, chara):
        # element emotes
        pyro = nextcord.utils.find(lambda e: e.name == 'pyro', ctx.guild.emojis)
        dendro = nextcord.utils.find(lambda e: e.name == 'dendro', ctx.guild.emojis)
        anemo = nextcord.utils.find(lambda e: e.name == 'anemo', ctx.guild.emojis)
        geo = nextcord.utils.find(lambda e: e.name == 'geo', ctx.guild.emojis)
        cryo = nextcord.utils.find(lambda e: e.name == 'cryo', ctx.guild.emojis)
        hydro = nextcord.utils.find(lambda e: e.name == 'hydro', ctx.guild.emojis)
        electro = nextcord.utils.find(lambda e: e.name == 'electro', ctx.guild.emojis)
        blank = nextcord.utils.find(lambda e: e.name == 'blank', ctx.guild.emojis)

        
        rendered_text = f"{blank}"

        for element in chara.reactor.applied_elements:
            emote = nextcord.utils.find(lambda e: e.name == element.lower(), ctx.guild.emojis)
            rendered_text += f"{emote}"

        return rendered_text



def setup(pmon):
    pmon.add_cog(GRPG(pmon))


def teardown(pmon):
    pmon.remove_cog("GRPG")
