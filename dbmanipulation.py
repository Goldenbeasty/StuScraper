
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

def convert_db_version_1_to_2(database):
    new_db = {}
    new_db['db_version'] = 2
    for object in database:
        if object == 'last_updated':
            new_db[object] = object
        elif type(database[object]) == list:
            new_db[object] = {}
            for element in database[object]:
                new_db[object][element['id']] = element
    return new_db

def consentrate_db(config):
    individual_userdb = "./users/"

    if not os.path.exists(individual_userdb):
        print(f"Folder {individual_userdb} does not exitst, consentrating database is not possible")
        return
    
    if os.path.exists("user_database.json"):
        user_database = json.load(open("user_database.json", "r"))
    else:
        user_database = {}
        user_database['db_version'] = 2
    
    try:
        db_version = user_database['db_version']
    except KeyError:
        db_version = 1
        ans = input("Your json database will be converted to version 2, no data loss will occur, you can press q to cancel")
        if ans == 'q':
            quit("Please back up your json database as old versions of the database are not supported!")
        user_database = convert_db_version_1_to_2(user_database)

    user_database['last_updated'] = int(time.time())

    hostname = config['host']['hostname']
    if not hostname in user_database:
        user_database[hostname] = {}

    for file in os.listdir(individual_userdb):
        if hostname in file:
            individual_user = json.load(open(individual_userdb + file))
            try:
                for object in individual_user:
                    user_database[hostname][individual_user['id']][object] = individual_user[object]
            except KeyError:
                user_database[hostname][individual_user['id']] = individual_user

    with open("user_database.json", "w") as userdb_file:
        json.dump(user_database, userdb_file, indent=4)

if __name__ =='__main__':
    consentrate_db(config=config)