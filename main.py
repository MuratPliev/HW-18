# main.py

import telebot
from extensions import CurrencyConverter, APIException

# Импортируем токен нашего Telegram-бота из файла config.py
from config import TELEGRAM_BOT_TOKEN

# Ваш API ключ от Cryptocompare
CRYPTOCOMPARE_API_KEY = 'e5697294bc29d839c0e9fdd4a2ed05059cbfc8a6480c91eaf9661e3405f8628d'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Для получения цены на валюту введите сообщение в формате:\n\n" \
                   "<имя валюты> <валюта, в которой хотите узнать цену первой валюты> <количество первой валюты>\n\n" \
                   "Например: USD EUR 100"
    bot.send_message(message.chat.id, instructions)


@bot.message_handler(commands=['values'])
def send_currency_values(message):
    values = "Доступные валюты: USD, EUR, RUB"
    bot.send_message(message.chat.id, values)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        user_input = message.text.split()
        if len(user_input) != 3:
            raise APIException("Неверный формат запроса. Введите три аргумента.")

        base_currency, quote_currency, amount = user_input
        result = CurrencyConverter.get_price(base_currency, quote_currency, amount, CRYPTOCOMPARE_API_KEY)
        response = f"{amount} {base_currency} = {result:.2f} {quote_currency}"
        bot.send_message(message.chat.id, response)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e.message}")


if __name__ == '__main__':
    bot.polling(none_stop=True)

