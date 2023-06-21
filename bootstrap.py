import os
import configparser
import requests
import json

def licence_agreement(packagebuild):
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
    if packagebuild: return #it being a packagebuild does not mean that it is licenced differently. The licence can still be found at 
    while arg != 'y':
        with open('./LICENCE', 'r') as licencefile:
            print(licencefile.read())
        arg = input("\n\n[y to agree, q to quit]\n")
        if arg == 'q':
            exit()
    input("\n\nIf you wish to scrape data enable it in the menu (under manual database management)")
    return

def save_config_file(config, configpath):
    with open (configpath, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def gethost():
    response = requests.get("https://stuudium.com/_/pweb/get-public-clients") # https://assets.stuudium.net/_/config/clients
    data = json.loads(response.text)

    querry = input('Enter your school: ')
    hits = []

    for school in data:
        if querry in school['search']:
            hits.append(school)

    for index, school in enumerate(hits):
        print(f"{index:>3}) {school['name']:<30}")
    
    choice = input('Enter the number of the school: ')

    if choice == '':
        choice = 0

    return hits[int(choice)]['client']

def main(packagebuild=False):
    if packagebuild:
        configpath = os.path.expanduser("~/.config/stuscraper/config.ini")
    else:
        configpath = "config.ini"
    
    configdir = os.path.dirname(os.path.realpath(os.path.expanduser(configpath)))
    if not os.path.exists(configpath):
        if not os.path.exists(configdir):
            os.mkdir(configdir)
        licence_agreement(packagebuild)
        print('No configuraton file found. Creating one:')
        config = configparser.ConfigParser()
        config['host'] = {}
        config['user'] = {}
        config['system'] = {}
        config['host']['hostname'] = gethost()
        config['host']['usercount'] = '1'
        config['user']['selfid'] = '1'
        config['user']['user_card_url'] = ''
        config['user']['scraper'] = 'False'
        config['system']['threadcount'] = '75'
        save_config_file(config, configpath)

if __name__ == '__main__':
    main()
