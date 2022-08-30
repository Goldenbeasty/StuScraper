#!/usr/bin/python3

# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

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
