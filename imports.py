import config
import logging
import markup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pymysql
import datetime
import re
from typing import List, NamedTuple, Optional
import time

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connection = pymysql.connect(host=config.host,
                             port=3306,
                             user=config.user,
                             password=config.password,
                             db=config.db_name)