#TODO: too ugly but not a priority right now

import nextcord
from nextcord.enums import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from nextcord.interactions import Interaction

from .grpg.event import Event
from .grpg.Game import Game
from .grpg.compute import v

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


        self.players['A'] = {'on_chara': 0, 'name': ctx.author.name}
        self.players['B'] = {'on_chara': 0, 'name': ctx.message.mentions[0].name}

        
        # setup game
        game = Game()
        game.pick_domain("Zhou")
        game.domain.add_player("A", "kaeya", "kaeya")
        game.domain.add_player("B", "kaeya", "kaeya")
        game.main_loop().__next__()

        self.game = game

        embed, view = self.render(ctx)




        # send or update message.
        if not self.message:
            self.message = await ctx.send(embed=embed, view=view)
        else:
            await self.message.edit(embed=embed, view=view)



    def render(self, ctx):

        if self.game is None:
            raise Exception('game not init' )


        #SECTION: prepare assets.


        # # health bar emotes
        # hple = nextcord.utils.find(lambda e: e.name == 'left_empty', ctx.guild.emojis)
        # hplf = nextcord.utils.find(lambda e: e.name == 'left_full', ctx.guild.emojis)
        # hpme = nextcord.utils.find(lambda e: e.name == 'middle_empty', ctx.guild.emojis)
        # hpmf = nextcord.utils.find(lambda e: e.name == 'middle_full', ctx.guild.emojis)
        # hpre = nextcord.utils.find(lambda e: e.name == 'right_empty', ctx.guild.emojis)
        # hprf = nextcord.utils.find(lambda e: e.name == 'right_full', ctx.guild.emojis)
        
        # # element emotes
        # pyro = nextcord.utils.find(lambda e: e.name == 'pyro', ctx.guild.emojis)
        # dendro = nextcord.utils.find(lambda e: e.name == 'dendro', ctx.guild.emojis)
        # anemo = nextcord.utils.find(lambda e: e.name == 'anemo', ctx.guild.emojis)
        # geo = nextcord.utils.find(lambda e: e.name == 'geo', ctx.guild.emojis)
        # cryo = nextcord.utils.find(lambda e: e.name == 'cryo', ctx.guild.emojis)
        # hydro = nextcord.utils.find(lambda e: e.name == 'hydro', ctx.guild.emojis)
        # electro = nextcord.utils.find(lambda e: e.name == 'electro', ctx.guild.emojis)
        # blank = nextcord.utils.find(lambda e: e.name == 'blank', ctx.guild.emojis)


        # # chara icons
        # kaeya = nextcord.utils.find(lambda e: e.name == 'kaeya', ctx.guild.emojis)
        # mona = nextcord.utils.find(lambda e: e.name == 'mona', ctx.guild.emojis)

        # embed / game screen
        embed = nextcord.Embed(title=self.game.player)

        

        contentA = ''
        for chara in self.game.domain.players['A']['party']:
            chara_name = f"**{chara}**" if chara.is_onfield() else f"{chara}"
            contentA += f"{chara_name}\n \
                ({chara.get_hp()/v(chara.stats.stats['Max HP'])*100})\
                (st: {chara.current_stamina})\n"

        contentB = ''
        for chara in self.game.domain.players['B']['party']:
            chara_name = f"**{chara}**" if chara.is_onfield() else f"{chara}"
            contentB += f"{chara_name}\n \
                ({chara.get_hp()/v(chara.stats.stats['Max HP'])*100})\
                (st: {chara.current_stamina})\n"


        embed.add_field(name=f"{list(self.players.keys())[0]}'s Party", value=contentA)
        embed.add_field(name=f"{list(self.players.keys())[1]}'s Party", value=contentB)

        # embed.add_field(
        #     name="**Boby's Party**",
        #     value=f"**Kaeya**\n{hplf}{hpmf}{hpmf}{hpmf}{hpmf}{hpme}{hpre}(100%)\n{blank}{dendro}{geo}\n**Mona**\n{hplf}{hpmf}{hpmf}{hpmf}{hpmf}{hpmf}{hpre} (100%)\n{blank}{electro}{pyro}", inline=True)
        
        # embed.add_field(
        #     name="**Bhalu's Party**",
        #     value=f"**Mona**\n{hplf}{hpmf}{hpmf}{hpmf}{hpmf}{hpme}{hpre}(100%)\n{blank}{dendro}{geo}\n**Kaeya**\n{hplf}{hpmf}{hpmf}{hpmf}{hpmf}{hpmf}{hpre}(100%)\n{blank}{electro}{pyro}", inline=True)

        embed.add_field(name='**Commentry**', value="`nothing to see here`", inline=False)

        embed.set_thumbnail(url=ctx.author.avatar.url)


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


        swap = nextcord.ui.Button(
            style=ButtonStyle.blurple,
            label='Swap',
            
        )



           # button handlers

        async def a(i: Interaction):
            
            self.game.events.append(Event(Event.ACTION_AUTO))
            self.game.main_loop().__next__()
            embed, view = self.render(ctx)
            await self.message.edit(embed=embed, view=view)
            pass
        
        async def c(i: Interaction):
            self.game.events.append(Event(Event.ACTION_CHARGE))
            self.game.main_loop().__next__()
            embed, view = self.render(ctx)
            await self.message.edit(embed=embed, view=view)
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
            embed, view = self.render(ctx)
            await self.message.edit(embed=embed, view=view)
            pass


        charge.callback = c
        auto.callback = a
        # skill.callback = e
        # burst.callback = q
        # plunge.callback = p
        swap.callback = s


 
  
        controls_view.add_item(auto)
        controls_view.add_item(charge)
        # controls_view.add_item(plunge)
        # controls_view.add_item(skill)
        # controls_view.add_item(burst)
        controls_view.add_item(swap)

        return embed ,controls_view
        











def setup(pmon):
    pmon.add_cog(GRPG(pmon))


def teardown(pmon):
    pmon.remove_cog("GRPG")
