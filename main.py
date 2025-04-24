import telebot
import pickle
from time import sleep

from AI import *
from information import *


API = '7584710593:AAHz-j_wQPtoYKpnwztoknFuZTom4jVqF_A'
bot = telebot.TeleBot(API)
print('Запустился')

dict_users = pickle.load(open('dict_users.txt', 'rb'))


def save_dict():
    pickle.dump(dict_users, open('dict_users.txt', 'wb'))


markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
profile_btn = telebot.types.KeyboardButton(text='Мой профиль👤')
ai_btn = telebot.types.KeyboardButton(text='Задать вопрос спорт-нейросети🤖')
imt_btn = telebot.types.KeyboardButton(text='Мой ИМТ💪')
sport_btn = telebot.types.KeyboardButton(text='Спорт в Сургуте🏙️')
my_sport = telebot.types.KeyboardButton(text='Подобрать мне спорт🔎')
markup.add(profile_btn, imt_btn)
markup.add(sport_btn, my_sport)
markup.add(ai_btn)

information_markup = telebot.types.InlineKeyboardMarkup()
age_btn = telebot.types.InlineKeyboardButton(text='Изменить возраст', callback_data='age')
gender_btn = telebot.types.InlineKeyboardButton(text='Указать пол', callback_data='gender')
height_btn = telebot.types.InlineKeyboardButton(text='Изменить рост', callback_data='height')
weight_btn = telebot.types.InlineKeyboardButton(text='Изменить вес', callback_data='weight')
goal_btn = telebot.types.InlineKeyboardButton(text='Поставить цель', callback_data='goal')
information_markup.add(age_btn, gender_btn)
information_markup.add(height_btn, weight_btn)
information_markup.add(goal_btn)

gender_markup = telebot.types.InlineKeyboardMarkup()
male = telebot.types.InlineKeyboardButton(text='Мужской👨', callback_data='male')
female = telebot.types.InlineKeyboardButton(text='Женский👩🏻', callback_data='female')
gender_markup.add(male, female)

pluses_markup = telebot.types.InlineKeyboardMarkup()
btn = telebot.types.InlineKeyboardButton(text='Каковы плюсы хорошего телосложения?', callback_data='pluses')
pluses_markup.add(btn)

change_info_markup = telebot.types.InlineKeyboardMarkup()
change_info_markup_btn = telebot.types.InlineKeyboardButton(text='Изменить данные📋', callback_data='info')
change_info_markup.add(change_info_markup_btn)

category_markup = telebot.types.InlineKeyboardMarkup()
game = telebot.types.InlineKeyboardButton(text='Игровые виды спорта', callback_data='game')
martial = telebot.types.InlineKeyboardButton(text='Боевые искусства', callback_data='martial')
athletics = telebot.types.InlineKeyboardButton(text='Лёгкая атлетика', callback_data='athletics')
season = telebot.types.InlineKeyboardButton(text='Сезонные виды спорта', callback_data='season')
heavy = telebot.types.InlineKeyboardButton(text='Тяжёлые виды спорта', callback_data='heavy')
category_markup.add(game)
category_markup.add(athletics)
category_markup.add(martial)
category_markup.add(season)
category_markup.add(heavy)

list_with_buttons = ['/start', 'Мой профиль👤', 'Задать вопрос спорт-нейросети🤖',
                     'Мой ИМТ💪', 'Спорт в Сургуте🏙️', 'Подобрать мне спорт🔎']

@bot.message_handler(commands=['start'], content_types=['text'])
def start_message(message):
    if message.from_user.first_name not in dict_users:
        dict_users[message.from_user.first_name] = {}
        dict_users[message.from_user.first_name]['name'] = message.from_user.first_name
        dict_users[message.from_user.first_name]['age'] = '(не указано)'
        dict_users[message.from_user.first_name]['gender'] = '(не указано)'
        dict_users[message.from_user.first_name]['height'] = '(не указано)'
        dict_users[message.from_user.first_name]['weight'] = '(не указано)'
        dict_users[message.from_user.first_name]['goal'] = '(не указано)'
        bot.send_message(message.chat.id, introduction_message1, reply_markup=pluses_markup)
        sleep(.5)
        bot.send_message(message.chat.id, '🚀 Давай начнем! Выбирай что тебя интересует на панели снизу и погнали!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, hello_message, reply_markup=markup)

    bot.register_next_step_handler(message, check_message)


def check_message(message):
    if message.text == '/start':
        start_message(message)
    elif message.text == 'Мой профиль👤':
        bot.send_message(message.chat.id, send_profile(dict_users[message.from_user.first_name]['name'],
                                                       dict_users[message.from_user.first_name]['age'],
                                                       dict_users[message.from_user.first_name]['gender'],
                                                       dict_users[message.from_user.first_name]['height'],
                                                       dict_users[message.from_user.first_name]['weight'],
                                                       dict_users[message.from_user.first_name]['goal']), parse_mode='markdown', reply_markup=change_info_markup)

        bot.register_next_step_handler(message, check_message)
    elif message.text == 'Задать вопрос спорт-нейросети🤖':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, 'Придумай какое-нибудь небольшое приветствие с именем'))
        bot.register_next_step_handler(message, message_ai)
    elif message.text == 'Проверить мой ИМТ':
        if dict_users[message.from_user.first_name]['height'] != '(не указано)' and dict_users[message.from_user.first_name]['weight'] != '(не указано)':
            IMT = int(dict_users[message.from_user.first_name]['weight']) / (int(dict_users[message.from_user.first_name]['height']) / 100) ** 2
            answer = check_IMT(IMT).lower()
            bot.send_message(message.chat.id, f'Ваш ИМТ равен: *{round(IMT, 2)}*\n\nДанное значение ИМТ соответствует: *{answer}*\n\nА также сейчас ваш ИМТ оценит наш эксперт', parse_mode='markdown')
            bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, f'Оцени индекс массы тела и дай рекомендации: имт={IMT}'))
        else:
            bot.send_message(message.chat.id, f'Для вычисление ИМТ пожалуйста, заполните данные в профиле')
        bot.register_next_step_handler(message, check_message)
    elif message.text == 'Спорт в Сургуте🏙️':
        bot.send_message(message.chat.id, 'Какая категория спорта вас интересует?', reply_markup=category_markup)

