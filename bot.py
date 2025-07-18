import telebot
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from psycopg2 import connect


bot = telebot.TeleBot('7602448230:AAF15Tx7YSYPdTy9imslbJ4y7c7sorJcqvw')   # токен бота

@bot.message_handler(commands=['start'])
def send_welcome(message):   # приветственное сообщение
    markup = telebot.types.InlineKeyboardMarkup()   # создание объекта разметки для inline-кнопок

    """Кнопка с url. переход из телеги в браузер на сайт:
    button = telebot.types.InlineKeyboardButton(text="Москва", url='https://www.gismeteo.ru/weather-moscow-4368/')"""

    button = telebot.types.InlineKeyboardButton(text="Москва", callback_data="москва")   # создание кнопки с идентификатором callback_data
    markup.row(button)   # ставит кнопку в ряд


    bot.send_message(
        chat_id=message.chat.id,
        text=(
            "Привет! Я Кондрачий бот прогноза погоды.\n"
            "Доступные города:\n"
            "Москва, Санкт-Петербург, Тверь,\n"
            "Екатеринбург, Владивосток, Дубна\n\n"
            "Введите город или нажмите кнопку ниже:"
        ),
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'москва')   # обработка клика на кнопку
def moscow_button_handler(call):
    try:
        bot.answer_callback_query(call.id)   # ответ на клик на кнопку (обязательный)
        class FakeMsg:   # создание фейкового сообщения в бот
            def __init__(self, text, chat_id):
                self.text = text
                self.chat = type('Chat', (), {'id': chat_id})()
                self.from_user = type('User', (), {'id': chat_id})()
        fk_mess = FakeMsg(text='москва', chat_id=call.message.chat.id)   # имитация фейкового сообщения в бот
        main(fk_mess)
        bot.delete_message(call.message.chat.id, call.message.message_id)   # удаление приветственного сообщения и кнопки
    except:
        print('Ошибка.')


"""Тестовая команда приветствия. Ввести в бот команду /testwelcome"""

# @bot.message_handler(commands=['testwelcome'])
# def test_welcome(message):
#     send_welcome(message)  # Вызов оригинальной функции
#     # bot.send_message(message.chat.id, "[Тест] Приветствие успешно вызвано!")

def data_time(soup):
    today = datetime.now().strftime("%d.%m.%Y")   # сегодняшняя дата
    time = soup.find('div', class_="day", attrs={"data-pattern": "G:i"})    # находим время на сайте
    return (f'Дата: {today}\n'
            f'Время: {time.text}')

def list_temperature(soup):    # находим данные о температурах на сайте и делам список
    list_temper = []
    """[текущая температура,
        по ощущению,
        сегодня min,
        сегодня max,
        завтра min,
        завтра max]"""
    qqq = soup.find_all('temperature-value')
    for i in qqq:
        try:
            list_temper.append(int(i['value']))
        except: break

    """Придумать правильное отображение вокруг 0 (- 2 0)"""

    return ('Сейчас: ' + ('+' if list_temper[0] > 0 else '-') + f'{list_temper[0]}°C\n'
            'По ощущению: ' + ('+' if list_temper[0] > 0 else '-') + f'{list_temper[1]}°C\n'
            'Сегодня: ' + ('+' if list_temper[0] > 0 else '-') + f'{list_temper[2]}+{list_temper[3]}°C\n'
            'Завтра: ' + ('+' if list_temper[0] > 0 else '-') + f'{list_temper[4]}+{list_temper[5]}°C\n')

def response_massage(soup):   # печать сообщения ответа
    return f'{data_time(soup)}\n{list_temperature(soup)}\nПо данным gismeteo'

def get_connection():   # коннект с БД

    return connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="12345"
    )

def execute_BD(city_name):   # запрос в БД
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, city FROM cities WHERE city_rus = %s", (city_name, ))
            result = cur.fetchone()

            return result

def link(city_name):   # создание ссылки на сайт для парсинга по данным из БД
    id, city = execute_BD(city_name)
    link =f'https://www.gismeteo.ru/weather-{city}-{id}/'
    return link

@bot.message_handler(content_types=['text'])
def main(message):
    # message.text = message.lower()
    city_name = message.text.lower()

    if execute_BD(city_name):

        # GISMETEO_TOKEN = "56b30cb255.3443075"
        weather_link = link(city_name)

        headers = {
        # "X-Gismeteo-Token": GISMETEO_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        response = requests.get(weather_link, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        bot.send_message(message.from_user.id, response_massage(soup))
        print(response_massage(soup))
    else:
        bot.send_message(message.from_user.id, 'Введите корректный город или команду /start')

bot.polling(none_stop=True, interval=0)

