#!/usr/bin/python3

from distutils.command.config import config
import requests
import configparser
import json
import os
from multiprocessing.pool import ThreadPool
from time import time as timer

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

threadcount = int(config['system']['threadcount'])
host = config['host']['hostname'] + '_'
failedlist = []
prefix = config['user']['prefix']
suffix = config['user']['suffix']

def getuserbyid(id):
    print(id)
    data = requests.get(config['user']['prefix'] + str(id) + config['user']['suffix'])
    data = json.loads(data.text)
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(id), 'w') as file:
        file.write(json.dumps(data))
        file.close()

def downloadbyid(id):
    id = id + 1
    r = requests.get(prefix + str(id) + suffix)
    if r.status_code != 200:
        failedlist.append(id)
    info = json.dumps(json.loads(r.text))
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(id), 'w') as f:
        f.write(info)
        f.close()
    return(id)

def downloaddb():
    start = timer()
    response = ThreadPool(int(config['system']['threadcount'])).imap_unordered(downloadbyid, range(0, int(config['host']['usercount'])))
    for res in response:
        print(res)
    elapsedtime = timer() - start
    print(f"Elapsed Time: {elapsedtime}")
    print(f"With avarage speed of {int(config['host']['usercount']) / elapsedtime}")
    if len(failedlist) != 0:
        print('Failed to get data for: ' + str(failedlist))

if __name__ == '__main__':
    downloaddb()