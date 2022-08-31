
# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import requests
import configparser
import os
import json
from multiprocessing.pool import ThreadPool
from time import time as timer

config_data = configparser.ConfigParser(interpolation=None)
config_data.read('config.ini')
host = config_data['host']['hostname'] + '_'

failedlist = []

def getfile(config, uid):
    host = config['host']['hostname'] + '_'
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(uid), 'r') as f:
        info = json.loads(f.read())
        f.close()
    return(info)

def download_image_and_save(indata):
    id, link = indata
    r = requests.get(link)
    if r.status_code != 200:
        failedlist.append(link)
    with open(os.path.dirname(os.path.abspath(__file__)) + '/icons/' + host + str(id) + '.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    return(id)

def downloadicons(config):
    if not os.path.isdir('./icons'):
        os.mkdir('./icons')

    threadcount = int(config['system']['threadcount'])
    usrcount = config['host']['usercount']
    list_of_links = []
    for user in range(int(usrcount)):
        try:
            user = user + 1
            userdata = getfile(config, user)
            link = userdata['avatar']['max']
            list_of_links.append([user, link])
        except KeyError:
            continue

    starttime = timer()
    response = ThreadPool(threadcount).imap_unordered(download_image_and_save, list_of_links)
    for res in response:
        print(res)
    elapsedtime = timer() - starttime
    print(f"Elapsed Time: {elapsedtime}")
    print(f"With avarage speed of {int(usrcount) / elapsedtime}")
    if len(failedlist) != 0:
        print('Failed: ' + str(len(failedlist)))
        for failed in failedlist:
            print(failed)

if __name__ == '__main__':
    downloadicons(config_data)
