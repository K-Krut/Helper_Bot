import asyncio

import Finances
import exceptions
from imports import *


@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    await bot.send_message(
        message.from_user.id, f"👤*Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                              f"{message.from_user.last_name if message.from_user.last_name else ''}\n "
                              f"I'm bot Student Assistant.*", parse_mode="Markdown",
        reply_markup=markup.inline_keyboard_menu
    )


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
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, f"👤*Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                           f"{call.from_user.last_name if call.from_user.last_name else ''}\n "
                           f"I'm bot Student Assistant.*", parse_mode="Markdown",
        reply_markup=markup.inline_keyboard_menu
    )


@dp.callback_query_handler(text="BACK_TO_FINANCE")
async def back(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
        reply_markup=markup.inline_keyboard_finance_menu
    )


""" Finance handlers  """


@dp.callback_query_handler(text='💰Finance💰')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_finance_menu)


@dp.callback_query_handler(text='🏛️Budget🏛️')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, f'<b>Your budget</b>:\n<b>Daily</b>: {Finances.get_budget_daily_limit()}\n'
                           f'<b>Month</b>: {Finances.get_budget_month_limit()}', parse_mode='HTML',
        reply_markup=markup.inline_keyboard_budget_menu
    )


@dp.callback_query_handler(text='📈Statistic📈')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_statistic_menu)


@dp.callback_query_handler(text='➕Add category➕')
async def add_category(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, "Enter category and key words like this:\n"
                           "<b>products: products, food, eating</b>", parse_mode="HTML"
    )

    @dp.message_handler()
    async def creating_finance_category(message: types.Message):
        try:
            Finances.create_category_finance(message['text'])
        except exceptions.AddCategoryError as exp:
            await message.answer(str(exp))
            return
        await asyncio.sleep(20)
        return
    await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
                           reply_markup=markup.inline_keyboard_finance_menu)
########################################################################################################################
# после добавления идет время и выводит меню, но работа функции не прекращаеться


@dp.callback_query_handler(text='💸Add expense💸')
async def add_expense_(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def adding_expense(message: types.Message):
        try:
            expense_ = Finances.add_expense(message['text'])
        except exceptions.AddExpenseError as exp:
            await message.answer(str(exp))
        await asyncio.sleep(20)
        await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
                               reply_markup=markup.inline_keyboard_finance_menu)


@dp.callback_query_handler(text='💰Add incomes💰')
async def add_incomes(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def adding_incomes(message: types.Message):
        try:
            income_ = Finances.add_incomes(message['text'])
        except exceptions.AddIncomeError as exp:
            await message.answer(str(exp))\



@dp.callback_query_handler(text='🖊️Edit budget🖊️')
async def edit_budget(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def editing_budget(message: types.Message):
        try:
            print(message['text'])
            Finances.edit_budget(message['text'])
        except exceptions.AddIncomeError as exp:
            await message.answer(str(exp))


    # await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
    #                        reply_markup=markup.inline_keyboard_finance_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
