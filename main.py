import pickle
from time import sleep

from AI import *
from information import *
from markups import *
from musics import *


dotenv.load_dotenv('.env')

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
print('Запустился')

dict_users = pickle.load(open('dict_users.txt', 'rb'))

def save_dict():
    pickle.dump(dict_users, open('dict_users.txt', 'wb'))

list_with_buttons = ['/start', 'Мой профиль 👤', 'Задать вопрос спорт-нейросети 🤖', 'Мой ИМТ 💪', 'Спорт в Сургуте 🏙️',
                     'Подобрать мне спорт 🔎', 'Музыка для тренировок ♫', 'Интересные факты о видах спорта 🤔', 'Мои достижения 🏆']

def edit_info(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=
    dict_users[message.from_user.first_name]['last_info'].message_id, text=send_profile(
        dict_users[message.from_user.first_name]['name'],
        dict_users[message.from_user.first_name]['age'],
        dict_users[message.from_user.first_name]['gender'],
        dict_users[message.from_user.first_name]['height'],
        dict_users[message.from_user.first_name]['weight'],
        dict_users[message.from_user.first_name]['goal']), parse_mode='markdown', reply_markup=change_info_markup)

def edit_info_callback(callback):
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=
    dict_users[callback.from_user.first_name]['last_info'].message_id, text=send_profile(
        dict_users[callback.from_user.first_name]['name'],
        dict_users[callback.from_user.first_name]['age'],
        dict_users[callback.from_user.first_name]['gender'],
        dict_users[callback.from_user.first_name]['height'],
        dict_users[callback.from_user.first_name]['weight'],
        dict_users[callback.from_user.first_name]['goal']), parse_mode='markdown', reply_markup=change_info_markup)


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
        dict_users[message.from_user.first_name]['last_message'] = message
        dict_users[message.from_user.first_name]['last_info'] = message.message_id
        dict_users[message.from_user.first_name]['achievements'] = []
        save_dict()
        bot.send_message(message.chat.id, introduction_message1, reply_markup=pluses_markup)
        sleep(0.5)
        bot.send_message(message.chat.id, '🚀 Давай начнем! Выбирай что тебя интересует на панели снизу и погнали!', reply_markup=setup_markup())
    else:
        bot.send_message(message.chat.id, hello_message, reply_markup=setup_markup())

    bot.register_next_step_handler(message, check_message)


