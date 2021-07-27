import logging
import os
import random
import uuid
from functools import wraps

from telegram import ChatAction, ParseMode
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

from .helpers import get_graph, load_yaml, set_graph

config = load_yaml('telegram_bot/bot_config.yaml')
phrases = load_yaml('telegram_bot/bot_phrases.yaml')

logging.basicConfig(**config['logging']['basic-config'])
logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in config['telegram-bot']['admin-ids']:
            logging.warn('unauthorized access denied for {}.'.format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def start_command(update, context):
    update.message.reply_text(phrases['start'])
    update.message.reply_text(phrases['help'])


def help_command(update, context):
    update.message.reply_text(phrases['help'])


def generate_command(update, context):
    try:
        if context.matches:
            words = int(context.matches[0][1])
        else:
            words = int(context.args[0])
    except (ValueError, IndexError) as exc:
        update.message.reply_text(phrases['error']['value-error'])
        logging.error(exc)
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
        graph, words, start, config['generator']['order']
    )
    output = join_tokens(sequence)
    update.message.reply_text(output)


@restricted
def upload_text(update, context):
    pass


@restricted
def upload_file(update, context):
    user_id = update.message.chat_id
    file = update.message.effective_attachment.get_file()
    context.bot.send_chat_action(user_id, ChatAction.TYPING)

    if os.path.basename(file['file_path']).split('.')[-1] == 'txt':
        try:
            path = os.path.join(
                config['telegram-bot']['temp-path'], uuid.uuid4()
            )
            file.download(path)

            with open(path, 'r') as f:
                set_graph(
                    config['generator']['path'],
                    convert_tokens_to_graph(
                        f.read(),
                        config['generator']['order'],
                        get_graph(config['generator']['path']),
                    ),
                )

            os.remove(path)
            context.bot.send_message(user_id, phrases['success']['done'])

        except Exception as exc:
            logging.error(exc)
            context.bot.send_message(user_id, phrases['error']['unknown'])

    else:
        context.bot.send_message(user_id, phrases['error']['wrong-file'])


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
