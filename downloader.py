import requests
import datetime as dt
import json
import time

# since = 1676485257 # Wednesday, February 15, 2023 
since = 1514765454 # Monday, January 1, 2018 
until = 1678920199 # Wednesday, March 15, 2023
d30 = 2592000 # 30 days worth of time in timestamp

def saveJson(data, name): # will save to this file location
    with open(name, 'w') as f:
        json.dump(data, f)

def get_req(since, until, subreddit = 'ambien'):
  start = time.time()
  dataset='reddit'
  kind = "submission"
  endpoint = '{dataset}/{kind}/search'.format(dataset=dataset, kind=kind)
  url = 'https://api.pushshift.io/{endpoint}'.format(endpoint=endpoint)
  params = {'subreddit': subreddit, 
            'size': 1000,  # this is the limit allowed (1000)
            'metadata': True,
            'track_total_hits': True, 
            'sort': 'created_utc', 
            'order': 'desc', 
            'until': until, #Wednesday, March 15, 2023 10:43:19 PM
            'since': since
            # 'since': 1671056402 #Wednesday, December 14, 2022 10:20:02 PM
            # 'since': 1638120199 2592000
          }    
  res = requests.get(url, params=params) # download the data accourding to params
  print("time get took:", time.time()-start)
  return json.loads(res.text)

starttime = time.time()
start = since
end = since+d30
count = 0
dataBlock = []
while end<until:
    s = time.time()
    data = get_req(start, end) #returns json
    # saveJson(data['data'], f"data/test{count}.json") #save data into file
    dataBlock += data["data"]
    start = end+1
    end = end+d30 if end+d30<until else until
    count += 1
    print("time took:",time.time()-s)

saveJson(dataBlock, "data/block.json")

# postNum = data['metadata']['es']['hits']['total']['value'] # this seems to be the number of items in a timeframe

saveJson(data['data'], "data/test.json") #save data into file
# print(data)
print(data['data'][0].keys())
print(len(data['data']))
print(data['metadata'])
print(data['metadata']['es']['hits']['total']['value']) 
print("time:",time.time()-starttime)