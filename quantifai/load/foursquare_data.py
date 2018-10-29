# Before running this script execut the following command:
# $ pip install requests
# To run this script execute:
# $ python export_foursquare_checkins.py
import requests
import json
import datetime
import time
import pickle
import gzip
import pdb
import apikeys

url_template = 'https://api.foursquare.com/v2/users/self/checkins?limit=250&oauth_token={}&v=20131026&offset={}'
headers={'User-Agent': 'My User Agent 1.0',}
# If you navigate to https://developer.foursquare.com/docs/explore, Foursquare
# will generate an OAuth token for you automatically. Copy and paste that token
# below.

oauth_token = apikeys.foursquare['oauth_token']
offset = 0
data = []

def return_venue_field(item,field):
    if 'venue' in item.keys():
        if type(item['venue'])==dict: 
            if field in item['venue'].keys():
                return item['venue'].get(field)
    else:
        return None

def return_location_field(item,field):
    location=return_venue_field(item,'location')
    if location:
        return item['venue']['location'].get(field)

def return_category(item):
    categories=return_venue_field(item,'categories')
    if categories:
        return item.get('venue').get('categories')[0].get('name')
    return None


## This will save your foursquare_checkins to a file in the same directory as
#  this script.
#with open("/home/apmechev/quantifai.me/raw_data/foursquare/foursquare_checkins.json", 'w') as f:
#    while True:
#        response = requests.get(url_template.format(oauth_token, offset))
#        if len(response.json()['response']['checkins']['items']) == 0:
#            break
#
#        data.append(response.json())
#        offset += 250
#
#    f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

def main():
	response = requests.get(url_template.format(oauth_token, offset), headers=headers)
	data=[]
	if response.ok:
		data.append(response.json())
	else:
		 response.raise_for_status
	
#	data=json.load(open("/home/apmechev/quantifai.me/raw_data/foursquare/foursquare_checkins.json", 'r'))
	
	foursq_data=pickle.load(gzip.open('/home/apmechev/quantifai.me/raw_data/foursquare/foursq_data.pklz','r'))
	for chunk in data:
	    for item in chunk['response']['checkins']['items']:
	        d={'timestamp': item.get('createdAt'), 
	                'venue': return_venue_field(item,'name'), 
	                'category': return_category(item),
	                '4sq_venue_id': return_venue_field(item,'id'), #item.get('venue').get('id'), 
	                'city': return_location_field(item,'city'), #item.get('venue').get('location').get('city'), 
	                'state': return_location_field(item,'state'), #item['venue']['location'].get('state'), 
	                'country': return_location_field(item,'country'), #item['venue']['location'].get('country'),
	                'country_code': return_location_field(item,'cc'), #item['venue']['location'].get('cc'), 
	                'postal_code': return_location_field(item,'postalCode'),# item['venue']['location'].get('postalCode'), 
	                'lat': return_location_field(item,'lat'), #etem['venue']['location']['lat'], 
	                'lng': return_location_field(item,'lng')} #item['venue']['location']['lng']}
	        ts=item['createdAt']+60*item['timeZoneOffset']
	        date=datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
	        date_time=datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
	        if date not in foursq_data.keys():
	            foursq_data[date]={}
	        foursq_data[date][date_time]=d
	
	
	pickle.dump(foursq_data,gzip.open('/home/apmechev/quantifai.me/raw_data/foursquare/foursq_data.pklz','w'))

def get_last_city():
	response = requests.get(url_template.format(oauth_token, offset))
	if response.ok:
        	data = response.json()
	else:
         	response.raise_for_status()
	return(data['response']['checkins']['items'][0]['venue']['location']['city'])


if __name__ == '__main__':
	main()
