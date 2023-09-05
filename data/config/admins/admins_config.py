import os

from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

ADMINS = os.getenv('ADMINS').split(',')
ADMINS = list(map(int, ADMINS)) if ADMINS[-1] else list(map(int, ADMINS[:-1]))
