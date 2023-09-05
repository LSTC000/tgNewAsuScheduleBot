import os

from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')

PARSE_MODE = 'HTML'
SKIP_UPDATES = True
DISABLE_WEB_PAGE_PREVIEW = True
