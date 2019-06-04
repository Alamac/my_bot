from datetime import datetime, time
from glob import glob
import logging
from random import choice

import ephem

from utils import get_keyboard, get_user_emo, not_number_checker

def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет, {}! {}'.format(update.message.chat.username, emo)
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = 'Hi {} {}! You\'ve messaged to me: \"{}\"'.format(
                update.message.chat.first_name,
                emo,
                update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s",
                 update.message.chat.username,
                 update.message.chat.id,
                 update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def define_constellation(bot, update, user_data):
    PLANETS = ['Mercury', 'Venus', 'Mars', 'Earth',
               'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    try:
        planet_name = update.message.text.split()[1].lower().capitalize()

    except TypeError:
        update.message.reply_text(
            'Please enter the planet name in English', reply_markup=get_keyboard())

    if planet_name in PLANETS:
        current_datetime = time.strftime("%Y/%m/%d %H:%M", time.localtime())
        planet_info = getattr(ephem, planet_name)(current_datetime)
        constellation = ephem.constellation(planet_info)
        update.message.reply_text('{} сегодня в созведии {}'.format(
            planet_name, constellation[1]), reply_markup=get_keyboard())

    else:
        update.message.reply_text('{} не является планетой'.format(
            planet_name), reply_markup=get_keyboard())


def wordcount(bot, update, user_data):
    user_sentence = update.message.text.split()
    user_sentence.pop(0)
    length = len(user_sentence)
    reply = update.message.reply_text
    reply_string = 'В вашем предложении {} слова/слов'

    if length == 0:
        reply('Вы прислали пустую строку')

    elif length == 1:
        user_sentence_undercheck = user_sentence[0].split('_')
        user_sentence_minus = user_sentence[0].split('-')
        user_sentence_dot = user_sentence[0].split('.')

        if len(user_sentence_undercheck) > 1 and not_number_checker(user_sentence_undercheck):
            reply(reply_string.format(len(user_sentence_undercheck)),
                  reply_markup=get_keyboard())

        # тут используется сравнение с двойкой, чтобы учесть слова с дефисом
        elif len(user_sentence_minus) > 2 and not_number_checker(user_sentence_minus):
            reply(reply_string.format(len(user_sentence_minus)),
                  reply_markup=get_keyboard())

        elif len(user_sentence_dot) > 2 and not_number_checker(user_sentence_dot):
            reply(reply_string.format(len(user_sentence_dot)),
                  reply_markup=get_keyboard())

        elif not_number_checker(user_sentence):
            reply('В вашем предложении 1 слово', reply_markup=get_keyboard())

        else:
            reply('Предложение не может состоять из одних цифр',
                  reply_markup=get_keyboard())

    elif length > 1 and not_number_checker(user_sentence):
        reply(reply_string.format(length), reply_markup=get_keyboard())

    elif not not_number_checker(user_sentence):
        reply('Предложение не может состоять из одних цифр',
              reply_markup=get_keyboard())


def next_full_moon(bot, update, user_data):
    reply = update.message.reply_text
    message_list = update.message.text.split()

    if len(message_list) > 1:
        date = message_list[1]
        format_date = ''
        try:
            format_date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            pass
        try:
            format_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            pass
        if format_date == '':
            reply('Введите дату в формате ГГГГ/ММ/ДД или ГГГГ-ММ-ДД',
                  reply_markup=get_keyboard())
        else:
            next_full_moon = ephem.next_full_moon(date)

    else:
        date = datetime.now()
        next_full_moon = ephem.next_full_moon(date)

    return reply('Следующее полнолуние будет {}'.format(next_full_moon), reply_markup=get_keyboard())


def cities(bot, update, user_data):

    user_cities_file = str(update.message.chat_id) + '_city.csv'
    last_reply_to_user_file = str(update.message.chat_id) + '_last_reply.txt'
    user_used_cities_file = str(update.message.chat_id) + '_used_cities.csv'
    user_city = update.message.text.split()[1].capitalize()

    try:
        with open(last_reply_to_user_file, 'r', encoding='utf-8') as last_reply:
            last_reply_to_user = last_reply.read()
            is_the_same_letter = user_city[0] == last_reply_to_user[-1].capitalize()

    except FileNotFoundError:
        last_reply_to_user = ''

    if last_reply_to_user != '':
        is_the_same_letter = user_city[0] == last_reply_to_user[-1].capitalize()
    else:
        is_the_same_letter = True

    try:
        with open(user_cities_file, 'r', encoding='utf-8') as user_city_file:
            cities = user_city_file.read().split('\n')
            if len(cities) == 0:
                with open('all_cities.csv', 'r', encoding='utf-8') as all_cities:
                    cities = all_cities.read().split('\n')

    except FileNotFoundError:
        with open('all_cities.csv', 'r', encoding='utf-8') as all_cities:
            cities = all_cities.read().split('\n')

    try:
        with open(user_used_cities_file, 'r', encoding='utf-8') as used_cities:
            used_cities = used_cities.read().split('\n')

    except FileNotFoundError:
        used_cities = []

    if not is_the_same_letter:
        update.message.reply_text('Нужно назвать город на {}!'.format(
            last_reply_to_user[-1].capitalize()), reply_markup=get_keyboard())

    else:
        if user_city in cities:
            last_digit = user_city[-1].upper()
            cities.remove(user_city)
            answer = [i for i in cities if i.startswith(last_digit)][0]
            cities.remove(answer)
            with open(last_reply_to_user_file, 'w', encoding='utf-8') as last_reply:
                last_reply.write(answer)
            city_string = '\n'.join(cities)
            with open(user_cities_file, 'w', encoding='utf-8') as user_city_file:
                user_city_file.write(city_string)
            with open(user_used_cities_file, 'a', encoding='utf-8') as used_cities:
                used_cities.write(answer + '\n' + user_city + '\n')
            update.message.reply_text(answer, reply_markup=get_keyboard())
        elif user_city in used_cities:
            update.message.reply_text(
                'Мы уже называли этот город!', reply_markup=get_keyboard())
        else:
            update.message.reply_text(
                'Нет такого города', reply_markup=get_keyboard())


def send_cat(bot, update, user_data):
    cat_list = glob('images/cats/*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(
        get_user_emo(user_data)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(
        get_user_emo(user_data)), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(
        emo), reply_markup=get_keyboard())

def get_info(bot, update, user_data):
    reply = """Данный бот поддерживает следующие команды:
    /planet \"Имя планеты на английском языке\" - сообщает, в каком созвездии находится данная планета сегодня
    /wordcount \"Предложение\" - подсчитывает количество слов в приложении
    /next_full_moon - сообщает дату следующего полнолуния от указанной даты
    /cities - играет с пользователем в города"""
    update.message.reply_text(reply, reply_markup=get_keyboard())
