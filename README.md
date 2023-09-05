# Hi, this is a new Telegram bot for schedule of Altay State University.

This bot help you to get your schedule on today, tomorrow week or your target date.

### To launch the bot:
1. __Clone__ the repository: git clone https://github.com/LSTC000/tgNewAsuScheduleBot.git
2. __Create__ a file __.env__ according to the template __.env.dist__. 
The __JSON_TOKEN__ token is a secret.
3. Due to the fact that __pymorphy2 died__ in python 3.11, it is necessary to replace pymorphy2 with pymorphy3 in __natasha__. You can do this in files that will cause errors in the terminal when entering __a voice message__ due to incorrect import of pymorphy2.
4. __Launch__ docker-compose.
