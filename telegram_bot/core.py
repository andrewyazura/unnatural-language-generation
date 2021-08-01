import logging
import os
import uuid

from telegram import ParseMode
from telegram.ext import (
    CommandHandler,
    Defaults,
    Filters,
    MessageHandler,
    Updater,
)

from .generator import Generator

from .helpers import (
    load_yaml,
    logged,
    restricted,
    typing_action,
)

config = load_yaml('telegram_bot/bot_config.yaml')
phrases = load_yaml('telegram_bot/bot_phrases.yaml')

public_generator = Generator(**config['generator']['graph'])
logging.basicConfig(**config['logging']['basic-config'])


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
    if public_generator.is_empty():
        update.message.reply_text(phrases['error']['empty-graph'])
        return

    update.message.reply_text(
        phrases['about-graph'].format(**public_generator.graph_info())
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

    if public_generator.is_empty():
        update.message.reply_text(phrases['error']['empty-graph'])
        return

    output = public_generator.generate(length)
    update.message.reply_text(output, parse_mode=None)


@logged
@restricted
@typing_action
def upload_text(update, context):
    public_generator.process_text(update.message.text)
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
            public_generator.process_text(f.read())

        os.remove(path)
        update.message.reply_text(phrases['success']['processed'])

    except Exception as exc:
        logging.error(exc)
        update.message.reply_text(phrases['error']['unknown'])


@logged
@restricted
@typing_action
def reload_command(update, context):
    public_generator.load_graph()
    update.message.reply_text(phrases['success']['done'])


@logged
@restricted
def clean_command(update, context):
    try:
        public_generator.delete_graph()
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
    updater = Updater(
        **config['telegram-bot']['updater'],
        defaults=defaults,
        use_context=True,
    )
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('clean', clean_command))
    dispatcher.add_handler(CommandHandler('graph', graph_command))
    dispatcher.add_handler(
        CommandHandler('reload', reload_command, run_async=True)
    )
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
