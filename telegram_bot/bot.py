import logging

import yaml
from telegram.ext import CommandHandler, Filters, Updater
from telegram.ext.messagehandler import MessageHandler

with open('telegram_bot/bot_config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

with open('telegram_bot/bot_phrases.yml', 'r') as stream:
    phrases = yaml.safe_load(stream)

logging.basicConfig(**config['logging'])
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(phrases['start'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def main():
    updater = Updater(**config['telegram-bot'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
