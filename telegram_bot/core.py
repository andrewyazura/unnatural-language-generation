import logging
import os
import random
import uuid

import tokenize_uk as tn
from telegram import ParseMode
from telegram.ext import (
    CommandHandler,
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

from .helpers import (
    get_graph,
    load_yaml,
    logged,
    restricted,
    set_graph,
    typing_action,
)

config = load_yaml('telegram_bot/bot_config.yaml')
phrases = load_yaml('telegram_bot/bot_phrases.yaml')

logging.basicConfig(**config['logging']['basic-config'])
logger = logging.getLogger(__name__)


@logged
def start_command(update, context):
    update.message.reply_text(phrases['start'])
    update.message.reply_text(phrases['help'])


@logged
def help_command(update, context):
    update.message.reply_text(phrases['help'])


@logged
@typing_action
def graph_command(update, context):
    graph = get_graph(config['generator']['path'])

    if not graph or not graph.nodes:
        update.message.reply_text(phrases['error']['empty-graph'])
        return

    update.message.reply_text(
        phrases['about-graph'].format(
            graph.number_of_nodes(),
            graph.number_of_edges(),
            int(graph.size('weight')),
            config['generator']['order'],
        ),
    )


@logged
@typing_action
def generate_command(update, context):
    try:
        if context.matches:
            length = int(context.matches[0][1])
        else:
            length = int(context.args[0])
    except (ValueError, IndexError) as exc:
        logging.error(exc)
        update.message.reply_text(phrases['error']['value-error'])
        return

    if length > config['generator']['max-text-length']:
        update.message.reply_text(phrases['error']['length-limit-exceeded'])
        return

    graph = get_graph(config['generator']['path'])

    if not graph or not graph.nodes:
        update.message.reply_text(phrases['error']['empty-graph'])
        return

    start = random.choice(
        [
            n.split()
            for n in graph.nodes
            if graph[n] and len(n.split()) == config['generator']['order']
        ]
    )
    sequence = generate_random_sequence(
        graph, length, start, config['generator']['order']
    )
    output = join_tokens(sequence)
    update.message.reply_text(output, parse_mode=None)


@logged
@restricted
@typing_action
def upload_text(update, context):
    set_graph(
        config['generator']['path'],
        convert_tokens_to_graph(
            tn.tokenize_words(update.message.text.lower()),
            config['generator']['order'],
            get_graph(config['generator']['path']),
        ),
    )
    update.message.reply_text(phrases['success']['processed'])


@logged
@restricted
@typing_action
def upload_file(update, context):
    file = update.message.effective_attachment.get_file()
    if os.path.basename(file['file_path']).split('.')[-1] != 'txt':
        update.message.reply_text(phrases['error']['wrong-file-format'])
        return

    try:
        path = os.path.join(
            config['telegram-bot']['temp-path'], uuid.uuid4().hex
        )
        file.download(path)

        with open(path, 'r') as f:
            set_graph(
                config['generator']['path'],
                convert_tokens_to_graph(
                    tn.tokenize_words(f.read().lower()),
                    config['generator']['order'],
                    get_graph(config['generator']['path']),
                ),
            )

        os.remove(path)
        update.message.reply_text(phrases['success']['processed'])

    except Exception as exc:
        logging.error(exc)
        update.message.reply_text(phrases['error']['unknown'])


@logged
@restricted
def clean_command(update, context):
    try:
        os.remove(config['generator']['path'])
        update.message.reply_text(phrases['success']['done'])

    except Exception as exc:
        logging.error(exc)
        update.message.reply_text(phrases['error']['unknown'])


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
    dispatcher.add_handler(CommandHandler('graph', graph_command))
    dispatcher.add_handler(CommandHandler('clean', clean_command))
    dispatcher.add_handler(
        CommandHandler('generate', generate_command, run_async=True)
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(r'^\+(\d+)$'), generate_command, run_async=True
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command, upload_text, run_async=True
        )
    )
    dispatcher.add_handler(
        MessageHandler(Filters.document, upload_file, run_async=True)
    )

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
