#!/usr/bin/env python3

import json
from time import sleep, time
import requests
import urllib.parse
from bs4 import BeautifulSoup
import configparser
from getpass import getpass
import pickle
import os
import re


##################
### File paths ###
##################

packagebuild = False

if packagebuild:
    configpath = "~/.config/stuscraper/config.ini"
    dbpath = "~/.config/stuscraper/user_database.json"
    cachepath = "~/.cache/stuscraper/"
    cookiejarpath = "~/.config/stuscraper/cookiejar"
else:
    configpath = "config.ini"
    dbpath = "user_database.json"
    cachepath = ""
    cookiejarpath = "cookiejar"

configpath = os.path.expanduser(configpath)
dbpath = os.path.expanduser(dbpath)
cachepath = os.path.expanduser(cachepath)
cookiejarpath = os.path.expanduser(cookiejarpath)

###################
### Local files ###
###################

if not packagebuild: # auxilarary packages in this project default to packagebuild = False, because the projcet is not currently meant for use as a dependency. If you feel inclined to use it as a dependency for other projects feel free to leave a issue at the repo!
    import bootstrap
    bootstrap.main()
    
    import stu_download # soon to be deprecated due to fun circumstances
    import search
    import usercounter
    import stu_imgdl
    import dbmanipulation

else:
    from . import bootstrap
    bootstrap.main(packagebuild=True)
    
    from . import stu_download
    from . import search
    from . import usercounter
    from . import stu_imgdl
    from . import dbmanipulation
    

##############################
### Standard configuration ###
##############################

config = configparser.ConfigParser(interpolation=None)
config.read(configpath)
host = config['host']['hostname']
requestssession = requests.Session()

last_homepage_fetch = 0


#############
### Login ###
#############

print(f"logging in to {host}") 
loginmethod = int(input(' 1) Password\n 2) Smart-ID\n 3) Existing session\n 4) Change school\nSelect login method: '))

if loginmethod == 1:
    username = str(input('Sisesta nimi: '))
    username = username.replace(' ', '+')
    password = getpass('Sisesta parool: ')
elif loginmethod == 2:
    username = str(input('Sisesta nimi: '))
    username = username.replace(' ', '+')
elif loginmethod == 3:
    with open(cookiejarpath, 'rb') as f:
        requestssession.cookies.update(pickle.load(f))
elif loginmethod == 4:
    config['host']['hostname'] = bootstrap.gethost()
    with open (configpath, "w") as f:
        config.write(f)
        f.close()
    exit(f"Changed host to {config['host']['hostname']}")
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
    data = f'data%5BUser%5D%5Busername%5D={username}&data%5BUser%5D%5Bpassword%5D={password}&data%5BUser%5D%5Bautologin_do%5D=on'
    response = requestssession.post(f'https://{host}.ope.ee/auth/', headers=headers, params=params, cookies=cookies, data=data)

if loginmethod == 2:
    data = f'data%5BUser%5D%5Busername%5D={username}&data%5BUser%5D%5Bpassword%5D=&data%5BUser%5D%5Bautologin_do%5D=on'
    first_response = requests.post(f'https://{host}.ope.ee/auth/smartid', headers=headers, params=params, cookies=cookies, data=data)
    first_response = json.loads(first_response.text)
    print(f"Your login code is: {first_response['data']['verification_code']}")    

    params = {
        'smartidsig': re.findall(r"=(\S+)&", first_response['data']['status_url']),
        'lang': 'et',
    }
    data = 'smartid_state=' + urllib.parse.quote(first_response['data']['state'])
    list_of_returned_users = False
    while list_of_returned_users == False:
        response = requestssession.post(f'https://{host}.ope.ee/auth/smartid/', headers=headers, params=params, cookies=cookies, data=data)
        if len(response.text) == 0:
            webpage = requestssession.get(f'https://{host}.ope.ee')
            list_of_returned_users = True
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

# After receiving the session token dump the cookies to a file
with open(cookiejarpath, 'wb') as f:
    pickle.dump(requestssession.cookies, f)


#################
### Functions ### 
#################

