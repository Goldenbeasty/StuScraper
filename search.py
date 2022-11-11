#!/usr/bin/env python3

# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import configparser
import json

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

host = config['host']['hostname'] + '_'

# Return user data by id
def id_search(uid:int, data, config=config):
    return data[config['host']['hostname']][str(uid)]

# Return all matching user IDs as an array in a asssending order
def username_search(query, config=config):
    response = []
    data = json.load(open('user_database.json', 'r'))

    for uid in data[config['host']['hostname']]:
        userdata = data[config['host']['hostname']][uid]
        if query.lower() in userdata['name_first'].lower() + ' ' + userdata['name_last'].lower():
            response.append(int(uid))
    response.sort()
    return response

def get_user_by_description(config, query):
    data = json.load(open('./user_database.json', 'r'))
    query = str(query).lower()
    usercout = int(config['host']['usercount'])
    response = []
    for i in range(usercout):
        for item in id_search(i + 1, data=data, config=config)['user_type_labels']:
            if str(query).lower() in str(item).lower():
                response.append(i + 1)
    return response

def list_users(config, list_of_users):
    data = json.load(open('./user_database.json', 'r'))
    for user in list_of_users:
        descriprion = ''

        userdata = id_search(user, data=data, config=config)
        names = f'{userdata["name_first"]} {userdata["name_last"]}'

        if userdata['user_type_labels'] != None:
            for i in range(len(userdata['user_type_labels'])):
                descriprion += ' ' + userdata['user_type_labels'][i]
                # if i is not the last element add a comma
                if i != len(userdata['user_type_labels']) - 1:
                    descriprion += ','

        #print user id, names and description with uniform spacing in a form of a table
        print(f'{userdata["id"]:<6} {names:<30} {descriprion:<20}')

def main(config):
    list = username_search(str(input('Insert query: ')), config=config)
    print('\n')
    data = json.load(open('./user_database.json', 'r'))

    for user in list:
        descriprion = ''

        userdata = id_search(user, data=data, config=config)
        names = f'{userdata["name_first"]} {userdata["name_last"]}'

        if userdata['user_type_labels'] != None:
            for i in range(len(userdata['user_type_labels'])):
                descriprion += ' ' + userdata['user_type_labels'][i]
                # if i is not the last element add a comma
                if i != len(userdata['user_type_labels']) - 1:
                    descriprion += ','

        #print user id, names and description with uniform spacing in a form of a table
        print(f'{userdata["id"]:<6} {names:<30} {descriprion:<20}')

if __name__ == '__main__':
    main(config)
