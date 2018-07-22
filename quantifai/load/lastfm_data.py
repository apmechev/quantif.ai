import pylast
import time
import datetime
import apikeys_apmechev as apikeys
import pandas as pd
import pickle
import gzip

API_KEY = apikeys.lastfm['APIKEY']
API_SECRET = apikeys.lastfm['APISECRET']
PASSWORD_HASH = apikeys.lastfm['PASSWORD_HASH']

username = "apmechev"
password_hash = PASSWORD_HASH

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
me = pylast.AuthenticatedUser(network)


e=time.mktime(datetime.datetime.strptime("001/2012", "%j/%Y").timetuple())
#lastfm_data={}

lastfm_data=pickle.load(gzip.open('/home/apmechev/quantifai.me/raw_data/last.fm/lastfm_data.pklz','r'))

today =  datetime.datetime.now().timetuple().tm_yday


#for year in range(2018,2019):
#    time.sleep(0.1)
#    for day in range(today -14 ,today, 1):

now = datetime.datetime.now()
year = now.year
day = datetime.datetime.now().timetuple().tm_yday
for year in range(year, year+1):
    time.sleep(0.1)
    for day in range(day ,day -  23, -1):
        s=e
        e=time.mktime(datetime.datetime.strptime("%03d/%s" % (day,year), "%j/%Y").timetuple())
        t1=me.get_recent_tracks( limit=100, cacheable=True, time_from=s, time_to=e)
        time.sleep(0.1)
        print("Year:%s Day:%s" % (year,day))
        day_data={}
        for track in t1:
            ts=track.timestamp
            date=datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
            date_time=datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
            day_data[date_time]={'timestamp':int(ts), "Time":date_time, 'artist':track[0].artist.name, 'track':track[0].title, 'album':track.album}
        if len(day_data.keys())>1:
            lastfm_data[date]=pd.DataFrame(day_data)


pickle.dump(lastfm_data,gzip.open('/home/apmechev/quantifai.me/raw_data/last.fm/lastfm_data.pklz','w'))


