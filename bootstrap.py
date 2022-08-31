
# This file is part of StuScraper.

# StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with StuScraper. If not, see <https://www.gnu.org/licenses/>. 

import os
import configparser
import requests
import json

def licence_agreement():
    arg = None
    while arg != '':
        os.system('clear')
        arg = input("""
StuScraper is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

StuScraper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

[Enter to continue, q to quit]
""")
        if arg == 'q':
            exit()

    os.system('clear')
    arg = None
    while arg != 'y':
        with open('./LICENCE', 'r') as licencefile:
            print(licencefile.read())
        arg = input("\n\n[y to agree, q to quit]\n")
        if arg == 'q':
            exit()
    return

def save_config_file(config):
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()

def gethost():
    response = requests.get('https://assets.stuudium.net/_/config/clients')
    data = json.loads(response.text)
    schools = []

    querry = input('Enter your school: ')
    hits = []

    for school in data:
        if querry in school['search']:
            hits.append(school)

    for index, school in enumerate(hits):
        print(f"{index:>3}) {school['name']:<30}")
    
    choise = input('Enter the number of the school: ')

    if choise == '':
        choise = 0

    return hits[int(choise)]['client']

def main():
    if not os.path.exists('./config.ini'):
        licence_agreement()
        print('No configuraton file found. Creating one:')
        config = configparser.ConfigParser()
        config['host'] = {}
        config['user'] = {}
        config['system'] = {}
        config['host']['hostname'] = gethost()
        config['host']['usercount'] = '1'
        config['user']['selfid'] = '1'
        config['user']['user_card_url'] = ''
        config['system']['threadcount'] = '75'
        save_config_file(config)

if __name__ == '__main__':
    main()