import telebot

# Клавиатура снизу
def setup_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    profile_btn = telebot.types.KeyboardButton(text='Мой профиль👤')
    ai_btn = telebot.types.KeyboardButton(text='Задать вопрос спорт-нейросети🤖')
    imt_btn = telebot.types.KeyboardButton(text='Мой ИМТ💪')
    sport_btn = telebot.types.KeyboardButton(text='Спорт в Сургуте🏙️')
    my_sport = telebot.types.KeyboardButton(text='Подобрать мне спорт🔎')
    music = telebot.types.KeyboardButton(text='Музыка для тренировок♫')
    facts = telebot.types.KeyboardButton(text='Интересные факты о видах спорта🤔')
    markup.add(profile_btn, imt_btn)
    markup.add(sport_btn, my_sport)
    markup.add(facts, music)
    markup.add(ai_btn)
    return markup


# Кнопки, для изменения информации для человека
information_markup = telebot.types.InlineKeyboardMarkup()
age_btn = telebot.types.InlineKeyboardButton(text='Изменить возраст', callback_data='age')
gender_btn = telebot.types.InlineKeyboardButton(text='Указать пол', callback_data='gender')
height_btn = telebot.types.InlineKeyboardButton(text='Изменить рост', callback_data='height')
weight_btn = telebot.types.InlineKeyboardButton(text='Изменить вес', callback_data='weight')
goal_btn = telebot.types.InlineKeyboardButton(text='Поставить цель', callback_data='goal')
information_markup.add(age_btn, gender_btn)
information_markup.add(height_btn, weight_btn)
information_markup.add(goal_btn)


# Кнопки для изменения пола
gender_markup = telebot.types.InlineKeyboardMarkup()
male = telebot.types.InlineKeyboardButton(text='Мужской 👨', callback_data='male')
female = telebot.types.InlineKeyboardButton(text='Женский 👩🏻', callback_data='female')
gender_markup.add(male, female)


# Кнопка для сообщения с плюсами хорошего тела
pluses_markup = telebot.types.InlineKeyboardMarkup()
btn = telebot.types.InlineKeyboardButton(text='Каковы плюсы хорошего телосложения?', callback_data='pluses')
pluses_markup.add(btn)


# Кнопка для изменения данных о пользователе
change_info_markup = telebot.types.InlineKeyboardMarkup()
change_info_markup_btn = telebot.types.InlineKeyboardButton(text='Изменить данные 📋', callback_data='info')
change_info_markup.add(change_info_markup_btn)


# Кнопки с категориями
category_markup = telebot.types.InlineKeyboardMarkup()
game = telebot.types.InlineKeyboardButton(text='⚽ Игровые виды спорта 🏀', callback_data='game')
athletics = telebot.types.InlineKeyboardButton(text='🏃 Лёгкая атлетика 🔥', callback_data='athletics')
martial = telebot.types.InlineKeyboardButton(text='🥋 Боевые искусства 🥊', callback_data='martial')
season = telebot.types.InlineKeyboardButton(text='⛷️ Сезонные виды спорта 🌞', callback_data='season')
heavy = telebot.types.InlineKeyboardButton(text='🏋️ Тяжёлые виды спорта 💪', callback_data='heavy')
category_markup.add(game)
category_markup.add(athletics)
category_markup.add(martial)
category_markup.add(season)
category_markup.add(heavy)


# Кнопки с типами спортов для категории игры
game_markup = telebot.types.InlineKeyboardMarkup()
football = telebot.types.InlineKeyboardButton(text='Футбол ⚽', callback_data='football')
basketball = telebot.types.InlineKeyboardButton(text='Баскетбол 🏀', callback_data='basketball')
volleyball = telebot.types.InlineKeyboardButton(text='Волейбол 🏐', callback_data='volleyball')
tennis = telebot.types.InlineKeyboardButton(text='Теннис 🎾', callback_data='tennis')
ice_hockey = telebot.types.InlineKeyboardButton(text='Хоккей 🏒', callback_data='ice_hockey')
game_markup.add(football, basketball)
game_markup.add(volleyball, tennis)
game_markup.add(ice_hockey)


# Кнопки с типами спортов для категории атлетика
athletics_markup = telebot.types.InlineKeyboardMarkup()
run_walk = telebot.types.InlineKeyboardButton(text='Бег и ходьба', callback_data='run')
yoga = telebot.types.InlineKeyboardButton(text='Йога 🧘‍♂️', callback_data='yoga')
gymnastics = telebot.types.InlineKeyboardButton(text='Гимнастика и акробатика 🤸‍♀️', callback_data='gymnastics')
dances = telebot.types.InlineKeyboardButton(text='Танцы 💃', callback_data='dances')
athletics_markup.add(run_walk, yoga)
athletics_markup.add(gymnastics, dances)


