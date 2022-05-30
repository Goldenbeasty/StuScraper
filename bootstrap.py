import os
import configparser
import requests
import json

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
        print(f"{index}) {school['name']}")
    
    choise = input('Enter the number of the school: ')

    if choise == '':
        choise = 0

    return hits[int(choise)]['client']

if not os.path.exists('./config.ini'):
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
