#!/usr/bin/python3

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
