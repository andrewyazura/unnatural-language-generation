import json
import logging
import os
from functools import wraps

import yaml
from networkx.readwrite import node_link_data, node_link_graph
from telegram import ChatAction


def load_yaml(filename):
    with open(filename, 'r') as stream:
        file = yaml.safe_load(stream)
    return file


config = load_yaml('telegram_bot/bot_config.yaml')


def get_graph(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return node_link_graph(json.load(f))

    return None


def set_graph(filename, graph):
    with open(filename, 'w+') as f:
        json.dump(node_link_data(graph), f)


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in config['telegram-bot']['admin-ids']:
            logging.warn('unauthorized access denied for {}.'.format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def logged(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        logging.info(f'{func.__name__} from user {user_id}')
        return func(update, context, *args, **kwargs)

    return wrapped


def typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func
