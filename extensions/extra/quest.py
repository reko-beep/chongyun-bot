from nextcord import Embed, Member, File
from nextcord.ext import commands

from extensions.views.quests import AllView, QuestView

from core.paimon import Paimon
import nextcord as discord

from asyncio import sleep
from util.logging import logc

from os import getcwd
from base.quest_rewrite import GenshinQuests

quest_handler = GenshinQuests()

class QuestsWalkthrough(commands.Cog):
    def __init__(self, pmon: Paimon):
        self.pmon = pmon

    @commands.command(aliases=['q','quest'])
    async def quests(self, ctx, *,quest_name: str=''):
        #testing
        quest_ = ''.join(quest_name)
        result,search_type = quest_handler.search(quest_name.lower(),'quests',True)

        not_found = (len(result) != 1 and len(result) > 0)

        if not_found:
            type_ = quest_handler.get_type(quest_)
            main_heading = f'{quest_} | {type_}'
            embeds = quest_handler.create_embed_search_pages(result, main_heading, search_type, ctx.author, 10)
            view = AllView(ctx,embeds)
            await ctx.send(f'You searched for {quest_.title()}',embed=embeds[0],view=view)
        
        else:
            if len(result) != 0:
                embeds = quest_handler.create_quest_embeds(ctx.author,result[0])
                view = QuestView(ctx,embeds)
                await ctx.send(f'You searched for {quest_.title()}',embed=embeds[list(embeds.keys())[0]],view=view)
            else:
                embed = Embed(title='Error',
                            description='Could not find anything!'
                            ,color=0xf5e0d0)
                embed.set_author(name=ctx.author.display_name,
                                icon_url=ctx.author.avatar.url)

                await ctx.send(f'You searched for {quest_.title()}',embed=embed)


    @commands.command(aliases=['act'])
    async def acts(self, ctx, *,act_name: str=''):
        #testing
        act_ = ''.join(act_name)
        
        if act_ == "":
            result,search_type = quest_handler.search('','acts',True)
            act_title = act_.title()
        else:
            result,search_type = quest_handler.search(act_,'quests',True)
            act_title = quest_handler.get_original_name(act_,'act')


        not_found = (len(result) > 0)

        if not_found:
            if act_title == '':
                act_title = quest_handler.get_original_name(act_,'act')
            type_ = quest_handler.get_type(act_)
            main_heading = f'{act_title} | {type_}'
            embeds = quest_handler.create_embed_search_pages(result,main_heading,search_type,ctx.author,10)
            view = AllView(ctx,embeds)
            await ctx.send(f'You searched for {act_title}',embed=embeds[0],view=view)

        else:

    
            embed = Embed(title='Error',
                            description='Could not find anything!'
                            ,color=0xf5e0d0)
            embed.set_author(name=ctx.author.display_name,
                            icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        

    @commands.command(aliases=['chapter','chap'])
    async def chapters(self, ctx, *,chapter_name: str=''):
        #testing
        chapter_ = ''.join(chapter_name)
        chapter_title = ''
        if chapter_ == '':
            result,search_type = quest_handler.search('','chapters',True)
            chapter_title = chapter_.title()
        else:
            result,search_type = quest_handler.search(chapter_,'acts',True)
            

        not_found = (len(result) > 0)
        if not_found:
            if chapter_title == '':
                chapter_title = quest_handler.get_original_name(chapter_,'chapter')
            type_ = quest_handler.get_type(chapter_)
            main_heading = f'{chapter_title} | {type_}'
            embeds = quest_handler.create_embed_search_pages(result,main_heading,search_type,ctx.author,10)
            view = AllView(ctx,embeds)
            await ctx.send(f'You searched for {chapter_title}',embed=embeds[0],view=view)
        
        else:
            if chapter_title == '':
                chapter_title = quest_handler.get_name(chapter_,'chapter')

            embed = Embed(title='Error',
                            description='Could not find anything or Either the chapter had no acts!'
                            ,color=0xf5e0d0)
            embed.set_author(name=ctx.author.display_name,
                            icon_url=ctx.author.avatar.url)

            await ctx.send(f'You searched for {chapter_title}',embed=embed)

def setup(bot):    
    bot.add_cog(QuestsWalkthrough(bot))


def teardown(bot):
    bot.remove_cog("QuestsWalkthrough")