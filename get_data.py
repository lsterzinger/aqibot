def getLatLon(search):
    req = f'https://nominatim.openstreetmap.org/search?q={search}&format=json'
    r = requests.get(req)

    if type(r) is dict:
        locname = r['display_name']
        print('Only one location found: ', locname)
        return locname, r
    
    elif type(r) is list:
        