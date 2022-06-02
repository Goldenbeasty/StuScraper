# How to use stu-cli
Some menus expect a return

## downloading the database
```
Logged in as Eesnimi Perekonnanimi

    1) Päevik
    2) Tera
    3) Suhtlus
    4) Loo sõnum
    5) Search user
    
Choose menu: 5

 1) Search for name
 2) Update usercount
 3) Update local database
Select choice: 2
Current usercount is 3076

    1) Päevik
    2) Tera
    3) Suhtlus
    4) Loo sõnum
    5) Search user
    
Choose menu: 5

 1) Search for name
 2) Update usercount
 3) Update local database
Select choice: 3

...
3072
3063
3069
3066
3074
Elapsed Time: 34.2168653011322
With avarage speed of 89.89718879649148


```
## sending messages
**To send messages you have to have downloaded the database!**

### send message to a group

in this example we send a message to group of students that have õpilane (10it) in their description. We can leave out some characters because we know that they are the only ones with that part of their description.


```
        1) Edit title
        2) Edit message
        3) Add subject
        4) Add subject by description (e.g. õpilane (10ME) )
        5) Remove subject
        6) Send message
        q) Cancel
        99) Add everyone to subjects
         
    Choose an option: 4
    Choose subject description: lane (10it
```
### Creating the body

```
        1) Edit title
        2) Edit message
        3) Add subject
        4) Add subject by description (e.g. õpilane (10ME) )
        5) Remove subject
        6) Send message
        q) Cancel
        99) Add everyone to subjects
         
    Choose an option: 2   
    Message(Emty line + Ctrl + C to finish): 
    This is the body of the message
    This is the next line
    and I need to leave an emty line and then press ctrl c to finish
    just like   
    ^CMessage: 

    This is the body of the message
    This is the next line
    and I need to leave an emty line and then press ctrl c to finish
    just like
```
**going back to edit the message overwrites the body**