# Кнопки с типами спортов для категории боевые
martial_markup = telebot.types.InlineKeyboardMarkup()
taekwondo = telebot.types.InlineKeyboardButton(text='Тхэквондо 👊', callback_data='taekwondo')
karate = telebot.types.InlineKeyboardButton(text='Карате Киокусинкай 🥋', callback_data='karate')
boxing = telebot.types.InlineKeyboardButton(text='Тайский бокс 🥊', callback_data='boxing')
martial_markup.add(taekwondo, karate)
martial_markup.add(boxing)


# Кнопки с типами спортов для категории сезонные
season_markup = telebot.types.InlineKeyboardMarkup()
ski = telebot.types.InlineKeyboardButton(text='Лыжи ⛷️', callback_data='ski')
snowboard = telebot.types.InlineKeyboardButton(text='Сноуборд 🏂', callback_data='snowboard')
bycycle = telebot.types.InlineKeyboardButton(text='Велоспорт 🚲', callback_data='bycycle')
season_markup.add(ice_hockey, snowboard)
season_markup.add(bycycle)


# Кнопки с типами спортов для категории тяжёлые
heavy_markup = telebot.types.InlineKeyboardMarkup()
powerlifting = telebot.types.InlineKeyboardButton(text='Пауэрлифтинг 💪️', callback_data='powerlifting')
rocking_chair = telebot.types.InlineKeyboardButton(text='Фитнес-залы', callback_data='rocking_chair')
heavy_athletics = telebot.types.InlineKeyboardButton(text='Тяжёлая атлетика 🏋️‍♂️', callback_data='heavy_athletics')
heavy_markup.add(powerlifting, heavy_athletics)
heavy_markup.add( rocking_chair)


# Кнопки для музыки
music_markup = telebot.types.InlineKeyboardMarkup()
popular = telebot.types.InlineKeyboardButton(text='Популярная музыка для тренировок', callback_data='popular')
crossfit = telebot.types.InlineKeyboardButton(text='CrossFit', callback_data='crossfit')
yoga_music = telebot.types.InlineKeyboardButton(text='Йога (спокойная)', callback_data='yoga_music')
for_gym = telebot.types.InlineKeyboardButton(text='Плейлист для спортзала', callback_data='for_gym')
music_markup.add(popular)
music_markup.add(crossfit, yoga_music)
music_markup.add(for_gym)


# Ссылки на плейлисты
popular_playlist = telebot.types.InlineKeyboardMarkup()
popular_playlist.add(telebot.types.InlineKeyboardButton(text='Ссылка на плейлист', url='https://music.yandex.ru/playlists/c233d83c-4b23-a1cd-f02e-71ad9f141276'))

crossfit_playlist = telebot.types.InlineKeyboardMarkup()
crossfit_playlist.add(telebot.types.InlineKeyboardButton(text='Ссылка на плейлист', url='https://music.yandex.ru/playlists/19d96e3e-3a55-ffc4-334e-f16c0c0bc032'))

yoga_music_playlist = telebot.types.InlineKeyboardMarkup()
yoga_music_playlist.add(telebot.types.InlineKeyboardButton(text='Ссылка на плейлист', url='https://music.yandex.ru/playlists/8454a57c-03e6-b417-8ce4-1e90b90da2a5'))

for_gym_playlist = telebot.types.InlineKeyboardMarkup()
for_gym_playlist.add(telebot.types.InlineKeyboardButton(text='Ссылка на плейлист', url='https://music.yandex.ru/playlists/d4f2a00a-b2b1-fc4f-12be-a951f743eb90'))


# Кнопки для интересных фактах
facts_markup = telebot.types.InlineKeyboardMarkup()
football_fact = telebot.types.InlineKeyboardButton(text='Футбол ⚽', callback_data='football_fact')
basketball_fact = telebot.types.InlineKeyboardButton(text='Баскетбол 🏀', callback_data='basketball_fact')
volleyball_fact = telebot.types.InlineKeyboardButton(text='Волейбол 🏐', callback_data='volleyball_fact')
tennis_fact = telebot.types.InlineKeyboardButton(text='Теннис 🎾', callback_data='tennis_fact')
ice_hockey_fact = telebot.types.InlineKeyboardButton(text='Хоккей 🏒', callback_data='ice_hockey_fact')
taekwondo_fact = telebot.types.InlineKeyboardButton(text='Тхэквондо 👊', callback_data='taekwondo_fact')
karate_fact = telebot.types.InlineKeyboardButton(text='Карате 🥋', callback_data='karate_fact')
ski_fact = telebot.types.InlineKeyboardButton(text='Лыжи ⛷️', callback_data='ski_fact')
snowboard_fact = telebot.types.InlineKeyboardButton(text='Сноуборд 🏂', callback_data='snowboard_fact')
for fact in [football_fact, basketball_fact, volleyball_fact, tennis_fact, ice_hockey_fact, taekwondo_fact, karate_fact, ski_fact, snowboard_fact]:
    facts_markup.add(fact)