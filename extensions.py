import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'введены одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'нет валюты в списке существующих {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'нет валюты в списке существующих {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'сумма должна быть в цифрах {amount}')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        
        return total_base