def check_message(message):
    if message.text == '/start':
        start_message(message)

    elif message.text == 'Мой профиль 👤':
        dict_users[message.from_user.first_name]['last_info'] = bot.send_message(message.chat.id, send_profile(dict_users[message.from_user.first_name]['name'],
                                                       dict_users[message.from_user.first_name]['age'],
                                                       dict_users[message.from_user.first_name]['gender'],
                                                       dict_users[message.from_user.first_name]['height'],
                                                       dict_users[message.from_user.first_name]['weight'],
                                                       dict_users[message.from_user.first_name]['goal']), parse_mode='markdown', reply_markup=change_info_markup)
        bot.send_message(message.chat.id, 'Режим работы бота с помощью кнопок клавиатуры ниже ↘️', reply_markup=setup_markup())
        bot.register_next_step_handler(message, check_message)

    elif message.text == 'Задать вопрос спорт-нейросети 🤖':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, 'Придумай какое-нибудь небольшое приветствие с именем'), reply_markup=setup_markup())
        bot.register_next_step_handler(message, message_ai)

    elif message.text == 'Мой ИМТ 💪':
        if dict_users[message.from_user.first_name]['height'] != '(не указано)' and dict_users[message.from_user.first_name]['weight'] != '(не указано)':
            bmi = int(dict_users[message.from_user.first_name]['weight']) / (int(dict_users[message.from_user.first_name]['height']) / 100) ** 2
            answer = check_bmi(dict_users[message.from_user.first_name]['gender'], int(dict_users[message.from_user.first_name]['age']), int(dict_users[message.from_user.first_name]['height']), int(dict_users[message.from_user.first_name]['weight']))
            bot.send_message(message.chat.id, answer, parse_mode='markdown')
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, f'Оцени индекс массы тела и дай рекомендации: имт={bmi}, мой пол: {dict_users[message.from_user.first_name]['gender']}, мой возраст {dict_users[message.from_user.first_name]['age']}'), reply_markup=setup_markup())
        else:
            bot.send_message(message.chat.id, f'Для вычисление ИМТ пожалуйста, заполните данные в профиле', reply_markup=setup_markup())
        bot.register_next_step_handler(message, check_message)

    elif message.text == 'Спорт в Сургуте 🏙️':
        bot.send_message(message.chat.id, 'Какая категория спорта вас интересует?', reply_markup=category_markup)
        bot.send_message(message.chat.id, 'Режим работы бота с помощью кнопок клавиатуры ниже ↘️', reply_markup=setup_markup())
        bot.register_next_step_handler(message, check_message)

    elif message.text == 'Подобрать мне спорт 🔎':
        if dict_users[message.from_user.first_name]['height'] == '(не указано)' or \
            dict_users[message.from_user.first_name]['weight'] == '(не указано)' or \
            dict_users[message.from_user.first_name]['gender'] == '(не указано)' or \
            dict_users[message.from_user.first_name]['age'] == '(не указано)':
            bot.send_message(message.chat.id, 'Для подбор спорта, пожалуйста, заполните данные в профиле')
        else:
            mes = bot.send_message(message.chat.id, 'Перебираю всё исходя из ваших данных...')
            bot.send_chat_action(message.chat.id, 'typing')
            answer = ask_ai(message.from_user.first_name, f'Я тебе даю данные о пользователе и весь список секций спорта в Сургуте. Возраст пользователя: {dict_users[message.from_user.first_name]['age']}, вес: {dict_users[message.from_user.first_name]['weight']} кг, рост: {dict_users[message.from_user.first_name]['height']} см, пол: {dict_users[message.from_user.first_name]['gender']}. Исходя из эти данных подбери секции которые подходят этому человек из этого списка: {sport_in_surgut}. Если не будет ничего то либо чуть-чуть соври, либо выбери наиболее подходящее. Пиши просто название секции и почему она подходит, в конце добавь что в разделе "Спорт в Сургуте" вы можете записаться на тренировки и узнать подробную информацию. Пиши без приветствий, а просто типо: давай разберём всё что для тебя подходит. ПИШИ БЕЗ ФОРМАТИРОВАНИЕ ТЕКСТА ПРОСТО ОБЫЧНЫЙ ТЕКСТ')
            bot.delete_message(message.chat.id, mes.message_id)
            bot.send_message(message.chat.id, answer, reply_markup=setup_markup())
            bot.register_next_step_handler(message, check_message)

    elif message.text == 'Музыка для тренировок ♫':
        bot.send_message(message.chat.id, 'Выберите жанр:', reply_markup=music_markup)
        bot.register_next_step_handler(message, check_message)

    elif message.text == 'Интересные факты о видах спорта 🤔':
        bot.send_message(message.chat.id, 'Выберите вид спорта, о котором вы хотели бы узнать:', reply_markup=facts_markup)
        bot.register_next_step_handler(message, check_message)

    elif message.text == 'Мои достижения 🏆':
        bot.send_message(message.chat.id, 'Введите достижение, которого вы достигли:', reply_markup=achievement_markup)
        bot.register_next_step_handler(message, check_achievement)

    else:
        bot.send_message(message.chat.id, 'Извини, я не могу тебя понять, пожалуйста, выбери элемент из панели снизу', reply_markup=setup_markup())
        bot.register_next_step_handler(message, check_message)

def check_achievement(message):
    if message.text in list_with_buttons:
        check_message(message)
        return
    dict_users[message.from_user.first_name]['achievements'].append(message.text)
    bot.send_message(message.chat.id, 'Достижение добавлено✅, а сейчас его оценит наш эксперт')
    save_dict()
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, f'Оцени достижение и дай рекомендации, моё достижение: {message.text}, мой возраст: {dict_users[message.from_user.first_name]['age']}, мой вес: {dict_users[message.from_user.first_name]['weight']} кг, мой рост: {dict_users[message.from_user.first_name]['height']} см, мой пол: {dict_users[message.from_user.first_name]['gender']}'))
    bot.register_next_step_handler(message, check_message)

def message_ai(message):
    if message.text in list_with_buttons:
        check_message(message)
    else:
        mes = bot.send_message(message.chat.id, 'Усердно думаю над ответом...📝')
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ask_ai(message.from_user.first_name, message.text + f" мой возраст: {dict_users[message.from_user.first_name]['age']}, мой вес: {dict_users[message.from_user.first_name]['weight']} кг, мой рост: {dict_users[message.from_user.first_name]['height']} см, мой пол: {dict_users[message.from_user.first_name]['gender']}")
        bot.delete_message(message.chat.id, mes.message_id)
        bot.send_message(message.chat.id, answer)
        bot.register_next_step_handler(message, message_ai)


@bot.message_handler(content_types=['text'])
def check_messages(message):
    if message.text in list_with_buttons:
        check_message(message)

