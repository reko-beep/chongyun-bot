
import nextcord as discord
from base.events import GenshinEvents
import json
from nextcord.ext import commands, tasks
from nextcord import TextChannel
from core.paimon import Paimon
from util.logging import logc


gevents = GenshinEvents()

def get_event(events, id):
    for event in events:
        if event['id'] == id:
            return event

class GenshinEventsList(commands.Cog):
    def __init__(self, client: Paimon):
        self.client = client
        self.name = 'Events'
        self.description = 'Module to send the events ongoing or passed in game!'
        self.event_channel : TextChannel = None
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            if self.event_channel is None:
                self.event_channel = self.client.get_channel(self.client.p_bot_config['events_channel'])
                self.update_event_embeds.start()

    # TODO: Make this a task too.
    # TODO: send a success/failure message acknowledging the command
    @tasks.loop(hours=24)
    async def update_event_embeds(self):
        # todo: validate event channel id.
        
        if self.event_channel is not None:
            new_active_events = gevents.get_active_events()


            with open('genshin_event_msgs.json') as f:
                active_event_msgs = json.load(f)
            

            new_active_event_IDs = set(map(lambda event: event['id'],  new_active_events))
            displayed_event_IDs = set(active_event_msgs.keys())

            logc("found", len(new_active_event_IDs), " active events.")

            # the events' embed messages to update.
            for event_id in (new_active_event_IDs & displayed_event_IDs):

                msg_id = active_event_msgs[event_id]
                embed_msg = await self.event_channel.fetch_message(msg_id)
                event = get_event(new_active_events, event_id)
                embed = discord.Embed(
                    title= event['name'],
                    colour=0xb8b6af,
                    url=event['web_path'],
                    description=event['desc'])

                embed.set_image(url=event['banner_url'])

                embed.add_field(name="Type", value=event['type'], inline=True)
                embed.add_field(name="Status", value=event['status'], inline=True)
                embed.add_field(name="Start", value=event['start'], inline=True)
                embed.add_field(name="End", value=event['end'], inline=True)
                await embed_msg.edit(embed=embed)
                logc("updated event msg:", msg_id)

            # the events' embed messages' status to mark as "Already Ended."
            # basically same as above, but you only update the event "status" 
            for event_id in (displayed_event_IDs - new_active_event_IDs):
                msg_id = active_event_msgs[event_id]
                embed_msg = await self.event_channel.fetch_message(msg_id)
                embed = embed_msg.embeds[0]
                for i in range(len(embed.fields)):
                    if embed.fields[i].name == 'Status':
                        embed.set_field_at(i,
                            name='Status',
                            value='Already Ended.',
                            inline=True)

                await embed_msg.edit(embed=embed)
                del active_event_msgs[event_id]
                logc("event message marked as no longer active:", msg_id)

            # create new embeds for undisplayed events.
            undisplayed_events = new_active_event_IDs - displayed_event_IDs
            for event_id in undisplayed_events:
                event = get_event(new_active_events, event_id)

                embed = discord.Embed(
                    title= event['name'],
                    colour=0xb8b6af,
                    url=event['web_path'],
                    description=event['desc'])

                embed.set_image(url=event['banner_url'])

                embed.add_field(name="Type", value=event['type'], inline=True)
                embed.add_field(name="Status", value=event['status'], inline=True)
                embed.add_field(name="Start", value=event['start'], inline=True)
                embed.add_field(name="End", value=event['end'], inline=True)

                msg = await self.event_channel.send(embed=embed)
                active_event_msgs[event_id] = msg.id
                logc("added new event msg:", msg.id)

            with open("genshin_event_msgs.json", 'w') as f:
                json.dump(active_event_msgs,f)




        

def setup(client: Paimon):
    client.add_cog(GenshinEventsList(client))




def teardown(client):
    client.remove_cog("GenshinEventsList")

