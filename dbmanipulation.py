
# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import os
import json
import time
import configparser


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

def consentrate_db(config, dbpath="user_database.json", cachepath='.cache/'):
    if not os.path.exists(".cache/dldata.json"):
        print("No new data was found")
        return
    # check if users directory and user_database.json exists along with it's version
    #if not os.path.exists(individual_userdb):
    #    print(f"Folder {individual_userdb} does not exitst, consentrating database is not possible")
    #    return
    
    if os.path.exists(dbpath):
        user_database = json.load(open(dbpath, "r"))
    else:
        user_database = {}
        user_database['db_version'] = 2
    
    try:
        db_version = user_database['db_version']
    except KeyError:
        db_version = 1

    if db_version != 2:
        ans = input("Your json database will be converted to version 2, no data loss will occur, you can press q to cancel")
        if ans == 'q':
            quit("Please back up your json database as old versions of the database are not supported!")
        if db_version == 1:
            user_database = convert_db_version_1_to_2(user_database)

    # update the database and set variables for database
    user_database['last_updated'] = int(time.time())

    hostname = config['host']['hostname']
    if not hostname in user_database:
        user_database[hostname] = {}

    # read files from directory and write them to the database
    newdata = json.load(open(cachepath + "dldata.json"))
    for individual_user in newdata:
        try:
            for object in individual_user:
                user_database[hostname][individual_user['id']][object] = individual_user[object]
        except KeyError:
            user_database[hostname][individual_user['id']] = individual_user

    # write the updated database
    with open(dbpath, "w") as userdb_file:
        json.dump(user_database, userdb_file, indent=4)

    #cleanup the old database
    os.remove(".cache/dldata.json")

if __name__ =='__main__':
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    consentrate_db(config=config)

