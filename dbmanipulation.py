
# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import os
import json
import time
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
host = config['host']['hostname']

def consentrate_db(config):
    individual_userdb = "./users/"

    if not os.path.exists(individual_userdb):
        print(f"Folder {individual_userdb} does not exitst, consentrating database is not possible")
        return
    
    if os.path.exists("user_database.json"):
        user_database = json.load(open("user_database.json", "r"))
    else:
        user_database = {}
    
    user_database['last_updated'] = int(time.time())

    hostname = config['host']['hostname']
    if not hostname in user_database:
        user_database[hostname] = []

    for file in os.listdir(individual_userdb):
        if hostname in file:
            individual_user = json.load(open(individual_userdb + file))
            user_exists = False
            for db_user in user_database[hostname]:
                if individual_user['id'] == db_user['id']:
                    user_exists = True
                    db_user = individual_user
                    break
            if user_exists == False:
                user_database[hostname].append(individual_user)

    with open("user_database.json", "w") as userdb_file:
        json.dump(user_database, userdb_file, indent=4)

if __name__ =='__main__':
    consentrate_db(config=config)