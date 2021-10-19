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
            status_int, status_ing = event['status_int'], event['status_ing']
            event_status = None
            if(status_int == 2):
                event_status = "Not Yet Started."
            elif(status_int == 4):
                event_status = "Already Ended."
            elif(status_int == 3):
                if (status_ing | 1) == status_ing:
                    event_status = "Call for Works In Progress"
                elif (status_ing | 2) == status_ing:
                    event_status  = "Voting in Progress"
                elif (status_ing | 4) == status_ing:
                    event_status = "Judging in Progress"
                elif (status_ing | 8) == status_ing:
                    event_status = "Publishing in Progress"
                else:
                    event_status = "In Progress"
            else:
                event_status = "Uknown"


            # determine event type. (can be improved ?)
            type = "??"
            if event['type'] == 1:
                type = "Contest"
            elif event['type'] == 2:
                type = "In Game/Web"

            
            # determine local time from epoch for start and end period
            start = time.strftime('%d/%m/%Y', time.localtime(int(event['start'])))
            end = time.strftime('%d/%m/%Y', time.localtime(int(event['end'])))

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
