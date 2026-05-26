import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Константы
TOKEN = '7768287450:ВАШ_ТОКЕН'  # Вставьте ваш полный токен
API_KEY = '858a128c50a7c9352cb227e05fca832b'
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

# Словарь с emoji для разных кодов погоды
EMOJI_CODE = {
    200: '⛈️', 201: '⛈️', 202: '⛈️',  # Гроза
    210: '🌩️', 211: '🌩️', 212: '🌩️', 221: '🌩️',
    230: '⛈️', 231: '⛈️', 232: '⛈️',
    300: '🌧️', 301: '🌧️', 302: '🌧️',  # Морось
    310: '🌧️', 311: '🌧️', 312: '🌧️', 313: '🌧️', 314: '🌧️', 321: '🌧️',
    500: '🌧️', 501: '🌧️', 502: '🌧️', 503: '🌧️', 504: '🌧️',  # Дождь
    511: '🌧️❄️', 520: '🌧️', 521: '🌧️', 522: '🌧️', 531: '🌧️',
    600: '❄️', 601: '❄️', 602: '❄️',  # Снег
    611: '🌨️', 612: '🌨️', 613: '🌨️', 615: '🌨️', 616: '🌨️',
    620: '🌨️', 621: '🌨️', 622: '🌨️',
    701: '🌫️', 711: '🔥', 721: '🌫️', 731: '🏜️', 741: '🌫️',  # Туман
    751: '🏜️', 761: '🏜️', 762: '🌋', 771: '💨', 781: '🌪️',
    800: '☀️',  # Ясноо
    801: '🌤️',  # Малооблачно
    802: '⛅',  # Облачно
    803: '☁️',  # Пасмурно
    804: '☁️'  # Пасмурно
}

bot = telebot.TeleBot(TOKEN)

# Создаём клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_about = KeyboardButton('О проекте')
button_location = KeyboardButton('Отправить геопозицию', request_location=True)
keyboard.add(button_about, button_location)


def get_weather(lat, lon):
    """Запрос к API и возврат строки с ответом."""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    response = requests.get(URL_WEATHER_API, params=params).json()

    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']

    emoji = EMOJI_CODE.get(code, '🌡️')  # если код не найден, показываем градусник

    message = f'Погода в: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'Температура {temp}°C.\n'
    message += f'Ощущается {temp_feels_like}°C.\n'
    message += f'Влажность {humidity}%.\n'

    return message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветственное сообщение."""
    bot.send_message(
        message.chat.id,
        '🌤️ Привет! Отправь геопозицию, чтобы узнать погоду.',
        reply_markup=keyboard
    )


@bot.message_handler(regexp='О проекте')
def send_about(message):
    """Сообщение о проекте."""
    bot.send_message(
        message.chat.id,
        'Погодный бот\n\nИспользует OpenWeatherMap API\nСоздан для показа текущей погоды по геопозиции.'
    )


@bot.message_handler(content_types=['location'])
def send_weather(message):
    """Извлечение координат и отправка ответа."""
    lon = message.location.longitude
    lat = message.location.latitude

    weather_message = get_weather(lat, lon)
    bot.send_message(message.chat.id, weather_message)


# Запуск бота
print('✅ Бот запущен...')
bot.infinity_polling()