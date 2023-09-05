# Hi, this is a new Telegram bot for schedule of Altay State University.

This bot help you to get your schedule on today, tomorrow week or your target date.

### To launch the bot:
1. __Clone__ the repository: git clone https://github.com/LSTC000/tgNewAsuScheduleBot.git
2. __Create__ a file __.env__ according to the template __.env.dist__. 
The __JSON_TOKEN__ token is a secret.
3. Due to the fact that __pymorphy2 died__ in python 3.11, it is necessary to replace pymorphy2 with pymorphy3 in the import in the following files: __venv\Lib\site-packages\natasha\morph\vocab.py__ and __venv\Lib\site-packages\yargy\morph.py__ . And then __remove pymorphy2__ installed in place with natasha: pip uninstall pymorphy2 -y.

__Docker__ uses an image suitable for pymorphy2, but does not yet support voice recognition.
4. __Launch__ docker-compose: docker-compose up or docker-compose up -d.
