
from datetime import datetime,timedelta
import pytz 
import calendar
 

        

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60



def get_times(date: int, hr_in_24: int):


    
    
    region_time = datetime.now()
    
    current_day = region_time.day
    current_month = region_time.month
    current_year = region_time.year

    comm_reset_time_in_region = datetime(current_year, current_month, current_day , hr_in_24, 0 ,0)




    asia_reset_time = comm_reset_time_in_region
    eu_reset_time = asia_reset_time + timedelta(hours=7)
    na_reset_time = asia_reset_time + timedelta(hours=13)

    asia_reset_time += timedelta(days=date)
    eu_reset_time += timedelta(days=date)
    na_reset_time += timedelta(days=date)  

    return {'asia': asia_reset_time, 'eu': eu_reset_time,'na': na_reset_time}


def get_remaining_time(date: int, hr_in_24: int):

    region_time = datetime.now()
    
    current_day = region_time.day
    current_month = region_time.month
    current_year = region_time.year

    comm_reset_time_in_region = datetime(current_year, current_month, current_day , hr_in_24, 0 ,0)




    asia_reset_time = comm_reset_time_in_region
    eu_reset_time = asia_reset_time + timedelta(hours=7)
    na_reset_time = asia_reset_time + timedelta(hours=13)

    asia_reset_time += timedelta(days=date)
    eu_reset_time += timedelta(days=date)
    na_reset_time += timedelta(days=date)  


    asia_delta = asia_reset_time - region_time
    eu_delta = eu_reset_time - region_time
    na_delta = na_reset_time - region_time
    if region_time > asia_reset_time:
        asia_delta = None
    if region_time > eu_reset_time:
        eu_delta =  None
    if region_time > na_reset_time:
        na_delta =  None

    return {'asia': asia_delta, 'eu': eu_delta, 'na': na_delta}

def get_in_str(return_delta: timedelta):
    days,hrs,mins = days_hours_minutes(return_delta)
    return "in {d} days, {h} hrs, {m} mins".format(d=days,h=hrs,m=mins)


def get_resettimes(hrin24forReset: int, region: str, all:bool=False):
    dict_ = get_times(0, hrin24forReset)

    check_remaining_time = get_remaining_time(0, hrin24forReset)
    if check_remaining_time.get(region) == None and region != '':
        dict_ = get_times(1, hrin24forReset)
    if all:
        for reg in check_remaining_time:
            if check_remaining_time[reg] == None:
                dict_[reg] = get_times(1, hrin24forReset).get(reg)
        return dict_
    return dict_.get(region)


    