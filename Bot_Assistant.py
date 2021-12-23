import Finances
import Slava
import Statistic
import exceptions
from imports import *
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
import markup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Varta4899",
    db='finance'
)


class HandlerIncomes(StatesGroup):
    AddIncomesState = State()


class HandlerExpenses(StatesGroup):
    AddExpensesState = State()


class HandlerStatistic(StatesGroup):
    StatisticState = State()


class HandlerCategory(StatesGroup):
    CategoriesState = State()


class HandlerBudget(StatesGroup):
    BudgetState = State()


class HandlerOtherFinances(StatesGroup):
    OtherState = State()


@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    print(Finances.check_user_exists(str(message.from_user.id)))
    if not Finances.check_user_exists(str(message.from_user.id)):
        Finances.add_user(message['from'])
        Finances.set_default_budget(str(message.from_user.id))
    await bot.send_message(
        message.from_user.id, f"👤*Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                              f"{message.from_user.last_name if message.from_user.last_name else ''}\n "
                              f"I'm bot Student Assistant.*", parse_mode="HTML",
        reply_markup=markup.inline_keyboard_menu
    )

#
# @dp.callback_query_handler(text="📝Notes📝")
# async def note_menu(call: types.CallbackQuery):
#     await call.message.delete()
#     await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
#                            reply_markup=markup.inline_keyboard_note_menu)
#
#
# @dp.callback_query_handler(text="📅Schedule📅")
# async def schedule_menu(call: types.CallbackQuery):
#     await call.message.delete()
#     await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
#                            reply_markup=markup.inline_keyboard_schedule_menu)
#
#
# @dp.callback_query_handler(text="🔧Settings🔧")
# async def schedule_settings(call: types.CallbackQuery):
#     await call.message.delete()
#     await bot.send_message(call.from_user.id, f"<b>Current settings</b>:\nGroup: \nNotification: ", parse_mode="HTML",
#                            reply_markup=markup.inline_keyboard_schedule_settings)
#


@dp.callback_query_handler(text="🔙")
async def back(call: types.CallbackQuery):
    """ back to main menu """
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                           f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                           f"bot Student Assistant.</b>", parse_mode="HTML", reply_markup=markup.inline_keyboard_menu)


""" Finance handlers  """


@dp.callback_query_handler(text="BACK_TO_FINANCE")
async def back(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, "*Choose action to perform*", parse_mode="HTML",
        reply_markup=markup.inline_keyboard_finance_menu
    )


@dp.callback_query_handler(text='💰Finance💰')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_finance_menu)


@dp.callback_query_handler(text='🏛️Budget🏛️')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, f'<b>Your budget</b>:\n<b>Daily</b>: {Finances.get_budget_daily_limit(call.from_user.id)}\n'
                           f'<b>Month</b>: {Finances.get_budget_month_limit(call.from_user.id)}', parse_mode='HTML',
        reply_markup=markup.inline_keyboard_budget_menu
    )


@dp.callback_query_handler(text='📈Statistic📈')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_statistic_menu)


@dp.callback_query_handler(text='OTHER_FINANCE_MENU')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_other_menu)


@dp.callback_query_handler(text='💸Add expense💸')
async def add_expense_(call: types.CallbackQuery):
    await call.message.delete()
    await HandlerExpenses.AddExpensesState.set()

    @dp.message_handler(state=HandlerExpenses.AddExpensesState)
    async def adding_expense(message: types.Message):
        print(message)
        try:
            Finances.add_expense(message['text'], message.from_user.id)
        except exceptions.AddExpenseError as exp:
            await message.answer(str(exp))
        await HandlerExpenses.next()


@dp.callback_query_handler(text='💰Add incomes💰')
async def add_incomes(call: types.CallbackQuery):
    await call.message.delete()
    await HandlerIncomes.AddIncomesState.set()

    @dp.message_handler(state=HandlerIncomes.AddIncomesState)
    async def adding_incomes(message: types.Message):
        try:
            Finances.add_incomes(message['text'], message.from_user.id)
        except exceptions.AddIncomeError(str(message)) as exp:
            await message.answer(str(exp))
        await HandlerIncomes.next()


