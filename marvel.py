import requests
import json
import itertools
from tomorrow import threads

@threads(7)
def get(offset):
    data = json.loads(
        requests.get('http://importmarvel.com/api/series?offset=' + str(offset)).text
    )
    data = data['data']['results']
    res = map(condense, data)
    return res

def condense(e):
    res = {}
    res['title'] = e['title']
    res['startYear'] = e['startYear']
    return res

def call_marvel():
    result = list([get(i) for i in range(0,1500,200)])
    return itertools.chain(*result)

