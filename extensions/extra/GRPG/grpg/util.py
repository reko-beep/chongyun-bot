
def interpolate_stat(stats_table, level):
    """calculates the stats for intermediate levels not listed in table"""
    stat = stats_table.get(level)
    
    if not stat:
        # find the lower and higher levels that the given level is between.
        low = high = 1      
        for lvl in stats_table.keys():
            if level > lvl:
                low = lvl
            else:
                high = lvl
                break

        step = (stats_table[high] - stats_table[low]) / (high - low)
        stat = stats_table[low] + (step * (level - low))

    return stat

def get_opponent(party_name):
    return 'B' if party_name == 'A' else 'A'