@dp.callback_query_handler(text='🖊️Edit budget🖊️')
async def edit_budget(call: types.CallbackQuery):
    await call.message.delete()
    await HandlerBudget.BudgetState.set()
    await bot.send_message(call.from_user.id, "daily <i>number</i> month <i>number</i>", parse_mode="HTML")

    @dp.message_handler(state=HandlerBudget.BudgetState)
    async def editing_budget(message: types.Message):
        try:
            Finances.edit_budget(message['text'], message.from_user.id)
        except exceptions.ChangeBudgetError(str(message)) as exp:
            await message.answer(str(exp))
        await HandlerBudget.next()


@dp.callback_query_handler(text='➕Add category➕')
async def add_category(call: types.CallbackQuery):
    await call.message.delete()
    await HandlerCategory.CategoriesState.set()
    await bot.send_message(
        call.from_user.id, "Enter category and key words like this:\n<b>products: products, food, eating</b>",
        parse_mode="HTML"
    )

    @dp.message_handler(state=HandlerCategory.CategoriesState)
    async def creating_finance_category(message: types.Message):
        try:
            Finances.create_category_finance(message['text'], message.from_user.id)
        except exceptions.AddCategoryError as exp:
            await message.answer(str(exp))
            await HandlerCategory.next()
        await bot.send_message(message.from_user.id, 'Edited', parse_mode='HTML')
        await HandlerCategory.next()


@dp.message_handler(lambda message: message.text.startswith('/delexp'))
async def del_expense(message: types.Message):
    try:
        Finances.delete_expense(int(message.text[7:]), message.from_user.id)
    except exceptions.DeleteError(str(message)) as exp:
        await bot.send_message(message.from_user.id, f'{exp}', parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Deleted', parse_mode='HTML')


@dp.message_handler(lambda message: message.text.startswith('/delinc'))
async def del_expense(message: types.Message):
    try:
        Finances.delete_expense(int(message.text[7:]), message.from_user.id)
    except exceptions.DeleteError(str(message)) as exp:
        await bot.send_message(message.from_user.id, f'{exp}', parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Deleted', parse_mode='HTML')


@dp.callback_query_handler(text='SEE_CATEGORIES')
async def categories_viewing_handler(call: types.CallbackQuery):
    await call.message.delete()
    categories_data = Finances.see_categories(call.from_user.id)
    if not categories_data:
        await bot.send_message(call.from_user.id, 'You haven`t any category yet', parse_mode='HTML')
        return
    categories_ = [f'<b>{category.name_}:</b>    {category.category_text}' for category in categories_data]
    print("\n".join(categories_))
    await bot.send_message(call.from_user.id, '<b>Your Categories:</b>\n\n' + '\n'.join(categories_), parse_mode='HTML')


@dp.callback_query_handler(text='TODAY_EXPENSES')
async def today_expenses_handler(call: types.CallbackQuery):
    print('@dp.callback_query_handler(text=TODAY_EXPENSES)')
    print(call.from_user.id)
    today_expenses_ = Finances.today_expenses(call.from_user.id)
    if not today_expenses_:
        await bot.send_message(call.from_user.id, 'Today expenses were not added', parse_mode='HTML')
        return
    today_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}'
        for expense in today_expenses_
    ]
    await bot.send_message(call.from_user.id, 'Today expenses\n' + '\n\n'.join(today_expenses_rows), parse_mode='HTML')


@dp.callback_query_handler(text='WEEK_EXPENSES')
async def week_expenses_handler(call: types.CallbackQuery):
    print('week_expenses_handler(call: types.CallbackQuery)')
    this_week_expenses_ = Finances.this_week_expenses(call.from_user.id)
    print(this_week_expenses_)
    if not this_week_expenses_:
        await bot.send_message(call.from_user.id, 'This week expenses were not added', parse_mode='HTML')
        return
    this_week_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}' for expense in this_week_expenses_
    ]
    await bot.send_message(
        call.from_user.id, 'This week expenses\n' + '\n\n'.join(this_week_expenses_rows), parse_mode='HTML'
    )


