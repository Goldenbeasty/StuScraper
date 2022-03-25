#!/usr/bin/python3

import configparser
import json
import os

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

usercount = int(config['host']['usercount'])
host = config['host']['hostname'] + '_'

# Return user data by id
def id_search(uid):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(uid), 'r') as file: # os.path etc. could be taken into a variable
        response = json.loads(file.read())
        file.close()
    return response

# Return all matching user IDs as an array
def username_search(querry):
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

def main():
    list = username_search(str(input('Insert querry: ').capitalize()))
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

def main_legacy():
    list = username_search(str(input('Insert querry: ').capitalize()))
    print('\n')

    for user in list:
        userdata = id_search(user)
        descriprion = ''
        try:
            if userdata['types'][0] == 'student':
                user_proffesion =  str(userdata['user_type_labels'][0])
            elif userdata['types'][0] != 'student':
                if len(userdata['types']) == 1:
                    user_proffesion = userdata['types'][0]
                elif len (userdata['types']) == 2:
                    user_proffesion = userdata['types'][0] + ', ' + userdata['types'][1]
                elif len (userdata['types']) == 3:
                    user_proffesion = userdata['types'][0] + ', ' + userdata['types'][1] + ', ' + userdata['types'][2]
            else:
                user_proffesion = userdata['types']
        except IndexError:
            user_proffesion = userdata['types']
        if userdata['description'] != None:
            descriprion = ', ' + userdata['description']
        print(userdata['id'] + ' ' + userdata['name_first'] + ' ' + userdata['name_last'] + '              ' + str(user_proffesion) + descriprion)

    print('\nTotal of ' + str(len(list)) + ' results')

if __name__ == '__main__':
    main()
