#!/usr/bin/python3

import json
from time import sleep
import requests
import urllib.parse
from bs4 import BeautifulSoup
import configparser
from getpass import getpass
import pickle
import os

import request
import search
import usercounter

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
    f'cli-{host}': '220306',
    'bid': '2.820883.33ee5e4400.2f005fc03d',
    '_ga': 'GA1.1.629990194.1642549389',
    '__stclid': '16465759597597d41ca42a6b3ae4d01673932c34',
    '_gid': 'GA1.1.1280619525.1647691284',
}

headers = {
    'Host': f'{host}.ope.ee',
    'Content-Length': '75',
    'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Origin': f'https://{host}.ope.ee',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': f'https://{host}.ope.ee/auth/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = {
    'lang': 'et',
}

if loginmethod == 1: #Needs testing, unsure if works
    data = f'data%5BUser%5D%5Busername%5D={name_first}+{name_last}&data%5BUser%5D%5Bpassword%5D={password}'

    response = requestssession.post(f'https://{host}.ope.ee/auth/', headers=headers, params=params, cookies=cookies, data=data, verify=False)

if loginmethod == 2:
    data = f'data%5BUser%5D%5Busername%5D={name_first}+{name_last}&data%5BUser%5D%5Bpassword%5D='

    first_response = requests.post(f'https://{host}.ope.ee/auth/smartid', headers=headers, params=params, cookies=cookies, data=data, verify=True)
    first_response = json.loads(first_response.text)
    print(f"Your login code is: {first_response['data']['verification_code']}")    

    params = {
        'smartidsig': first_response['data']['status_url'][26:66],  #subject to being broken five times over
        'lang': 'et',
    }
    data = 'smartid_state=' + urllib.parse.quote(first_response['data']['state'])
    answer = False
    while answer == False:
        response = requestssession.post(f'https://{host}.ope.ee/auth/smartid/', headers=headers, params=params, cookies=cookies, data=data, verify=True)
        if len(response.text) == 0:
            webpage = requestssession.get(f'https://{host}.ope.ee')
            answer = True
        sleep(2)

    page = requestssession.get(response.headers['x-redirect'], cookies=cookies)

headers = {
    'Host': f'{host}.ope.ee',
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

def save_config_file():
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()

def getrawpost(message_id):
    page = requestssession.get(f'https://{host}.ope.ee/suhtlus/api/posts/get/{message_id}', headers=headers, params=params, cookies=cookies, verify=True)
    return page

#godsend
def get_chatpage():
    global chatspage
    chatspage = requestssession.get(f'https://{host}.ope.ee/suhtlus/api/channels/updates/a/inbox?v=2020&output-format=json&merge_events=0&get_post_membership_data=0&language=et')

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
    if message_choice == 'm': 
        for i in range(25-10):
            i += 10
            print(f"{i}) {chatdata['updates'][i]['title']}")
        message_choice = input('\nChoose message: ')
    message_id = chatdata['updates'][int(message_choice)]['id']
    displaymessage(message_id)
    input()

def open_chats():
    get_chatpage()
    choose_message()

def update_usercount():
    count = usercounter.updateusercount()
    print(f'Current usercount is {count}')
    config['host']['usercount'] = str(count)
    save_config_file()

def update_user_card_url():
    chat_response = requestssession.get('https://tamme.ope.ee/suhtlus/', headers=headers, cookies=cookies, verify=True)

    parsedinput = BeautifulSoup(chat_response.text, "lxml")
    meta_config = parsedinput.head.find('meta', attrs={'name':"suhtlus:config"}).get('content')
    user_card_url = str(json.loads(meta_config)['user_card_url'])
    config['user']['user_card_url'] = user_card_url
    save_config_file()



def gethomepage():
    homepage = requestssession.get(f"https://{host}.ope.ee/s/{config['user']['selfid']}", headers=headers, cookies=cookies, verify=True)
    parsed_output = BeautifulSoup(homepage.text, "lxml")
    return parsed_output

def getgrades():
    print('Grades:\n')
    gradedata = gethomepage()
    printablegrade = gradedata.body.findAll('div', attrs={'class':'stream-entry ng-grade-is-summary-wrapper'})
    
    for i in printablegrade:
        i = i.text.split('•')
        print(f'{i[0]:<60} • {i[1]}')

def gethomework():
    print('Homework:\n')
    gradedata = gethomepage()
    printablegrade = gradedata.body.findAll('div', attrs={'class':'todo_container'})
    # print(printablegrade.text)
    for i in printablegrade:
        print(f"Tähtaeg {i.attrs['data-date'][6:8]}.{i.attrs['data-date'][4:6]}")
        print(i.text.replace('\n',' ').replace('https://',' https://'),end='\n\n')
        
        # i = i.text.split('•')
        # print(f'{i[0]:<60} • {i[1]}')

# UID = {
#     'USERID' : '9999999999'
# }
# print(user_card_url.format(**UID))


# def submit_draft():
#     headers = {
#         'Host': 'tamme.ope.ee',
#         'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
#         'Sec-Ch-Ua-Mobile': '?0',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'Accept': '*/*',
#         'X-User-Token': xuid_token,
#         'X-Requested-With': 'XMLHttpRequest',
#         'X-App-Type': 'web',
#         'Sec-Ch-Ua-Platform': '"Linux"',
#         'Origin': 'https://tamme.ope.ee',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Dest': 'empty',
#         'Referer': 'https://tamme.ope.ee/suhtlus/p/13348039',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'en-US,en;q=0.9',
#     }

#     params = {
#         'v': '2020',
#         'save_draft': '1',
#     }

#     data = 'Post%5Bid%5D=13348039&Post%5Btitle%5D=So+anyways+what+is+this+I+do+neowitjsajkjdwijoidajwoijdoiajijdoij&Post%5Bevent_date%5D=&Post%5Bevent_time%5D=&Post%5Bevent_date_end%5D=&Post%5Bevent_time_end%5D=&Post%5Bbody%5D=joasdoijawidjoiawjdiowajoidjadawd'

#     response = requests.post('https://tamme.ope.ee/suhtlus/api/posts/edit', headers=headers, params=params, cookies=cookies, data=data, verify=True)
#     print(response)

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
    
    os.system('clear')

    if menu_choice == 3:
        open_chats()
    elif menu_choice == 5:
        submenu_choice = int(input(' 1) Search for name\n 2) Update usercount\n 3) Update local database\nSelect choice: '))
        if submenu_choice == 1:
            search.main()
            input()
        elif submenu_choice == 2:
            update_usercount()
            input()
        elif submenu_choice == 3:
            update_user_card_url()
            request.downloaddb()
            input()
    elif menu_choice == 1:
        getgrades()
        gethomework()
        input()
    # elif menu_choice == 9:
    #     chat_response = requestssession.get('https://tamme.ope.ee/suhtlus/', headers=headers, cookies=cookies, verify=True)
    #     parsedinput = BeautifulSoup(chat_response.text, "lxml")
    #     meta_config = parsedinput.head.find('meta', attrs={'name':"suhtlus:config"}).get('content')
    #     xuid_token = json.loads(meta_config)['user']['token']
    #     print(xuid_token)
    #     submit_draft()