@bot.callback_query_handler(func=lambda callback: True)
def check_call_data(callback):
    # Сообщение с изменением информации
    if callback.data == 'info':
        bot.send_message(callback.message.chat.id, 'Выберите, что хотите изменить:', reply_markup=information_markup)
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)

    # Изменение информации о пользователе
    if callback.data == 'age':
        dict_users[callback.from_user.first_name]['last_message'] = bot.send_message(callback.message.chat.id, 'Введите ваш возраст:')
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        bot.register_next_step_handler(callback.message, check_age)
    elif callback.data == 'gender':
        dict_users[callback.from_user.first_name]['last_message'] = bot.send_message(callback.message.chat.id, 'Укажите ваш пол:', reply_markup=gender_markup)
    elif callback.data == 'height':
        dict_users[callback.from_user.first_name]['last_message'] = bot.send_message(callback.message.chat.id, 'Введите ваш рост:')
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        bot.register_next_step_handler(callback.message, check_height)
    elif callback.data == 'weight':
        dict_users[callback.from_user.first_name]['last_message'] = bot.send_message(callback.message.chat.id, 'Введите ваш вес:')
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        bot.register_next_step_handler(callback.message, check_weight)
    elif callback.data == 'goal':
        dict_users[callback.from_user.first_name]['last_message'] = bot.send_message(callback.message.chat.id, 'Какая у вас цель?')
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        bot.register_next_step_handler(callback.message, check_goal)

    # Выбор пола
    if callback.data == 'male':
        dict_users[callback.from_user.first_name]['gender'] = 'Мужской👨'
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        edit_info_callback(callback)
        save_dict()
        bot.send_message(callback.message.chat.id, 'Данные сохранены✅')
    if callback.data == 'female':
        dict_users[callback.from_user.first_name]['gender'] = 'Женский👩🏻'
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        edit_info_callback(callback)
        save_dict()
        bot.send_message(callback.message.chat.id, 'Данные сохранены✅')

    # Сообщение с плюсами здорового тела
    if callback.data == 'pluses':
        bot.send_message(callback.message.chat.id, introduction_message2, reply_markup=setup_markup())

    # Выбор категории спорта
    if callback.data == 'game':
        bot.send_message(callback.message.chat.id, 'Выберите тип спорта:', reply_markup=game_markup)
    elif callback.data == 'athletics':
        bot.send_message(callback.message.chat.id, 'Выберите тип спорта:', reply_markup=athletics_markup)
    elif callback.data == 'martial':
        bot.send_message(callback.message.chat.id, 'Выберите тип спорта:', reply_markup=martial_markup)
    elif callback.data == 'season':
        bot.send_message(callback.message.chat.id, 'Выберите тип спорта:', reply_markup=season_markup)
    elif callback.data == 'heavy':
        bot.send_message(callback.message.chat.id, 'Выберите тип спорта:', reply_markup=heavy_markup)

    # Отправка сообщений из категории игровые
    if callback.data == 'football':
        bot.send_message(callback.message.chat.id, football_info, parse_mode='markdown')
    elif callback.data == 'basketball':
        bot.send_message(callback.message.chat.id, basketball_info, parse_mode='markdown')
    elif callback.data == 'volleyball':
        bot.send_message(callback.message.chat.id, volleyball_info, parse_mode='markdown')
    elif callback.data == 'tennis':
        bot.send_message(callback.message.chat.id, tennis_info, parse_mode='markdown')
    elif callback.data == 'ice_hockey':
        bot.send_message(callback.message.chat.id, hockey_info, parse_mode='markdown')

    # Отправка сообщений из категории атлетика
    if callback.data == 'run':
        bot.send_message(callback.message.chat.id, running_info, parse_mode='markdown')
    elif callback.data == 'yoga':
        bot.send_message(callback.message.chat.id, yoga_info, parse_mode='markdown')
    elif callback.data == 'gymnastics':
        bot.send_message(callback.message.chat.id, gymnastics_info, parse_mode='markdown')
    elif callback.data == 'dances':
        bot.send_message(callback.message.chat.id, dance_info, parse_mode='markdown')

    # Отправка сообщений из категории боевые
    if callback.data == 'taekwondo':
        bot.send_message(callback.message.chat.id, taekwondo_info, parse_mode='markdown')
    elif callback.data == 'karate':
        bot.send_message(callback.message.chat.id, karate_info, parse_mode='markdown')
    elif callback.data == 'judo':
        bot.send_message(callback.message.chat.id, judo_info, parse_mode='markdown')
    elif callback.data == 'boxing':
        bot.send_message(callback.message.chat.id, muay_thai_info, parse_mode='markdown')

    # Отправка сообщений из категории сезонные
    if callback.data == 'ski':
        bot.send_message(callback.message.chat.id, ski_info, parse_mode='markdown')
    elif callback.data == 'snowboard':
        bot.send_message(callback.message.chat.id, snowboard_info, parse_mode='markdown')
    elif callback.data == 'bycycle':
        bot.send_message(callback.message.chat.id, cycling_info, parse_mode='markdown')

    # Отправка сообщений из категории тяжёлая атлетика
    if callback.data == 'powerlifting':
        bot.send_message(callback.message.chat.id, powerlifting_info, parse_mode='markdown')
    elif callback.data == 'heavy_athletics':
        pass
    elif callback.data == 'rocking_chair':
        bot.send_message(callback.message.chat.id, fitness_clubs_info, parse_mode='markdown')

    # Выбор музыки
    if callback.data == 'popular':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Вот топ-10 треков из жанра "Популярная музыка для тренировок"', reply_markup=popular_playlist)
        for music in send_popular_music():
            bot.send_audio(callback.message.chat.id, music)
    elif callback.data == 'crossfit':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Вот топ-10 треков из жанра "Crossfit"', reply_markup=crossfit_playlist)
        for music in send_crossfit_music():
            bot.send_audio(callback.message.chat.id, music)
    elif callback.data == 'yoga_music':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Вот топ-10 треков из жанра "Йога (спокойная)"', reply_markup=yoga_music_playlist)
        for music in send_yoga_music():
            bot.send_audio(callback.message.chat.id, music)
    elif callback.data == 'for_gym':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Вот топ-10 треков из жанра "Плейлист для спортзала"', reply_markup=for_gym_playlist)
        for music in send_gym_music():
            bot.send_audio(callback.message.chat.id, music)

    # Выбор фактов
    if callback.data == 'football_fact':
        bot.send_message(callback.message.chat.id, football_facts, parse_mode='markdown')
    elif callback.data == 'basketball_fact':
        bot.send_message(callback.message.chat.id, basketball_facts, parse_mode='markdown')
    elif callback.data == 'volleyball_fact':
        bot.send_message(callback.message.chat.id, volleyball_facts, parse_mode='markdown')
    elif callback.data == 'tennis_fact':
        bot.send_message(callback.message.chat.id, tennis_facts, parse_mode='markdown')
    elif callback.data == 'ice_hockey_fact':
        bot.send_message(callback.message.chat.id, hockey_facts, parse_mode='markdown')
    elif callback.data == 'taekwondo_fact':
        bot.send_message(callback.message.chat.id, taekwondo_facts, parse_mode='markdown')
    elif callback.data == 'karate_fact':
        bot.send_message(callback.message.chat.id, karate_facts, parse_mode='markdown')
    elif callback.data == 'ski_fact':
        bot.send_message(callback.message.chat.id, ski_facts, parse_mode='markdown')
    elif callback.data == 'snowboard_fact':
        bot.send_message(callback.message.chat.id, snowboard_facts, parse_mode='markdown')

    if callback.data == 'achievement':
        achievement_message = 'МОИ ДОСТИЖЕНИЯ 🏆\n\n'
        for i, achievement in enumerate(dict_users[callback.from_user.first_name]['achievements']):
            achievement_message += str(i + 1) + '. ' + achievement + '\n'
        bot.send_message(callback.message.chat.id, achievement_message)

