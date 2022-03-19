#!/usr/bin/python3

import json
from time import sleep
import requests
import urllib.parse
from bs4 import BeautifulSoup
import configparser
from getpass import getpass
import pickle

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
host = config['host']['hostname']
requestssession = requests.Session()

loginmethod = int(input(' 1) Password\n 2) Smart-ID\n 3) ID card\n 4) Existing session\nSelect login method: '))

if loginmethod == 1:
    print('currently not supported')
    username = [str(input('Sisesta nimi: '))]
    username = username[0].split()
    name_first = username[0]
    name_last = username[1]
    password = getpass('Sisesta parool: ')
elif loginmethod == 2:
    username = [str(input('Sisesta nimi: '))]
    username = username[0].split()
    name_first = username[0]
    name_last = username[1]
elif loginmethod == 3:
    print('currently not supported')
elif loginmethod == 4:
    with open('cookiejar', 'rb') as f:
        requestssession.cookies.update(pickle.load(f))
else:
    quit('Choice out of range')
print('')

cookies = {
    'cli-tamme': '220306',
    'bid': '2.820883.33ee5e4400.2f005fc03d',
    '_ga': 'GA1.1.629990194.1642549389',
    '__stclid': '16465759597597d41ca42a6b3ae4d01673932c34',
    '_gid': 'GA1.1.1280619525.1647691284',
}

headers = {
    'Host': 'tamme.ope.ee',
    'Content-Length': '75',
    'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Origin': 'https://tamme.ope.ee',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://tamme.ope.ee/auth/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = {
    'lang': 'et',
}

if loginmethod == 1: #Needs testing, unsure if works
    data = f'data%5BUser%5D%5Busername%5D={name_first}+{name_last}&data%5BUser%5D%5Bpassword%5D={password}'

    response = requestssession.post('https://tamme.ope.ee/auth/', headers=headers, params=params, cookies=cookies, data=data, verify=False)

if loginmethod == 2:
    data = f'data%5BUser%5D%5Busername%5D={name_first}+{name_last}&data%5BUser%5D%5Bpassword%5D='

    first_response = requests.post('https://tamme.ope.ee/auth/smartid', headers=headers, params=params, cookies=cookies, data=data, verify=True)
    first_response = json.loads(first_response.text)
    print(f"Your login code is: {first_response['data']['verification_code']}")    

    params = {
        'smartidsig': first_response['data']['status_url'][26:66],  #subject to being broken five times over
        'lang': 'et',
    }
    data = 'smartid_state=' + urllib.parse.quote(first_response['data']['state'])
    answer = False
    while answer == False:
        response = requestssession.post('https://tamme.ope.ee/auth/smartid/', headers=headers, params=params, cookies=cookies, data=data, verify=True)
        if len(response.text) == 0:
            webpage = requestssession.get('https://tamme.ope.ee')
            answer = True
        sleep(2)

    page = requestssession.get(response.headers['x-redirect'], cookies=cookies)

headers = {
    'Host': 'tamme.ope.ee',
    'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'X-App-Type': 'web',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = {
    'v': '2020',
    'output-format': 'html',
    'comments': '1',
    'comments_metadata': '1',
    'files': '1',
    'attachments': '1',
    'status_404_if_not_found': '1',
    'language': 'et',
    'context': 'single',
    'mark_read': '0',
}

with open('cookiejar', 'wb') as f:
    pickle.dump(requestssession.cookies, f)

def getrawpost(message_id):
    page = requestssession.get(f'https://tamme.ope.ee/suhtlus/api/posts/get/{message_id}', headers=headers, params=params, cookies=cookies, verify=True)
    return page

#godsend
def get_chatpage():
    global chatspage
    chatspage = requestssession.get('https://tamme.ope.ee/suhtlus/api/channels/updates/a/inbox?v=2020&output-format=json&merge_events=0&get_post_membership_data=0&language=et')

def displaymessage(message_id):
    page = getrawpost(message_id)
    parsed_message = BeautifulSoup(page.text, "lxml")
    print(parsed_message.body.find('div', attrs={'class':'post-body formatted-text'}).text)


def choose_message():
    chatdata = json.loads(chatspage.text)
    for i in range(10):
        print(f"{i}) {chatdata['updates'][i]['title']}")
    message_choice = input('\nChoose message: ')
    print('\n')
    if message_choice == 'q': return
    
    message_id = chatdata['updates'][int(message_choice)]['id']
    displaymessage(message_id)
    input()


def open_chats():
    get_chatpage()
    choose_message()
while True:
    print('''
    1) Päevik
    2) Tera
    3) Suhtlus
    4) Klassid
    5) Search user
    ''')
    
    menu_choice = input('Choose menu: ')
    if menu_choice == 'q':
        quit('')
    else:
        menu_choice = int(menu_choice)
    
    if menu_choice == 3:
        open_chats()