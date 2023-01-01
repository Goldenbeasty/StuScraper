#!/usr/bin/env python3

# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import requests
import configparser
import json
import os
from multiprocessing.pool import ThreadPool
from time import time as timer


failedlist = []
saved_data = []

def downloadbyid(id):
    try:
        id = id + 1
        r = requests.get(config_data['user']['user_card_url'].format(USERID=id))
        if r.status_code != 200:
            failedlist.append(id)
            return f"Failed {id}"
        if save_to_disk != None:
            info = r.json()
            with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + save_to_disk + str(id), 'w') as f:
                json.dump(info,f)
                f.close()

        saved_data.append(r.json())
        return(id)
    except json.JSONDecodeError:
        failedlist.append(id)
    except requests.exceptions.ConnectionError:
        failedlist.append(id)

def downloaddb(config, cachepath=".cache/"):
    global config_data
    config_data = config
    usercount = int(config['host']['usercount'])
    threadcount = int(config['system']['threadcount'])
    
    start = timer()
    try: config["user"]["scraper"] # This is just here as a legacy catch, could probably removed in 3 months or so
    except KeyError:
        config["user"]["scraper"] = "False"

    global save_to_disk
    if config["user"]["scraper"] == "True":
        save_to_disk = config["host"]["hostname"]
    else:
        save_to_disk = None
    
    response = ThreadPool(threadcount).imap_unordered(downloadbyid, range(0,usercount))
    for res in response:
        print(res)
    elapsedtime = timer() - start
    print(f"Elapsed Time: {elapsedtime}")
    print(f"With avarage speed of {int(usercount) / elapsedtime}")
    if len(failedlist) != 0:
        print('Failed to get data for: ' + str(failedlist))
    if not os.path.exists(cachepath):
        os.mkdir(cachepath)
    with open(cachepath + "dldata.json", "w") as f:
        json.dump(saved_data, f)

if __name__ == '__main__':
    config_data = configparser.ConfigParser(interpolation=None)
    config_data.read('config.ini')
    downloaddb(config_data)