def check_age(message):
    if message.text in list_with_buttons:
        check_message(message)
        return

    if message.text and message.text.isdigit():
        if 1 <= int(message.text) <= 125:
            dict_users[message.from_user.first_name]['age'] = message.text
            bot.delete_message(message.chat.id, dict_users[message.from_user.first_name]['last_message'].message_id)
            bot.delete_message(message.chat.id, message.message_id)
            edit_info(message)
            save_dict()
            bot.send_message(message.chat.id, 'Данные сохранены✅')
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
        if 20 <= int(message.text) <= 220:
            dict_users[message.from_user.first_name]['height'] = message.text
            bot.delete_message(message.chat.id, dict_users[message.from_user.first_name]['last_message'].message_id)
            bot.delete_message(message.chat.id, message.message_id)
            edit_info(message)
            save_dict()
            bot.send_message(message.chat.id, 'Данные сохранены✅')
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
            bot.delete_message(message.chat.id, dict_users[message.from_user.first_name]['last_message'].message_id)
            bot.delete_message(message.chat.id, message.message_id)
            edit_info(message)
            save_dict()
            bot.send_message(message.chat.id, 'Данные сохранены✅')
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
        bot.delete_message(message.chat.id, dict_users[message.from_user.first_name]['last_message'].message_id)
        bot.delete_message(message.chat.id, message.message_id)
        mes = bot.send_message(message.chat.id, 'Оцениваю вашу цель...📝')
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, ask_ai(message.from_user.first_name, f'Оцени мою цель: {message.text}'))
        bot.delete_message(message.chat.id, mes.message_id)
        edit_info(message)
        dict_users[message.from_user.first_name]['goal'] = message.text
        save_dict()
        bot.send_message(message.chat.id, 'Данные сохранены✅')
        bot.register_next_step_handler(message, check_message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите цель')
        bot.register_next_step_handler(message, check_goal)


if __name__ == '__main__':
    bot.infinity_polling()