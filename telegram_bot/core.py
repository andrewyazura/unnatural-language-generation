import logging
import sqlite3

import yaml
from telegram import (
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Defaults,
    Filters,
    MessageHandler,
    Updater,
)
from text_generation import (
    convert_tokens_to_graph,
    generate_random_sequence,
    join_tokens,
)

with open('telegram_bot/bot_config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

with open('telegram_bot/bot_phrases.yaml', 'r') as stream:
    phrases = yaml.safe_load(stream)

with open('telegram_bot/sql_queries.yaml', 'r') as stream:
    sql_queries = yaml.safe_load(stream)

logging.basicConfig(**config['logging']['basic-config'])
logger = logging.getLogger(__name__)

con = sqlite3.connect(**config['database']['connect'])
cur = con.cursor()
cur.execute(sql_queries['create-db'])


def start_command(update, context):
    update.message.reply_text(phrases['start'])
    update.message.reply_text(phrases['help'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def error_handler(update, context):
    logging.error(context.error)


def run_bot():
    defaults = Defaults(
        parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True
    )
    updater = Updater(**config['telegram-bot']['updater'], defaults=defaults)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
