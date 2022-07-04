KQM_TEAMS_IDS = range(1, 50,1)
print(list(KQM_TEAMS_IDS))
import asyncio
from websockets.client import connect
import json


async def get_kqmteams():
    data = {
            'type':'advice',
            'about':'characters',
            'charIDs': list(KQM_TEAMS_IDS),
            'priority':[]
        }
    async def run_s():
        async with connect('wss://www.paimons-teams.nl/ptws') as socket_:

            src = await socket_.send(json.dumps(data))
            data_ = await socket_.recv()
            print(src)
            teams = json.loads(data_)
            print(len(data_))
            print(teams, data_[2])
            with open('kqm_teams.json', 'w') as f:
                json.dump({'teams': teams}, f, indent=1)

def generate_id(string: str):
        seps = ['-','/','\\','.',':',';','|', "'","!","`","~"]
        string = string.strip()
        for s in seps:
            string = string.replace(s, '_',99)
        return string.replace(' ','_',99).lower()

base_ = {
   "title": "",
   "id": "",
   "chars": [
    
   ],
   "description": ""
  }

with open('kqm_teams.json', 'r') as f:
    data_ = json.load(f)['teams'][1]

print(data_)
teams_data = [

]
chars_basekeys = ['leadername', 'char1', 'char2', 'char3']

altkey = '{char}altnames'
name = '{char}name'

for team in data_:
    title = ''
    desc = ''
    chars = []
    if 'teamdesc' in team:
        title = team['teamdesc'] if '\n' not in team['teamdesc'] else team['teamdesc'].split('\n')[0]
        desc = ''if '\n' not in team['teamdesc'] else team['teamdesc'].replace(team['teamdesc'].split('\n')[0]  , '', 1)  
    
    for charkey in chars_basekeys:
        if charkey in team:
            chars.append({ team[charkey]: 'role here'})
        
        if name.format(char=charkey) in team:

            chars.append({team[name.format(char=charkey)]: 'role here'})

        if altkey.format(char=charkey) in team:

            if len(team[altkey.format(char=charkey)]) > 0:
                chars_ = ','.join(team[altkey.format(char=charkey)])
                desc += f'\n{team[name.format(char=charkey)]} can be replaced with {chars_}\n'
      
    exists = [t['title'] for t in teams_data if title.lower() in t['title']]
    if len(exists) >= 1:
        title = title+"-"+str(len(exists))

    teams_data.append({
        'title': title,
        'description': desc+"\n Retrieved from KQM mains",
        'chars': chars,
        'owner': 947245815263555605,
        'file' : '',
        'id': generate_id(title)
    })


with open('kqm_bot.json', 'w') as f:
    json.dump({'teamcomps': teams_data}, f, indent=1)