def message_ai(message):
    if message.text in list_with_buttons:
        check_message(message)
    else:
        mes = bot.send_message(message.chat.id, 'Усердно думаю над ответом...📝')
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ask_ai(message.from_user.first_name, message.text)
        bot.delete_message(message.chat.id, mes.message_id)
        bot.send_message(message.chat.id, answer)
        bot.register_next_step_handler(message, message_ai)


@bot.callback_query_handler(func=lambda callback: True)
def check_call_data(callback):
    if callback.data == 'age':
        bot.send_message(callback.message.chat.id, 'Введите ваш возраст:')
        bot.register_next_step_handler(callback.message, check_age)
    if callback.data == 'gender':
        bot.send_message(callback.message.chat.id, 'Укажите ваш пол:', reply_markup=gender_markup)
    if callback.data == 'height':
        bot.send_message(callback.message.chat.id, 'Введите ваш рост:')
        bot.register_next_step_handler(callback.message, check_height)
    if callback.data == 'weight':
        bot.send_message(callback.message.chat.id, 'Введите ваш вес:')
        bot.register_next_step_handler(callback.message, check_weight)
    if callback.data == 'goal':
        bot.send_message(callback.message.chat.id, 'Какая у вас цель?')
        bot.register_next_step_handler(callback.message, check_goal)

    if callback.data == 'male':
        dict_users[callback.from_user.first_name]['gender'] = 'Мужской👨'
        bot.send_message(callback.message.chat.id, 'Данные обновлены')
    if callback.data == 'female':
        dict_users[callback.from_user.first_name]['gender'] = 'Женский👩🏻'
        bot.send_message(callback.message.chat.id, 'Данные обновлены')

    if callback.data == 'pluses':
        bot.send_message(callback.message.chat.id, introduction_message2, reply_markup=markup)

    if callback.data == 'info':
        bot.send_message(callback.message.chat.id, 'Выберите, что хотите изменить:', reply_markup=information_markup)

def check_age(message):
    if message.text in list_with_buttons:
        check_message(message)
        return
    if message.text and message.text.isdigit():
        if 1 <= int(message.text) <= 125:
            dict_users[message.from_user.first_name]['age'] = message.text
            bot.send_message(message.chat.id, 'Данные обновлены')
            bot.register_next_step_handler(message, check_message)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите свой настоящий возраст, это важно т. к. мы будем присылать вам рекомендации')
            bot.register_next_step_handler(message, check_age)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числом')
        bot.register_next_step_handler(message, check_age)


def check_height(message):
    if message.text in list_with_buttons:
        check_message(message)
        return
    if message.text and message.text.isdigit():
        if 1 <= int(message.text) <= 220:
            dict_users[message.from_user.first_name]['height'] = message.text
            bot.send_message(message.chat.id, 'Данные обновлены')
            bot.register_next_step_handler(message, check_message)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите свой настоящий рост, это важно т. к. мы будем присылать вам рекомендации')
            bot.register_next_step_handler(message, check_height)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числом')
        bot.register_next_step_handler(message, check_height)


def check_weight(message):
    if message.text in list_with_buttons:
        check_message(message)
        return
    if message.text and message.text.isdigit():
        if 5 <= int(message.text) <= 350:
            dict_users[message.from_user.first_name]['weight'] = message.text
            bot.send_message(message.chat.id, 'Данные обновлены')
            bot.register_next_step_handler(message, check_message)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите свой настоящий вес, это важно т. к. мы будем присылать вам рекомендации')
            bot.register_next_step_handler(message, check_weight)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числом')
        bot.register_next_step_handler(message, check_weight)


def check_goal(message):
    if message.text in list_with_buttons:
        check_message(message)
        return
    if message.text:
        bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, f'Оцени мою цель: {message.text}'))
        dict_users[message.from_user.first_name]['goal'] = message.text
        bot.send_message(message.chat.id, 'Данные обновлены')
        bot.register_next_step_handler(message, check_message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите цель')
        bot.register_next_step_handler(message, check_goal)

bot.infinity_polling()