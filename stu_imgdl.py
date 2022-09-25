
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
from PIL import Image

config_data = configparser.ConfigParser(interpolation=None)
config_data.read('config.ini')
host = config_data['host']['hostname'] + '_'

failedlist = []

def folder_pathcheck(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return

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
    with open(os.path.dirname(os.path.abspath(__file__)) + '/icons/' + host + str(id) + '.jpg', 'wb') as f: # NOTE both jpeg and png files are used as icons for some reson
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

def sort_default_images():
    
    folder_pathcheck("./sorted_images/defaults/")
    folder_pathcheck("./sorted_images/customs/")
    folder_pathcheck("./sorted_images/fails/")

    path_to_images = "./icons/"
    default_colors = [(70,70,70),(255,255,255)]
    for imagepath in os.listdir(path_to_images):
        if os.path.isfile(imagepath):
            try:
                image = Image.open(path_to_images + imagepath)
                pix = image.getpixel((200,200))
                if pix in default_colors:
                    with open("./sorted_images/defaults/" + imagepath, "wb") as outfile:
                        outfile.write(open(path_to_images + imagepath, "rb").read())
                else:
                    if Image.MIME[image.format] == 'image/jpeg':
                        with open("./sorted_images/customs/" + imagepath, "wb") as outfile:
                            outfile.write(open(path_to_images + imagepath, "rb").read())
                    else:
                        with open("./sorted_images/customs/" + imagepath.split(".")[0] + ".png", "wb") as outfile:
                            outfile.write(open(path_to_images + imagepath, "rb").read())
            except OSError:
                with open("./sorted_images/fails/" + imagepath, "wb") as outfile:
                    outfile.write(open(path_to_images + imagepath, "rb").read())


if __name__ == '__main__':
    # downloadicons(config_data)
    sort_default_images()
