#!/usr/bin/python3

import requests

def getrequestforuser(config, id):
    user_card_url = config['user']['user_card_url']
    return requests.get(user_card_url.format(USERID=id))

def updateusercount(config):
    currentusercount = int(config['host']['usercount'])
    if len(getrequestforuser(config, currentusercount).text) == 0:
        quit(print('Invalid user number in config file, please reduce the number!'))
    guessstep = 1000
    while guessstep != 0:
        guess = currentusercount + guessstep
        if len(getrequestforuser(config, guess).text) != 0:
            currentusercount = guess
        else:
            guessstep = int(guessstep / 2)
    return currentusercount

if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    usercount = updateusercount(config)
    print(f'Current user count is: {usercount}')
