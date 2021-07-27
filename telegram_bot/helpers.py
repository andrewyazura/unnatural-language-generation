import yaml
from telegram import InlineKeyboardButton


def load_yaml(filename):
    with open(filename, 'r') as stream:
        file = yaml.safe_load(stream)
    return file


def generate_keyboard_layout(graphs, current, phrases, prefix):
    custom_keyboard = [
        [InlineKeyboardButton(name, callback_data='use.' + name)]
        for name in graphs
        if name != current
    ]

    if current:
        custom_keyboard.insert(
            0,
            [
                InlineKeyboardButton(
                    current + phrases['current'],
                    callback_data=prefix + current,
                )
            ],
        )
