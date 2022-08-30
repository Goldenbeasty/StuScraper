#!/usr/bin/python3

# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import configparser
import json
import os

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

host = config['host']['hostname'] + '_'

# Return user data by id
def id_search(uid):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(uid), 'r') as file: # os.path etc. could be taken into a variable
        response = json.loads(file.read())
        file.close()
    return response

# Return all matching user IDs as an array
def username_search(querry, usercount):
    tmp = []

    response = []
    for i in range(usercount):
        i = i + 1
        with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(i),'r') as file:
            tmp.append(json.loads(file.read()))
            file.close()
    for i in range(usercount - 1):
        i = i + 1
        if querry in tmp[i]['name_first'] or querry in tmp[i]['name_last']:
            response.append(tmp[i]['id'])
    return response

def get_user_by_description(config, querry):
    querry = str(querry).lower()
    usercout = int(config['host']['usercount'])
    response = []
    for i in range(usercout):
        for item in id_search(i + 1)['user_type_labels']:
            if str(querry).lower() in str(item).lower():
                response.append(i + 1)
    return response

def main(config):
    usercount = int(config['host']['usercount'])

    list = username_search(str(input('Insert querry: ').capitalize()), usercount=usercount)
    print('\n')

    for user in list:
        descriprion = ''

        userdata = id_search(user)
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
