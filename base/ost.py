from json import load, dump
from os.path import exists
from os import getcwd
from nextcord import Embed

class GenshinOST:
    def __init__(self):
        self.path = f'{getcwd()}/assets/'
        self.albums = {}
        self._load()


    def _load(self):
        if exists(self.path+'albums.json'):
            with open(self.path+'albums.json', 'r') as f:
                self.albums = load(f)
    
    def get_album_names(self):
        return list(self.albums.keys())

    def get_track_names(self, album_name:str):
        return [track['name'] for track in self.albums[album_name]]
    
    def get_track_info(self, album_name:str, track_name:str):

        tracks = self.albums.get(album_name, None)
        if tracks is not None:
            for track in tracks:
                if track_name in track['name']:
                    return track

    def track_embed(self, album_name, track):
        embed = Embed(title=f"Track: {track['name']}", description=f"This soundtrack is played in\n **{track['src']}**",color=0xf5e0d0) 
        embed.add_field(name='Album name', value=album_name.title())
        embed.set_thumbnail(url=track['album_image'])
        return embed