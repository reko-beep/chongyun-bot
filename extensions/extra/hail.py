import nextcord
import shutil
from nextcord.ext import commands
import requests
import subprocess
import platform
from util.logging import logc


class Hail(commands.Cog):
    def __init__(self, pmon):
        self.pmon = pmon

    
    @commands.command()
    async def hail(self, ctx):
        user = ctx.message.mentions[0]
        if user:
            url = user.avatar.url[:-13] + "png?size=256"
            res = requests.get(url)
            with open('assets/Hail/input.png', 'wb') as f:
                f.write(res.content)
            
            logc("url: ", url)

            shutil.copyfile('assets/Hail/input.png', 'bin/hailgen/assets/input.png')
            if platform.system() == "Windows":
                subprocess.call(
                    "hailgen.exe",
                    cwd="bin/hailgen/",
                    shell=True)
            elif platform.system() == "Linux":
                subprocess.call(
                    "export LD_LIBRARY_PATH=./lib && xvfb-run ./hailgen",
                    cwd="bin/hailgen/",
                    shell=True)

            subprocess.call(
                "echo y | ffmpeg -y -hide_banner -loglevel error -f image2 -framerate 20 -i assets/out/frame%d.png assets/out/output.gif",
                cwd="bin/hailgen/",
                shell=True)
            shutil.copyfile('bin/hailgen/assets/out/output.gif', 'assets/Hail/output.gif')
            await ctx.send(file=nextcord.File(r'assets/Hail/output.gif'))

def setup(client):
    client.add_cog(Hail(client))


def teardown(client):
    client.remove_cog("Hail")
