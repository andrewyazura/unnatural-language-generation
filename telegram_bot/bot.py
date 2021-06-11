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


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(phrases['start'])


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(phrases['help'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
