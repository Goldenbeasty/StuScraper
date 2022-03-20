#!/usr/bin/python3

import configparser
import requests

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

user_card_url = config['user']['user_card_url']

def getrequestforuser(id):
    return requests.get(user_card_url.format(USERID=id))

def updateusercount():
    currentusercount = int(config['host']['usercount'])
    if len(getrequestforuser(currentusercount).text) == 0:
        quit(print('Invalid user number in config file, please reduce the number!'))
    guessstep = 1000
    while guessstep != 0:
        guess = currentusercount + guessstep
        if len(getrequestforuser(guess).text) != 0:
            currentusercount = guess
        else:
            guessstep = int(guessstep / 2)
    return currentusercount

if __name__ == '__main__':
    usercount = updateusercount()
    print(f'Current user count is: {usercount}')
