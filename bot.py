import logging

import yaml
from aiogram import Bot, Dispatcher, executor, types

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

logging.basicConfig(**config['logging'])

bot = Bot(token=config['telegram-bot']['token'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
