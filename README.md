# StuScraper

This project is currently unmaintained.

CLI tool to scrape Stuudium's ope.ee sites for user information.

Requres an account on site.

The current code doen't work as intended, but I belive the fix isn't that hard. The codebase itself is a bit suboptimally written, but I don't care for the code for now. Feel free to fork and maintain the project!

## Stu-cli

login works with password and with Smart-ID.

Some outdated examples can be found at [examples](./assets/examples.md)

## Installation

### Source

OS - all platform

Clone the repository and enter the directory

```
git clone https://github.com/goldenbeasty/stuscraper && cd stuscraper
```

and run `stu-cli.py`

```
python3 ./stu-cli.py
```

## First time login

If you want to change what school's Stuudium you log into delete the config.ini file found at `~/.config/stuscraper/config.ini` or in case of source installation in the same folder as the program `./config.ini`
The ability to do that in program will be added soon

## Fun facts about Stuudium

### Stuudium's security model

Stuudium has a permission based security model where school's IT-admins and other administrative staff have permission to view the whole platform as someone else (meaning you don't have any privacy on the platform)

### Suhtlus

The messaging feature is just build separately from everything else (still integrates though). Just has different dependecies and stuff.

### Teatchers can view your birthdays and a lot more stuff

### April fools

On April 1st 2022 you were able to submit "kind words to others" on stuudium and for the 1st and 2nd of April these messages could be seen on the user home page.

### Backend

The website is run on aws, it can most be seen in TERA, where files are hosted in s3 buckets.

### 1984

In the messaging section (as of 01.01.2023) you can react with emojis, currenttly you can react with up to eight different emojis out of which with only 6 at the same time.
It didn't use to be that way some time afte 15.01.2021 was the ability to react with any emoji removed. While you could react with any emoji some emojis were shadowbanned such as the eggplant emoji and the middle finger emoji.
Any emoji reaction isn't removed from the backend and posts older than 15.01.2021 can still be seen with any emoji. About that, the API endpoint for emojis wasn't removed until at least 19.01.2022, until that point I was still able to react to a message with a custom emoji by manually editing the POST request. Subsequent tries have failed.

![the last emoji](./assets/emoji.webp)

### other (technical)

#### list of all schools
https://assets.stuudium.net/_/config/clients
(includes test schools)
has chainged to

https://stuudium.com/_/pweb/get-public-clients 
(does not include test schools)

# Licence

Copyright © 2023 Goldenbeasty

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWA
