import telebot
from config import keys, TOKEN
from extensions import ConversionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)



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

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'для конвертации введите команду в следующем формате: \n<базовая валюта>\n<в какую валюту перевести>\n<сумма>\nсписок доступных валют: /values'
    bot.reply_to(message, text)
    
@bot.message_handler(commands=['values', 'help'])
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)