@dp.callback_query_handler(text='MONTH_EXPENSES')
async def month_expenses_handler(call: types.CallbackQuery):
    this_month_expenses_ = Finances.this_month_expenses(call.from_user.id)
    if not this_month_expenses_:
        await bot.send_message(call.from_user.id, 'This month expenses were not added', parse_mode='HTML')
        return
    this_month_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}'
        for expense in this_month_expenses_
    ]
    await bot.send_message(
        call.from_user.id, 'This month expenses\n' + '\n\n'.join(this_month_expenses_rows), parse_mode='HTML'
    )


@dp.callback_query_handler(text='TODAY_INCOMES')
async def today_incomes_handler(call: types.CallbackQuery):
    today_expenses_ = Finances.today_incomes(call.from_user.id)
    if not today_expenses_:
        await bot.send_message(call.from_user.id, 'Today incomes were not added', parse_mode='HTML')
        return
    today_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delinc{expense.id}'
        for expense in today_expenses_
    ]
    await bot.send_message(
        call.from_user.id, 'Today incomes\n' + '\n\n'.join(today_expenses_rows), parse_mode='HTML'
    )


@dp.callback_query_handler(text='WEEK_INCOMES')
async def week_incomes_handler(call: types.CallbackQuery):
    this_week_expenses_ = Finances.this_week_incomes(call.from_user.id)
    if not this_week_expenses_:
        await bot.send_message(call.from_user.id, 'This week incomes were not added', parse_mode='HTML')
        return
    this_week_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delinc{expense.id}'
        for expense in this_week_expenses_
    ]
    await bot.send_message(
        call.from_user.id, 'This week incomes\n' + "\n\n".join(this_week_expenses_rows), parse_mode='HTML'
    )


@dp.callback_query_handler(text='MONTH_INCOMES')
async def month_incomes_handler(call: types.CallbackQuery):
    this_month_expenses_ = Finances.this_month_incomes(call.from_user.id)
    if not this_month_expenses_:
        await bot.send_message(call.from_user.id, 'This month incomes were not added', parse_mode='HTML')
        return
    this_month_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delinc{expense.id}'
        for expense in this_month_expenses_
    ]
    await bot.send_message(
        call.from_user.id, 'This month incomes\n' + '\n\n'.join(this_month_expenses_rows), parse_mode='HTML'
    )


@dp.callback_query_handler(text='WEEK_STATISTIC')
async def this_week_statistic_handler(call: types.CallbackQuery):
    await call.message.delete()
    print('@dp.callback_query_handler(text=WEEK_STATISTIC)')
    file_name_ = Statistic.stats_for_current_week(call.from_user.id)
    result_ = Statistic.resulting_for_the_current_week(call.from_user.id)
    await bot.send_photo(
        call.from_user.id, open(f'{file_name_}.png', 'rb'),
        caption=f'<b>Total expenses:</b> {result_[0]}\n<b>Total incomes:</b> {result_[1] - result_[2]}\n'
                f'<b>Pure profit:</b> {result_[2]}\n'
                f'<b>Of Budget:</b> {Finances.get_budget_month_limit(call.from_user.id)}', parse_mode='HTML'
    )
    await asyncio.sleep(10)
    Statistic.delete_stats_image(file_name_)


@dp.callback_query_handler(text='MONTH_STATISTIC')
async def this_month_statistic_handler(call: types.CallbackQuery):
    await call.message.delete()
    print('@dp.callback_query_handler(text=MONTH_STATISTIC)')
    file_name_ = Statistic.stats_for_current_month(call.from_user.id)
    result_ = Statistic.resulting_for_the_current_month(call.from_user.id)
    await bot.send_photo(
        call.from_user.id, open(f'{file_name_}.png', 'rb'),
        caption=f'<b>Total expenses:</b> {result_[0]}\n<b>Total incomes:</b> '
                f'{result_[1]}\n<b>Pure profit: </b>{result_[2]}\n'
                f'<b>Of Budget:</b> {Finances.get_budget_month_limit(call.from_user.id) - result_[2]}',
        parse_mode='HTML'
    )
    await asyncio.sleep(10)
    Statistic.delete_stats_image(file_name_)


@dp.callback_query_handler(text='BACK_TO_OTHER_FINANCE')
async def back(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        call.from_user.id, "*Choose action to perform*", parse_mode="HTML",
        reply_markup=markup.inline_keyboard_other_menu
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

