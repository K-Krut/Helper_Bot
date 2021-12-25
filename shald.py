import json, re, time, datetime, bd
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.types.callback_query import CallbackQuery
from imports import *
from Bot_Assistant import *


class FSMBook(StatesGroup):
    write_search = State()
    write_delete = State()


@dp.message_handler(content_types=['text', 'document', 'audio', 'photo', 'sticker', 'video', 'voice', 'unknown'],
                    state=FSMBook.write_search)
async def search(message: types.Message, state: FSMContext):
    if message.text:
        info = bd.get_info(message.text)
        await state.finish()
        if info:
            if bd.add_book(info, message.from_user.id):
                await bot.send_message(message.chat.id, "Книга-" + info[0]['Название'] + '\nЗа авторством-' + info[0][
                    'Автор'] + '\nОт издания-' + info[0]['Издательство'] + '\nБыла добавлена в ваш список')
            else:
                await bot.send_message(message.chat.id, "Это произведение уже есть у вас ,или поиск выдал не книгу")
        else:
            await bot.send_message(message.chat.id, "Я не смог найти книгу по даному запросу")
    else:
        await bot.send_message(message.chat.id, "Введите пожалуйста текст")
        await message.delete()


@dp.message_handler(content_types=['text', 'document', 'audio', 'photo', 'sticker', 'video', 'voice', 'unknown'],
                    state=FSMBook.write_delete)
async def delete(message: types.Message, state: FSMContext):
    if message.text and not any((numb not in '1234567890') for numb in message.text):
        await state.finish()
        if bd.delete_book(int(message.text), message.from_user.id):
            await bot.send_message(message.chat.id, "Книга удалена")
        else:
            await bot.send_message(message.chat.id, "Я не смог найти книгу по даному запросу")
    else:
        await bot.send_message(message.chat.id, "Введите пожалуйста код")
        await message.delete()


@dp.callback_query_handler(text="library")
async def library(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, "Выбирайте,что именно вы хотите сделать с книжным списком желаний:",
                           reply_markup=lib)


@dp.callback_query_handler(text="add")
async def add_(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, "Напишите запрос,по которому я буду искать книгу:")
    await FSMBook.write_search.set()


@dp.callback_query_handler(text="full")
async def full_(call: CallbackQuery):
    delete = types.InlineKeyboardButton(text="Удалить книгу со списка", callback_data="delete")
    await bot.send_message(call.message.chat.id, "Список ваших интересов:\n" + bd.get_list(
        call.from_user.id) + '\nВведи код книги ,если хочешь убрать её',
                           reply_markup=InlineKeyboardMarkup(row_width=1).add(delete))


@dp.callback_query_handler(text="delete")
async def delete_(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, "Введи код книги для удаления:")
    await FSMBook.write_delete.set()


@dp.callback_query_handler(text="stats")
async def stats_(call: CallbackQuery):
    data = bd.get_max_info(call.from_user.id)
    await bot.send_message(call.message.chat.id, "Информация:\n" + '<><><><><><><><>\n'.join(
        '\n'.join(str(item) for item in group) for group in data.items()))


executor.start_polling(dp, skip_updates=True)
