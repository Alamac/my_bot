from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(
            choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def get_keyboard():

    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton(
        'Прислать геолокацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватарку', 'Инфо'],
        [contact_button, location_button]
    ], resize_keyboard=True)
    return my_keyboard


def not_number_checker(sentence):
    wordcount = 0
    intcount = 0
    for word in sentence:
        wordcount += 1
        try:
            int(word)
            intcount += 1
        except (ValueError, TypeError):
            pass
    if wordcount == intcount and wordcount > 0:
        return False
    else:
        return True