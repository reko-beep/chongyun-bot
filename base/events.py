import requests
import time

class GenshinEvents:
    def __init__(self):
        pass


    def get_active_events(self):
        """get only active events."""
        total_active_events = []
        offset = 0
        while True:
            events, next_offset = self.get_events(offset)
            active_events = list(filter(lambda event: event['status'] != "Already Ended.", events))
          
            if len(active_events) == 0: return total_active_events

            total_active_events.extend(active_events)
            offset = next_offset


    def get_events(self, offset=0):
        """
        get an arbitrary number of events from Hoyolab.
        offset represents the offset from which events should be retrieved.
        -> also returns  "next_offset" to continue retieiving subsequent events.

        available fields: id, name, start, end, banner_url, desc, web_path, status
        """

        res = requests.get(
            f"https://api-os-takumi.mihoyo.com/community/community_contribution/wapi/event/list?gids=2&offset={offset}"
        )

        if res.status_code != 200: raise LookupError("failed to fetch events.")
        res_data = res.json()['data']

        events_list = res_data['list']
        next_offset = int(res_data['next_offset'])


        for event in events_list:
            
            # determine event status.
            event_triplet = (event['status'], event['status_ing'], event['status_int'])
            event_status = "Unknown"
            if event_triplet == (3,0,3):
                event_status = "In Progress"
            elif event_triplet == (3,1,3):
                event_status = "Call for Work in Progress"
            elif event_triplet == (3,5,3):
                event_status = "Judging in Progress"
            elif event_triplet == (3,3,3):
                event_status = "Voting in Progress"
            # elif event_triplet == (x,x,x):
            #     event_status = "???"
            else:
                event_status = "Already Ended."


            # determine event type. (can be improved ?)
            type = "??"
            if event['type'] == 1:
                type = "Contest"
            elif event['type'] == 2:
                type = "In Game/Web"

            
            # determine local time from epoch for start and end period
            start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(event['start'])))
            end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(event['end'])))

            del event['status']
            del event['status_ing']
            del event['status_int']
            del event['game_id']
            del event['app_path']

            
            event['status'] = event_status
            event['web_path'] = "https://hoyolab.com" + event["web_path"]
            event['type'] = type
            event['start'] = start
            event['end'] = end
            
        return events_list, next_offset
