import logging

import numpy as np
import yaml
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from text_generation import (
    random_sentence,
    sentences_to_graph,
    text_to_sentences,
)

from .helpers import get_user_graph, update_user_graph, delete_user_graph

with open('telegram_bot/bot_config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

with open('telegram_bot/bot_phrases.yml', 'r') as stream:
    phrases = yaml.safe_load(stream)

logging.basicConfig(**config['logging'])
logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text(
        phrases['start'],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def help_command(update, context):
    update.message.reply_text(
        phrases['help'],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def generate_command(update, context):
    user_id = update.message.chat_id
    context.bot.send_chat_action(user_id, 'typing')

    try:
        length = int(context.args[0])
        graph = get_user_graph(user_id)
        word = np.random.choice(graph.nodes)

        context.bot.send_message(
            user_id,
            random_sentence(graph, word, length),
        )

    except (IndexError, ValueError):
        update.message.reply_text(phrases['generate_help'])


def clear_command(update, context):
    delete_user_graph(update.message.chat_id)
    update.message.reply_text(phrases['done'])


def handle_text(update, context):
    user_id = update.message.chat_id
    context.bot.send_chat_action(user_id, 'typing')

    update_user_graph(
        user_id,
        sentences_to_graph(
            text_to_sentences(update.message.text),
            get_user_graph(user_id),
        ),
    )

    context.bot.send_message(user_id, phrases['processed'])


def error_handler(update, context):
    logging.error(context.error)


def main():
    updater = Updater(**config['telegram-bot'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('generate', generate_command))
    dispatcher.add_handler(CommandHandler('clear', clear_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_text)
    )

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