# Save config file after changes
def save_config_file():
    with open (configpath, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def logout():
    os.remove(cookiejarpath)
    requestssession.get(f'https://{host}.ope.ee/auth/logout', headers=headers, params=params)
    quit("Logged out")

# Get raw post html using the post id
def getrawpost(message_id):
    page = requestssession.get(f'https://{host}.ope.ee/suhtlus/api/posts/get/{message_id}', headers=headers, params=params, cookies=cookies)
    return page

# Get JSON formatted chats page
def get_chatpage():
    global chatspage
    chatspage = requestssession.get(f'https://{host}.ope.ee/suhtlus/api/channels/updates/a/inbox?v=2020&output-format=json&merge_events=0&get_post_membership_data=0&language=et')

# Display message body
def displaymessage(message_id):
    page = requestssession.get(f'https://{host}.ope.ee/suhtlus/api/posts/get/{message_id}', headers=headers, cookies=cookies)
    page = json.loads(page.text)
    print(page['post']['title'])
    print(page['post']['user_name_first'], page['post']['user_name_last'], end='\n\n\n')
    print(page['post']['body'])
    if page['post']['comment_count'] != 0 :
        print('\n\nComments:')
        comments = requestssession.get(f"https://{host}.ope.ee/suhtlus/api/{page['next_comments_url']}", headers=headers, cookies=cookies)
        comments = json.loads(comments.text)
        for comment in comments:
            print(comment['user_name_first'], comment['user_name_last'])
            print(comment['body'], end='\n\n')
        

# Choose the message to open
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

def open_chats():
    get_chatpage()
    choose_message()
    input()
    
def update_usercount():
    count = usercounter.updateusercount(config)
    print(f'Current usercount is {count}')
    config['host']['usercount'] = str(count)
    save_config_file()

# Update user data from chats page config
def update_user_data():
    chat_response = requestssession.get(f'https://{host}.ope.ee/suhtlus/', headers=headers, cookies=cookies)

    parsedinput = BeautifulSoup(chat_response.text, "lxml")
    meta_config = parsedinput.head.find('meta', attrs={'name':"suhtlus:config"}).get('content')
    parsed = json.loads(meta_config)
    user_card_url = str(parsed['user_card_url'])
    config['user']['user_card_url'] = user_card_url
    uid = str(parsed['user']['id'])
    config['user']['selfid'] = uid

    print(f"Logged in as {str(parsed['user']['name_first'])} {str(parsed['user']['name_last'])}")
    save_config_file()

# Get the homepage with homework and grades
def gethomepage():
    global parsed_homepage
    global last_homepage_fetch
    if (time() - last_homepage_fetch) > 20:
        homepage = requestssession.get(f"https://{host}.ope.ee/s/{config['user']['selfid']}", headers=headers, cookies=cookies)
        last_homepage_fetch = time()
        parsed_homepage = BeautifulSoup(homepage.text, "lxml")
    return parsed_homepage


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


#########################
### Message functions ###
#########################

def send_message(Title, Message, subjects):
    headers = {
        'Host': f'{host}.ope.ee',
        'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-User-Token': get_xuid_token(),
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Type': 'web',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': f'https://{host}.ope.ee',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://{host}.ope.ee/suhtlus/p/new',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = {
        'v': '2020',
    }

    data = {
        'Post[title]': Title,
        'Post[event_date]':'',
        'Post[event_time]':'',
        'Post[event_date_end]':'',
        'Post[event_time_end]':'',
        'Post[body]':Message,
    }
    data = data | subjects

    response = requestssession.post(f'https://{host}.ope.ee/suhtlus/api/posts/edit', headers=headers, params=params, cookies=cookies, data=data)
    if response.status_code == 200:
        print('Message sent!')
    else:
        print('Error sending message!')

def get_xuid_token():
    chat_response = requestssession.get('https://tamme.ope.ee/suhtlus/', headers=headers, cookies=cookies)
    parsedinput = BeautifulSoup(chat_response.text, "lxml")
    meta_config = parsedinput.head.find('meta', attrs={'name':"suhtlus:config"}).get('content')
    xuid_token = json.loads(meta_config)['user']['token']
    return xuid_token

# user interface to create and send messages
def create_message():
    subjects = {}

    composing_messsage = True
    while composing_messsage:
        print(""" 
        1) Edit title
        2) Edit message
        3) Add subject
        4) Add subject by description (e.g. õpilane (10ME) )
        5) Remove subject
        6) Send message
        q) Cancel
        99) Add everyone to subjects
         """)
        choice = input("Choose an option: ")
        if choice == '1':
            Title = input("Title: ")
        elif choice == '2':
            print("Message(Emty line + Ctrl + C to finish): ")
            Message = ''
            try:
                while True:
                    Message += input() + '\n'
            except KeyboardInterrupt:
                print('Message: \n\n' + Message)
        elif choice == '3':            
            search.main(config)
            user_to_add = input("Choose user id to add: ")
            if type(menu_choice) == int:
                subjects[f'Post[recipients][{user_to_add}]'] = f'{host}-{user_to_add}-user'
        elif choice == '4':
            description_query = input("Choose subject description: ")
            user_to_add = search.get_user_by_description(config, description_query)
            for user in user_to_add:
                subjects[f'Post[recipients][{user}]'] = f'{host}-{user}-user'
        elif choice == '5':
            for i in subjects:
                print(i)
            user_to_remove = input("Choose user id to remove: ")
            if type(menu_choice) == int:
                del subjects[f'Post[recipients][{user_to_remove}]']
        elif choice == '6':
            send_message(Title, Message, subjects)
            composing_messsage = False
        elif choice == 'q':
            composing_messsage = False
        elif choice == '99':
            for i in range(1, int(config['host']['usercount']) + 1):
                subjects[f'Post[recipients][{i}]'] = f'{host}-{i}-user'
        elif choice == 'l':
            print(f"Total of {len(subjects)} subjects")
            print(subjects)

#####################################
### I am your benevolent dictator ###
#####################################

def make_userspace_message(trialcount=10000):
    subjects = {}
    for i in range(1, trialcount):
        subjects[f'Post[recipients][{i}]'] = f'{host}-{i}-user'
    
    headers = {
        'Host': f'{host}.ope.ee',
        'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-User-Token': get_xuid_token(),
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Type': 'web',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': f'https://{host}.ope.ee',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://{host}.ope.ee/suhtlus/p/new',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = {
        'v': '2020',
        'save_draft': '1'
    }

    data = {
        'Post[title]':'',
        'Post[event_date]':'',
        'Post[event_time]':'',
        'Post[event_date_end]':'',
        'Post[event_time_end]':'',
        'Post[body]':'',
    }
    data = data | subjects
    
    r = requestssession.post(url=f"https://{host}.ope.ee/suhtlus/api/posts/edit?v=2020&save_draft=1", headers=headers, params=params, cookies=cookies, data=data)
    # r = requestssession.post(url=f"https://{host}.ope.ee/suhtlus/api/posts/edit", headers=headers, params=params, cookies=cookies, data=data)
    rjson = r.json()
    with open("debug_json.json", "w") as f:
        json.dump(rjson, f)
        f.close()
    if not rjson["ok"]: exit(rjson)
    id = rjson["data"]["id"]

    return id

def get_message_data(id):


    rjson = requestssession.get(url=f"https://{host}.ope.ee/suhtlus/api/posts/get/{id}?v=2020&output-format=json").json()
    data = rjson["post"]
    return data

def delete_message(id):
    headers = {
        'Host': f'{host}.ope.ee',
        'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="96"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-User-Token': get_xuid_token(),
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Type': 'web',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': f'https://{host}.ope.ee',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://{host}.ope.ee/suhtlus/p/new',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = {
        'v': '2020',
    }

    data = {
        'Post[id]': id,
        'Post[title]':'',
        'Post[event_date]':'',
        'Post[event_time]':'',
        'Post[event_date_end]':'',
        'Post[event_time_end]':'',
        'Post[body]':'',
        'Post[do_delete]':'1'
    }
    requestssession.get(url=f"https://{host}.ope.ee/suhtlus/api/posts/edit", headers=headers, params=params, cookies=cookies, data=data)

def db_download(): # This is a management function, might be removed in the future for a more intuative workflow
    testsize = 10000
    sufficent = False
    while not sufficent:
        postid = make_userspace_message(trialcount=testsize)
        data = get_message_data(postid)
        if data["post_users_count"] + 2 >= testsize:
            testsize *= 2
            delete_message(id)
        else:
            sufficent = True
    config["host"]["usercount"] = str(data["post_users_count"])
    save_config_file()
    userdata = data["post_membership_data_object"]["users"]
    with open(cachepath + "namedata.json", "w") as f:
        json.dump(userdata, f)
        f.close()
    print(userdata)
    delete_message(id)

#################
### Main loop ###
#################

# update configuraiton file and greet user
update_user_data()
if os.path.exists(dbpath):
    data = json.load(open(dbpath))
    print(f"User database last updated {int((time() - int(data['last_updated'])) / 86400)} day(s) ago")
else:
    print("No database detected, many functions require the downloaded database, you can do it by choosing 5")


while True:
    #print('''
    #1) Päevik
    #2) Tera (not implemented)
    #3) Suhtlus
    #4) Loo sõnum
    #5) Automatic database management
    #6) Manual database functions

    #l) logout
    #q) quit
    #''')
    
    #menu_choice = input('Choose menu: ')

    input("\n\nuevc2 POC [ENTER] to continue")

    db_download()
    print("Check the current directory for namedata.json")
    exit()
    continue

    # Exit with q
    if menu_choice == 'q':
        quit('')
    
    # Logout with l
    elif menu_choice == 'l':
        logout()

    os.system('clear')
    
    if menu_choice.isnumeric():
        menu_choice = int(menu_choice)

        if menu_choice == 1:
            getgrades()
            gethomework()
            input()
        elif menu_choice == 3:
            open_chats()
        elif menu_choice == 4:
            create_message()
        elif menu_choice == 5:
            update_usercount()
            stu_download.downloaddb(config, cachepath)
            dbmanipulation.consentrate_db(config, dbpath, cachepath)
            print("\nUpdated database!")
            input()
        elif menu_choice == 6:
            submenu_choice = input('''
    1) Search for name
    2) Update usercount
    3) Update local database
    4) Download all avatar icons
    5) Create/update single file database
    6) Sort custom images
    7) Search by desctiption
    8) Individual user/file scraping (source installation only)

Select choice: ''')
            if submenu_choice.isnumeric():
                submenu_choice = int(submenu_choice)
                if submenu_choice == 1:
                    search.main(config)
                    input()
                elif submenu_choice == 2:
                    update_usercount()
                    input()
                elif submenu_choice == 3:
                    stu_download.downloaddb(config, cachepath)
                    input()
                elif submenu_choice == 4:
                    stu_imgdl.downloadicons(config)
                    input()
                elif submenu_choice == 5:
                    dbmanipulation.consentrate_db(config, dbpath, cachepath)
                elif submenu_choice == 6:
                    print("""Not 100% accruate""")
                    stu_imgdl.sort_default_images()
                elif submenu_choice == 7:
                    os.system("clear")
                    description_query = input("Choose subject description: ")
                    print("")
                    list_of_returned_users = search.get_user_by_description(config, description_query)
                    search.list_users(config=config, list_of_users=list_of_returned_users)
                    print(f"\nTotal of {len(list_of_returned_users)} results\n")
                elif submenu_choice == 8:
                    if packagebuild:
                        print("This option is unavalable to installation via pip, download from source to enable individual file scraping")
                        continue
                    try: config["user"]["scraper"]
                    except KeyError:
                        config["user"]["scraper"] = "False"
                        save_config_file()
                    a = input(f"Scraping option is for people who wish to keep track of databases using git. Value toggles whether the scripts saves user databse to ./users/ folder as individual files. The suggested way to keep track is to use the user_database.json file and therefore this is a legacy feature.\n\n Currently set to {config['user']['scraper']}\n Do you wish to change it? [y/N]\n").lower()
                    if a != 'y': continue
                    if config["user"]["scraper"] == "False":
                        config["user"]["scraper"] = "True"
                    else:
                        config["user"]["scraper"] = "False"
                    save_config_file()
                elif submenu_choice == 11:
                    db_download()
                else:
                    print("Invalid choice")
