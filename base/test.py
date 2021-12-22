import discord
from discord.ext import commands
from discord.flags import Intents

intents = Intents.all()
bot = commands.Bot(command_prefix='?',intents=intents)

async def send_message(discord_id: str):
    member = await bot.fetch_user(int(discord_id))
    try:
        dm = member.dm_channel
        if dm is None:
            await member.create_dm()

        await dm.send('message here')

        print(f'[+] sent message to id {discord_id}')
    except Exception as e:
        print(f'[!] {e}')

bot.run('token here')



##
# import send_message in main script
# keep this script running
#   pass the id to script to whom you want to send message
#
#   it should technicall work
