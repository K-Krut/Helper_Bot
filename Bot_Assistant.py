import config
import logging
from aiogram import Bot, Dispatcher, executor, types
import markup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
 
 
@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"👤*Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                           f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
                           f"bot Student Assistant.*", parse_mode="Markdown", reply_markup=markup.inline_keyboard_menu)
 
 
@dp.callback_query_handler(text="📝Notes📝")
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_note_menu)
 
 
@dp.callback_query_handler(text="➕Add note➕")
async def add_note(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*📝Enter theme of note📝*", parse_mode="Markdown")
 
    @dp.message_handler()
    async def add_theme(message: types.Message):
        await bot.send_message(message.from_user.id, f"*{message.text}*", parse_mode="Markdown")
 
 
 
 
@dp.callback_query_handler(text="📅Schedule📅")
async def schedule_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_schedule_menu)
 
 
@dp.callback_query_handler(text="🔧Settings🔧")
async def schedule_settings(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, f"*Current settings*:\nGroup: \nNotification: ", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_schedule_settings)
 
 
@dp.callback_query_handler(text="🔙")
async def back(call: types.CallbackQuery):
    """ back to main menu """
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           f"👤*Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                           f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                           f"bot Student Assistant.*", parse_mode="Markdown", reply_markup=markup.inline_keyboard_menu)
 
 
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)