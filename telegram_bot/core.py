import logging

import networkx as nx
from networkx.readwrite import node_link_data, node_link_graph
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
)
from telegram.ext import (
    CommandHandler,
    Defaults,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater,
)
from telegram.ext.conversationhandler import ConversationHandler
from text_generation import (
    convert_tokens_to_graph,
    generate_random_sequence,
    join_tokens,
)

from .helpers import load_yaml

config = load_yaml('telegram_bot/bot_config.yaml')
phrases = load_yaml('telegram_bot/bot_phrases.yaml')

logging.basicConfig(**config['logging']['basic-config'])
logger = logging.getLogger(__name__)

GRAPH_NAME_STATE = 42


def start_command(update, context):
    if not context.user_data:
        context.user_data['graphs'] = {}

    update.message.reply_text(phrases['start'])
    update.message.reply_text(phrases['help'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def cancel_command(update, context):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(phrases['cancelled'], reply_markup=reply_markup)
    return ConversationHandler.END


def create_graph_entry(update, context):
    if len(context.user_data['graphs']) >= 3:
        update.message.reply_text(phrases['error']['many-graphs'])
        return ConversationHandler.END

    update.message.reply_text(phrases['ask-graph-name'])
    return GRAPH_NAME_STATE


def create_graph(update, context):
    if update.message.text in context.user_data['graphs']:
        update.message.reply_text(phrases['error']['graph-exists'])

    else:
        graph = nx.DiGraph()
        context.user_data['graphs'][update.message.text] = node_link_data(
            graph
        )
        update.message.reply_text(phrases['success']['saved'])

    return ConversationHandler.END


def delete_graph_entry(update, context):
    custom_keyboard = [[name] for name in context.user_data['graphs']]

    if not custom_keyboard:
        update.message.reply_text(phrases['error']['no-graphs'])
        return ConversationHandler.END

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        phrases['ask-graph-name'], reply_markup=reply_markup
    )
    return GRAPH_NAME_STATE


def delete_graph(update, context):
    g = context.user_data['graphs'].pop(update.message.text, None)

    if not g:
        update.message.reply_text(phrases['error']['no-such-graph'])
        return GRAPH_NAME_STATE

    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        phrases['success']['done'], reply_markup=reply_markup
    )
    return ConversationHandler.END


def error_handler(update, context):
    logging.error(context.error)


def run_bot():
    defaults = Defaults(
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
    )
    persistence = PicklePersistence(
        **config['telegram-bot']['persistence'],
    )
    updater = Updater(
        **config['telegram-bot']['updater'],
        defaults=defaults,
        persistence=persistence,
        use_context=True,
    )
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('delete_graph', delete_graph_entry)],
            states={
                GRAPH_NAME_STATE: [
                    MessageHandler(
                        Filters.text & (~Filters.command), delete_graph
                    )
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel_command)],
        )
    )
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('create_graph', create_graph_entry)],
            states={
                GRAPH_NAME_STATE: [
                    MessageHandler(
                        Filters.text & (~Filters.command), create_graph
                    )
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel_command)],
        )
    )

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
