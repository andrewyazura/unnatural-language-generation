import logging
import os

import numpy as np
import yaml
from telegram import ChatAction, ParseMode
from telegram.ext import (
    CommandHandler,
    Defaults,
    Filters,
    MessageHandler,
    Updater,
)
from text_generation import (
    random_sentence,
    sentences_to_graph,
    text_to_sentences,
)

from .helpers import (
    delete_all_graphs,
    delete_user_graph,
    get_all_graphs,
    get_user_graph,
    restricted,
    update_user_graph,
)

with open('telegram_bot/bot_config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

with open('telegram_bot/bot_phrases.yml', 'r') as stream:
    phrases = yaml.safe_load(stream)

logging.basicConfig(**config['logging'])
logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text(phrases['start'] + '\n\n' + phrases['help'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def stats_command(update, context):
    user_id = update.message.chat_id
    graph = get_user_graph(user_id)

    if graph:
        update.message.reply_text(
            phrases['stats'].format(
                graph.number_of_nodes(),
                graph.number_of_edges(),
                graph.size('weight'),
            )
        )

    else:
        update.message.reply_text(phrases['no-graph'])


@restricted
def stats_all_command(update, context):
    for filename, graph in get_all_graphs():
        update.message.reply_text(
            f'*Користувач:* {filename}\n'
            + phrases['stats'].format(
                graph.number_of_nodes(),
                graph.number_of_edges(),
                graph.size('weight'),
            )
        )


def generate_command(update, context):
    user_id = update.message.chat_id
    context.bot.send_chat_action(user_id, ChatAction.TYPING)

    try:
        length = int(context.args[0])
        graph = get_user_graph(user_id)
        word = np.random.choice(graph.nodes)

        context.bot.send_message(
            user_id,
            random_sentence(graph, word, length),
        )

    except (IndexError, ValueError):
        update.message.reply_text(
            phrases['generate-help'],
        )

    except:
        update.message.reply_text(phrases['no-graph'])


def clear_command(update, context):
    try:
        delete_user_graph(update.message.chat_id)
        update.message.reply_text(phrases['done'])

    except:
        update.message.reply_text(phrases['no-graph'])


@restricted
def clear_user_command(update, context):
    try:
        user_id = int(context.args[0])
        delete_user_graph(user_id)
        update.message.reply_text(phrases['done'])

    except:
        update.message.reply_text(phrases['clear-user-help'])


@restricted
def clear_all_command(update, context):
    delete_all_graphs()
    update.message.reply_text(phrases['done'])


def handle_text(update, context):
    user_id = update.message.chat_id
    context.bot.send_chat_action(user_id, ChatAction.TYPING)

    update_user_graph(
        user_id,
        sentences_to_graph(
            text_to_sentences(update.message.text),
            get_user_graph(user_id),
        ),
    )

    context.bot.send_message(user_id, phrases['processed'])


def handle_file(update, context):
    user_id = update.message.chat_id
    file = update.message.effective_attachment.get_file()

    if os.path.basename(file['file_path']).split('.')[-1] == 'txt':
        try:
            path = config['user-texts-path'].format(user_id)
            file.download(path)

            with open(path, 'r') as f:
                update_user_graph(
                    user_id,
                    sentences_to_graph(
                        text_to_sentences(f.read()),
                        get_user_graph(user_id),
                    ),
                )

            os.remove(path)
            context.bot.send_message(user_id, phrases['processed'])

        except Exception as exc:
            logging.error(exc)
            context.bot.send_message(user_id, phrases['error'])

    else:
        context.bot.send_message(user_id, phrases['wrong-file'])


def error_handler(update, context):
    logging.error(context.error)


def run_bot():
    defaults = Defaults(
        parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )
    updater = Updater(**config['telegram-bot'], defaults=defaults)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('stats_all', stats_all_command))
    dispatcher.add_handler(CommandHandler('stats', stats_command))
    dispatcher.add_handler(CommandHandler('generate', generate_command))
    dispatcher.add_handler(CommandHandler('clear_all', clear_all_command))
    dispatcher.add_handler(CommandHandler('clear_user', clear_user_command))
    dispatcher.add_handler(CommandHandler('clear', clear_command))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_text)
    )

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
