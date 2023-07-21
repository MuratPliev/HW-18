# extensions.py

import requests


class APIException(Exception):
    def __init__(self, message):
        self.message = message


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float, api_key: str) -> float:
        if base == quote:
            raise APIException("Вы запросили конвертацию валюты самой в себя.")

        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)
        except ValueError:
            raise APIException("Неверно введено число.")

        url = f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "Response" in data:
            raise APIException("Ошибка при получении данных о курсе валют.")

        if quote not in data:
            raise APIException("Для данной валюты нет курса на данный момент.")

        rate = data[quote]
        result = amount * rate
        return result
