import logging
import random

import networkx as nx
from networkx.readwrite import node_link_data, node_link_graph
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Defaults,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater,
)
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
        context.user_data['current_graph'] = None

    update.message.reply_text(phrases['start'])
    update.message.reply_text(phrases['help'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def cancel_command(update, context):
    update.message.reply_text(phrases['cancelled'])


def generate_command(update, context):
    graph_data = context.user_data['graphs'].get(
        context.user_data['current_graph'], None
    )

    if not graph_data:
        return

    try:
        if context.matches:
            words = int(context.matches[0][1])
        else:
            words = int(context.args[0])
    except (ValueError, IndexError) as exc:
        logging.error(exc)
        update.message.reply_text(phrases['error']['value-error'])
        return

    graph = node_link_graph(graph_data)

    if not graph.nodes:
        update.message.reply_text(phrases['error']['empty-graph'])
        return

    start = random.choice(
        [
            n.split()
            for n in graph.nodes
            if graph[n] and len(n.split()) == config['order']
        ]
    )
    sequence = generate_random_sequence(
        graph, words, start, config['generator']['order']
    )
    output = join_tokens(sequence)
    update.message.reply_text(output)


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


def current_graph(update, context):
    if not context.user_data['graphs']:
        update.message.reply_text(phrases['error']['no-graphs'])
        return

    update.message.reply_text(
        phrases['current-graph'].format(context.user_data['current_graph'])
    )


def list_graphs(update, context):
    custom_keyboard = [
        [InlineKeyboardButton(name, callback_data='use.' + name)]
        for name in context.user_data['graphs']
    ]

    if not custom_keyboard:
        update.message.reply_text(phrases['error']['no-graphs'])
        return

    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        phrases['choose-graph'], reply_markup=reply_markup
    )


def delete_graph(update, context):
    custom_keyboard = [
        [
            InlineKeyboardButton(name, callback_data='del.' + name)
            for name in context.user_data['graphs']
        ]
    ]

    if not custom_keyboard:
        update.message.reply_text(phrases['error']['no-graphs'])
        return

    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        phrases['choose-graph'], reply_markup=reply_markup
    )


def inline_button_callback(update, context):
    query = update.callback_query
    query.answer()

    data = query.data.split('.')
    other = ''.join(data[1:])

    if data[0] == 'use':
        context.user_data['current_graph'] = other
        query.edit_message_text(text=phrases['changed-graph'].format(other))

    elif data[0] == 'del':
        g = context.user_data['graphs'].pop(other, None)

        if not g:
            query.edit_message_text(text=phrases['error']['no-such-graph'])
            return

        query.edit_message_text(text=phrases['deleted-graph'].format(other))


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
    dispatcher.add_handler(CommandHandler('generate', generate_command))
    dispatcher.add_handler(
        MessageHandler(Filters.regex(r'^\+(\d+)$'), generate_command)
    )
    dispatcher.add_handler(CommandHandler('current_graph', current_graph))
    dispatcher.add_handler(CommandHandler('list_graphs', list_graphs))
    dispatcher.add_handler(CommandHandler('delete_graph', delete_graph))
    dispatcher.add_handler(CallbackQueryHandler(inline_button_callback))
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
