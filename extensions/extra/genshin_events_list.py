
import nextcord as discord
from base.events import GenshinEvents
import json
from nextcord.ext import commands, tasks
from core.paimon import Paimon


gevents = GenshinEvents()

def get_event(events, id):
    for event in events:
        if event['id'] == id:
            return event

class GenshinEventsList(commands.Cog):
    def __init__(self, client: Paimon):
        self.client = client

    

    # TODO: Make this a task too.
    # TODO: send a success/failure message acknowledging the command
    @commands.command()
    async def update_event_embeds(self, ctx):
        event_channel = self.client.p_bot_config['events_channel']
        # todo: validate event channel id.
        event_channel = self.client.get_channel(event_channel)

        new_active_events = gevents.get_active_events()


        with open('genshin_event_msgs.json') as f:
            active_event_msgs = json.load(f)
        

        new_active_event_IDs = set(map(lambda event: event['id'],  new_active_events))
        displayed_event_IDs = set(active_event_msgs.keys())

        # the events' embed messages to update.
        for event_id in (new_active_event_IDs & displayed_event_IDs):

            msg_id = active_event_msgs[event_id]
            embed_msg = await event_channel.fetch_message(msg_id)
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


        # the events' embed messages' status to mark as "Already Ended."
        # basically same as above, but you only update the event "status" 

        # currently replacing entire embed, since i don't know how
        # to partially edit an embed.


        # possible solution: @bobyclaws
        # embed_msg = await event_channel.fetch_message(msg_id)
        # embed = embed_msg.embeds[0]
        # status_index = i for i in range(0,len(embed.fields),1) if embed.fields[i]['name'] == 'Status'
        # embed.set_field_at(status_index, name='Status', value ='Event has ended',inline=True)
        # await embed_msg.edit(embed=embed)

        for event_id in (displayed_event_IDs - new_active_event_IDs):
            msg_id = active_event_msgs[event_id]
            embed_msg = await event_channel.fetch_message(msg_id)
            embed = discord.Embed(
                title= "Event Expired.",
                colour=0xb8b6af,
                description="the event has ended")

         
            await embed_msg.edit(embed=embed)

            del active_event_msgs[event_id]

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

            msg = await event_channel.send(embed=embed)
            active_event_msgs[event_id] = msg.id

        with open("genshin_event_msgs.json", 'w') as f:
            json.dump(active_event_msgs,f)




        

def setup(client: Paimon):
    client.add_cog(GenshinEventsList(client))




def teardown(client):
    client.remove_cog(GenshinEventsList(client))

