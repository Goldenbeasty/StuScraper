#!/usr/bin/python3

import requests
import configparser
import json
import os
from multiprocessing.pool import ThreadPool
from time import time as timer

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

host = config['host']['hostname'] + '_'
failedlist = []
user_card_url = config['user']['user_card_url']

def downloadbyid(id):
    id = id + 1
    r = requests.get(user_card_url.format(USERID=id))
    if r.status_code != 200:
        failedlist.append(id)
    info = json.dumps(json.loads(r.text))
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(id), 'w') as f:
        f.write(info)
        f.close()
    return(id)

def downloaddb(usercount):
    start = timer()
    response = ThreadPool(int(config['system']['threadcount'])).imap_unordered(downloadbyid, range(0, int(usercount)))
    for res in response:
        print(res)
    elapsedtime = timer() - start
    print(f"Elapsed Time: {elapsedtime}")
    print(f"With avarage speed of {int(usercount) / elapsedtime}")
    if len(failedlist) != 0:
        print('Failed to get data for: ' + str(failedlist))

if __name__ == '__main__':
    downloaddb(config['host']['usercount'])