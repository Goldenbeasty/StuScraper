#!/usr/bin/python3

import configparser
import json
import os

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

usercount = int(config['host']['usercount'])
host = config['host']['hostname'] + '_'

def id_search(uid):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/users/' + host + str(uid), 'r') as file: # os.path etc. could be taken into a variable
        response = json.loads(file.read())
        file.close()
    return response

def username_search(querry): # Returns all matching user id as an array
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
