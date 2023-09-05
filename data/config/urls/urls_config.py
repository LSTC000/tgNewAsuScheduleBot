import os

from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

JSON_TOKEN = os.getenv('JSON_TOKEN')
