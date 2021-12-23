# import requests
# from bs4 import BeautifulSoup
# from imports import *
# import databases as db
#
#
# class CurrencyData(NamedTuple):
#     id_: Optional[int]
#     code_name_: str
#     amount_: Optional[int]
#     name_: str
#     rate_: float
#
#
# url = 'https://bank.gov.ua/ua/markets/exchangerates?date=22.12.2021&period=daily'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, features="html.parser")
#
#
# def processing(el):
#     res_ = re.sub(r"\s+", " ", el[1:-1]).replace(',', '.').split(' ')
#     return CurrencyData(id_=int(res_[0]), code_name_=res_[1], amount_=int(res_[2]),
#                         name_=' '.join(i for i in res_[3: -1]), rate_=float(res_[-1:][0]))
#
#
# def get_exchange_info():
#     for i in soup.find('table', id='exchangeRates').find_all('tbody'):
#         return [processing(j.text) for j in i.find_all('tr')]
#
#
# def inserting_exchange_data(arr):
#     for i in arr:
#         db.insert(
#             "currency",
#             {
#                 "currency_id": i.id_,
#                 "currency_code": i.code_name_,
#                 "number_of_units": i.amount_,
#                 "currency_name": i.name_,
#                 "exchange_rate": i.rate_
#             }
#         )
#
#
# def get_all_exchange_data():
#     with connection.cursor() as cursor:
#         cursor.execute(f'SELECT currency_code, currency_name, exchange_rate FROM currency ')
#         rows = cursor.fetchall()
#     return [CurrencyData(id_=None, code_name_=row[0], amount_=None, name_=row[1], rate_=row[2]) for row in rows]
#
#
# def getting_rate(code_: str):
#     """
#
#     :rtype: object
#     """
#     with connection.cursor() as cursor:
#         cursor.execute(f'SELECT exchange_rate FROM currency WHERE currency_code = %s', (code_,))
#         rate_ = cursor.fetchone()
#     return rate_[0]
#
#
# def calculating(amount, rate):
#     return round(amount * rate, 2)
#
#
# def calculating2(amount, rate):
#     return round(amount * 1 / rate, 2)
#
#
# """def getting_currency_codes():
#     with connection.cursor() as cursor:
#         cursor.execute(f'SELECT currency_code FROM currency')
#         rate_ = cursor.fetchall()
#     return [i[0] for i in rate_]
#
# def parse_exchange_message(message):
#     regexp = re.match(r"(([\d ]+) ([A-Z]{3}))|(([\d ]+)(.|,)([\d ]+) ([A-Z]{3}))", message)
#     print(regexp.group(3))
#     if not regexp or not regexp.group(0) or not any(i == str(regexp.group(3)) for i in currency_codes):
#         raise ValueError(str(message))
#     return regexp
# currency_codes = getting_currency_codes()"""
#
#
#
#
#
# @dp.callback_query_handler(text='SEE_CURRENCY')
# async def see_currencies(call: types.CallbackQuery):
#     data_ = Slava.get_all_exchange_data()
#     exchange_data = [f'{i.code_name_} --> {i.rate_}' for i in data_]
#     await bot.send_message(call.from_user.id, "\n".join(exchange_data), parse_mode='HTML')
#
#
# @dp.callback_query_handler(text='ANOTHER_TO_UAH')
# async def exchange_another_to_uah(call: types.CallbackQuery):
#     data_ = Slava.get_all_exchange_data()
#     exchange_data = [f'{i.code_name_} --> {i.rate_} — /exch_{i.code_name_}' for i in data_]
#     await bot.send_message(call.from_user.id, "\n".join(exchange_data), parse_mode='HTML')
#
#     @dp.message_handler(lambda message: message.text.startswith('/exch_'))
#     async def exchanging2(message: types.Message):
#         rate_ = Slava.getting_rate(message.text[6:])
#         print(message)
#
#         @dp.message_handler()
#         async def exchanging3(mes: types.Message):
#             print(mes)
#             await bot.send_message(
#                 message.from_user.id, f'{mes.text} {message.text[6:]} --> {Slava.calculating(float(mes.text), rate_)} UAH',
#                 parse_mode='HTML', reply_markup=markup.inline_button_back_to_finance
#             )
#         return
#
#
# @dp.message_handler(lambda message: message.text.startswith('/exch__'))
# async def exchanging(message: types.Message):
#     # global rate_
#     # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
#     rate_ = Slava.getting_rate(message.text[7:])
#     print(message)
#
#     @dp.message_handler()
#     async def exchanging2(mes: types.Message):
#         print(mes.text)
#         await bot.send_message(
#             message.from_user.id, f'{mes.text} UAH --> {Slava.calculating2(float(mes.text), rate_)} '
#                                f'{message.text[7:]}', parse_mode='HTML',
#             reply_markup=markup.inline_button_back_to_finance
#         )
#     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
#
#
#
# @dp.callback_query_handler(text='UAH_TO_ANOTHER')
# async def exchange_uah_to_another(call: types.CallbackQuery):
#     data_ = Slava.get_all_exchange_data()
#     exchange_data = [f'{i.code_name_} --> {round(1 / i.rate_, 2)} — /exch__{i.code_name_}' for i in data_]
#     await bot.send_message(call.from_user.id, "\n".join(exchange_data), parse_mode='HTML')
#
#
#
#
#
#
#
#
#
# inline_button_see_categories = InlineKeyboardButton('My categories', callback_data='SEE_CATEGORIES')
# inline_button_see_currencies = InlineKeyboardButton('See currency', callback_data='SEE_CURRENCY')
# inline_button_exchange_another_to_uah = InlineKeyboardButton('TO UAH', callback_data='ANOTHER_TO_UAH')
# inline_button_exchange_uah_to_another = InlineKeyboardButton('FROM UAH', callback_data='UAH_TO_ANOTHER')
#
# k = inline_button_see_categories, inline_button_see_currencies, inline_button_exchange_uah_to_another, \
#     inline_button_exchange_another_to_uah,
# # print(getting_currency_codes())
# # parse_exchange_message('234 UAH')
