import requests
import os
import json

comic_url = "http://importmarvel.com/api/series"
comic_results = requests.get(comic_url).json()['data']['results']

results = {}
for v in comic_results:
	year = v['startYear']
	if year in results:
		results[year].append(v['comics']['items'][0]['name'])
	else:
		results[year] = [v['comics']['items'][0]['name']]

with open('series_data.json', 'w') as outfile:
	json.dump(results, outfile)

print (results)