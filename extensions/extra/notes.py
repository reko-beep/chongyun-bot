
from nextcord.ext import commands
from nextcord import Embed, File
from nextcord.ui import View

from base.guides import GenshinGuides
from base.notes import GuidesNotes
from extensions.views.notes import AllList,NavigatableView, NoteAdd

from core.paimon import Paimon


class Notes(commands.Cog):
    def __init__(self, pmon: Paimon):
        
        self.pmon = pmon
        self.notes_handler = GuidesNotes(pmon)
        self.name = 'Guides Notes'
        self.description = 'Allows member to add notes, so they can add their suggestions to added builds!'


    @commands.command(aliases=['note'],description='Opens an interaction to see the added notes!\nOnly the original creator can delete the note!')
    async def notes(self,ctx):      


        view_object = NavigatableView(ctx.author)

        view_object.add_item(AllList(self.pmon,self.notes_handler,'characters',ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)
    
    @commands.command(aliases=['addn'],description='Opens an interaction to add a note!')
    async def addnotes(self,ctx):        
        view_object = View()
        view_object.add_item(NoteAdd(self.pmon,self.notes_handler,ctx.author))
        await ctx.send('Please select a option from below?',view=view_object)


def setup(bot):
    bot.add_cog(Notes(bot))


def teardown(bot):
    bot.remove_cog("Notes")