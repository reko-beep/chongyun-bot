from core.paimon import Paimon
from datetime import datetime,timedelta
import pytz 


class ResetNotifier:
    def __init__(self, pmon: Paimon):
        self.pmon = pmon
        
        

    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60)%60


    def corrected_times(self, correction, time):        
        region_change = pytz.timezone(correction)
        return region_change.localize(time) 



    def get_times(self, date: int):


        
        
        time_region = 'Asia/Shanghai'
        now_utc_ = datetime.now(pytz.timezone('UTC'))
            # Convert to Asia/Kolkata time zone
        region_time = now_utc_.astimezone(pytz.timezone(time_region))


        correction = time_region



        current_day = region_time.day
        current_month = region_time.month
        current_year = region_time.year

        asia_reset_time = self.corrected_times(correction,datetime(current_year,current_month, current_day, 4, 0, 0))
        eu_reset_time = asia_reset_time + timedelta(hours=7)
        na_reset_time = asia_reset_time + timedelta(hours=13)


        asia_reset_time += timedelta(days=date)
        eu_reset_time += timedelta(days=date)
        na_reset_time += timedelta(days=date)


        asia_delta = asia_reset_time - region_time
        eu_delta = eu_reset_time - region_time
        na_delta = na_reset_time - region_time

        days,hrs,mins = self.days_hours_minutes(asia_delta)
        print(asia_reset_time, region_time)
        asia_return = "in {d} days, {h} hrs, {m} mins".format(d=days,h=hrs,m=mins)

        days,hrs,mins = self.days_hours_minutes(eu_delta)
        print(eu_reset_time, region_time)
        eu_return = "in {d} days, {h} hrs, {m} mins".format(d=days,h=hrs,m=mins)

        days,hrs,mins = self.days_hours_minutes(na_delta)
        print(na_reset_time, region_time)
        na_return = "in {d} days, {h} hrs, {m} mins".format(d=days,h=hrs,m=mins)
        if region_time > asia_reset_time:
            asia_return = 'Resetted today!'
        if region_time >eu_reset_time:
            eu_return = 'Resetted today!'
        if region_time > na_reset_time:
            na_return = 'Resetted today!'

        return asia_return, eu_return, na_return
        

    def get_resettimes(self):

        asia, eu, na = self.get_times(0)

        if asia == eu == na == 'Resetted today!':
            asia, eu, na = self.get_times(1)
        
        return asia, eu , na


        
        
