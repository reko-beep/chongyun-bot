def get_server_region(**kwargs):
        from_uid = kwargs.get("uid", -1)
        region_str = kwargs.get("region", '').lower()
        print('region provided', region_str)
        if from_uid != -1:
            uid = from_uid
            if type(from_uid) == int:
                uid = str(from_uid)
            
            if uid[0] == '8':
                return 'asia'
            if uid[0] == '7':
                return 'eu'
            if uid[0] == '6':
                return 'na'
           
        if region_str != '':
            allowed :list = ['','asia','as','eu','europe','na','northamerica']
            
            try:
                index = allowed.index(region_str)
                print('index found', index)
            except ValueError:                
                pass
            else:      
                print(index % 2)        
                if index % 2 == 0:                    
                    return allowed[index-1]
                else:
                    return allowed[index]

str_ = 'Asia Carry'.lower().replace("carry", '', 99)
print(str_)
test = get_server_region(region='asia')

print(test)