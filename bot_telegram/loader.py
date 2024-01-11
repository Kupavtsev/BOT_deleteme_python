from aiogram import Bot, Dispatcher
from config import *
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
 
 
bot = Bot(TOKEN, parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )