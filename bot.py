import logging

import yaml
from aiogram import Bot, Dispatcher, executor, types

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

with open('phrases.yml', 'r') as stream:
    phrases = yaml.safe_load(stream)

logging.basicConfig(**config['logging'])
bot = Bot(**config['telegram-bot'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(phrases['start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
