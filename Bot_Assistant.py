import Finances
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

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

list_of_themes = []


class NoteSearch(StatesGroup):
    SearchNote = State()


class NoteSearchByTitle(StatesGroup):
    SearchByTitle = State()


class NoteEdit(StatesGroup):
    DeleteNote = State()
    DeleteTopic = State()


class EditNote(StatesGroup):
    SearchThemes = State()
    SearchTitle = State()
    EnterText = State()


class Note(StatesGroup):
    AddTheme = State()
    AddName = State()
    AddText = State()


# @dp.message_handler(commands=['start'])
# async def send_welcome_message(message: types.Message):
#     await message.delete()
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
#         if not cursor.rowcount:
#             insert_query = f"INSERT INTO users(id) VALUES({message.from_user.id});"
#             cursor.execute(insert_query)
#             connection.commit()
#     await bot.send_message(message.from_user.id,
#                            f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
#                            f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
#                            f"bot Student Assistant.</b>", parse_mode="HTML", reply_markup=markup.inline_keyboard_menu
@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    print(Finances.check_user_exists(str(message.from_user.id)))
    if not Finances.check_user_exists(str(message.from_user.id)):
        Finances.add_user(message['from'])
        Finances.set_default_budget(str(message.from_user.id))
    await bot.send_message(
        message.from_user.id, f"👤*Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                              f"{message.from_user.last_name if message.from_user.last_name else ''}\n "
                              f"I'm bot Student Assistant.*", parse_mode="Markdown",
        reply_markup=markup.inline_keyboard_menu
    )


@dp.callback_query_handler(text="📝Notes📝")
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_note_menu)


# @dp.callback_query_handler(text="➕Add note➕")
# async def add_note(call: types.CallbackQuery):
#     await call.message.delete()
#     selected_theme_id = 0
#     selected_note_id = 0
#
#     with connection.cursor() as cursor:
#
#         select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
#         cursor.execute(select_id)
#         result = cursor.fetchall()
#         global list_of_themes
#         list_of_themes = []
#         if result:
#             for themes in result:
#                 for theme in themes:
#                     list_of_themes.append(theme)
#             await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_of_themes),
#                                    parse_mode="HTML")
#         await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note📝</b>", parse_mode="HTML")
#         await Note.AddTheme.set()
#
#     @dp.message_handler(state=Note.AddTheme)
#     async def add_theme(message: types.Message):
#         nonlocal selected_theme_id
#         global list_of_themes
#         print(list_of_themes)
#         if message.text in list_of_themes:
#             with connection.cursor() as curs:
#                 search_theme = f"SELECT id FROM themes WHERE user_id = {message.from_user.id} " \
#                                f"AND themes = '{message.text}'"
#                 curs.execute(search_theme)
#                 selected_theme_id = curs.fetchone()[0]
#         else:
#             with connection.cursor() as curs:
#                 adding_theme = f"INSERT INTO themes(user_id, themes) VALUES({message.from_user.id}, '{message.text}');"
#                 curs.execute(adding_theme)
#                 connection.commit()
#                 search_theme = f"SELECT id FROM themes WHERE user_id = {message.from_user.id} " \
#                                f"AND themes = '{message.text}'"
#                 curs.execute(search_theme)
#                 selected_theme_id = curs.fetchone()[0]
#         await bot.send_message(message.from_user.id, "<b>📝Enter NAME of note📝</b>", parse_mode="HTML")
#         await Note.AddName.set()
#
#     @dp.message_handler(state=Note.AddName)
#     async def add_name(message: types.Message):
#         nonlocal selected_theme_id
#         nonlocal selected_note_id
#         with connection.cursor() as cur:
#
#             this_title = f"""SELECT title FROM notatics WHERE themes_id={selected_theme_id}"""
#             cur.execute(this_title)
#             results = cur.fetchall()
#             list_of_title = []
#             if results:
#                 for titles in results:
#                     for title in titles:
#                         list_of_title.append(title)
#         if message.text in list_of_title:
#             await bot.send_message(message.from_user.id, "This name is already used on this topic, try another")
#         else:
#
#             with connection.cursor() as curs:
#                 adding_name = f"""INSERT INTO notatics(themes_id, title) VALUES({selected_theme_id}, "{message.text}")"""
#                 curs.execute(adding_name)
#                 connection.commit()
#                 search_note = f"""SELECT id FROM notatics WHERE themes_id = {selected_theme_id} """ \
#                               f"""AND title = "{message.text}" """
#                 curs.execute(search_note)
#                 selected_note_id = curs.fetchone()[0]
#                 await Note.AddText.set()
#                 await bot.send_message(message.from_user.id, "<b>📝Enter TEXT of note📝</b>", parse_mode="HTML")
#
#     @dp.message_handler(state=Note.AddText)
#     async def add_text(message: types.Message):
#         nonlocal selected_note_id
#         with connection.cursor() as curs:
#             adding_name = f"""UPDATE notatics SET text_notatics = "{message.text}" WHERE id = {selected_note_id};"""
#             curs.execute(adding_name)
#             connection.commit()
#         await Note.next()
#         mes = await bot.send_message(message.from_user.id, "<b>✅Note added✅</b>", parse_mode="HTML")
#         await asyncio.sleep(3)
#         await mes.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
#                             f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
#                             f"bot Student Assistant.</b>", parse_mode="HTML",
#                             reply_markup=markup.inline_keyboard_menu)
#
#
# @dp.callback_query_handler(text="🔥Delete note🔥")
# async def send_themes(call: types.CallbackQuery):
#     await call.message.delete()
#     topic_names_list = []
#     theme_id = 0
#     with connection.cursor() as cursor:
#         select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
#         cursor.execute(select_id)
#         result = cursor.fetchall()
#         list_themes = []
#         if result:
#             for themes in result:
#                 for theme in themes:
#                     list_themes.append(theme)
#             await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
#                                    parse_mode="HTML")
#         if len(list_themes):
#             await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note to delete it📝</b>", parse_mode="HTML")
#             await NoteEdit.DeleteNote.set()
#         else:
#             note = await bot.send_message(call.from_user.id, "<b>❌THERE IS NO NOTES TO DELETE❌</b>", parse_mode="HTML")
#             await asyncio.sleep(3)
#             await note.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
#                                  f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
#                                  f"bot Student Assistant.</b>", parse_mode="HTML",
#                                  reply_markup=markup.inline_keyboard_menu)
#
#     @dp.message_handler(state=NoteEdit.DeleteNote)
#     async def delete_note(message: types.Message):
#         nonlocal list_themes
#
#         if message.text in list_themes:
#             with connection.cursor() as curs:
#                 nonlocal topic_names_list
#                 nonlocal theme_id
#                 select_theme_id = f"""SELECT id FROM themes WHERE themes="{message.text}" AND user_id={message.from_user.id};"""
#                 curs.execute(select_theme_id)
#                 theme_id = curs.fetchone()[0]
#                 select_topics = f"""SELECT title FROM notatics WHERE themes_id= {theme_id}"""
#                 curs.execute(select_topics)
#                 topics = curs.fetchall()
#                 for topic in topics:
#                     topic_names_list.append(topic[0])
#                 await bot.send_message(call.from_user.id,
#                                        "<b>Available notes on this theme:</b>\n" + '\n'.join(topic_names_list),
#                                        parse_mode="HTML")
#                 await bot.send_message(call.from_user.id, "<b>📝Enter TITLE of note to delete it📝</b>",
#                                        parse_mode="HTML")
#                 await NoteEdit.DeleteTopic.set()
#
#     @dp.message_handler(state=NoteEdit.DeleteTopic)
#     async def delete_topic(message: types.Message):
#         if message.text in topic_names_list:
#             with connection.cursor() as curs:
#                 note_delete = f"""DELETE FROM notatics WHERE themes_id={theme_id} AND title = '{message.text}';"""
#                 curs.execute(note_delete)
#                 connection.commit()
#             mes = await bot.send_message(message.from_user.id, f"<b>✅Note was successfully deleted✅</b>",
#                                          parse_mode="HTML")
#             await asyncio.sleep(3)
#             await mes.edit_text(f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
#                                 f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
#                                 f"bot Student Assistant.</b>", parse_mode="HTML",
#                                 reply_markup=markup.inline_keyboard_menu)
#             await NoteEdit.next()
#             topic_names_list.remove(message.text)
#             if not topic_names_list:
#                 with connection.cursor() as curs:
#                     themes_delete = f"""DELETE FROM themes WHERE id={theme_id};"""
#                     curs.execute(themes_delete)
#                     connection.commit()
#         else:
#             await bot.send_message(message.from_user.id, "<b>❌THERE IS NO NAMES LIKE THIS❌</b>\nTRY AGAIN.",
#                                    parse_mode="HTML")
#
#
# @dp.callback_query_handler(text="🔎Search note🔎")
# async def search_note_menu(call: types.CallbackQuery):
#     await call.message.delete()
#     await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
#                            reply_markup=markup.inline_keyboard_search_menu)
#
#     @dp.callback_query_handler(text="🔎Show all notes🔎")
#     async def show_all_notes(c: types.CallbackQuery):
#         tuple_list = await find_tuple_list(c)
#         output_list = []
#         for i in tuple_list:
#             notes_text = f"Title: {i[0]}\nText: {i[1]}"
#             output_list.append(notes_text)
#         await bot.send_message(c.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list), parse_mode="HTML")
#
#     @dp.callback_query_handler(text="🔎Search by theme🔎")
#     async def search_by_theme(c: types.CallbackQuery):
#         list_themes = []
#         tuple_list = await find_tuple_list(c)
#         with connection.cursor() as cursor:
#             select_id = f"""SELECT themes FROM themes WHERE user_id={c.from_user.id}"""
#             cursor.execute(select_id)
#             result = cursor.fetchall()
#             if result:
#                 for themes in result:
#                     for theme in themes:
#                         list_themes.append(theme)
#                 await bot.send_message(c.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
#                                        parse_mode="HTML")
#                 await bot.send_message(c.from_user.id, "<b>📝Enter THEME of note📝</b>", parse_mode="HTML")
#                 await NoteSearch.SearchNote.set()
#             else:
#                 note = await bot.send_message(c.from_user.id, "<b>❌THERE IS NO THEMES❌</b>", parse_mode="HTML")
#                 await asyncio.sleep(3)
#                 await note.edit_text(f"👤<b>Hi! {c.from_user.first_name if c.from_user.first_name else ''} "
#                                      f"{c.from_user.last_name if c.from_user.last_name else ''}\n I'm "
#                                      f"bot Student Assistant.</b>", parse_mode="HTML",
#                                      reply_markup=markup.inline_keyboard_menu)
#
#         @dp.message_handler(state=NoteSearch.SearchNote)
#         async def search_notes_for_themes(message: types.Message):
#             nonlocal tuple_list
#             output_list = []
#             with connection.cursor() as curs:
#                 curs.execute(f"""SELECT id FROM themes WHERE themes = '{message.text}'""")
#                 this_theme_id = curs.fetchone()[0]
#             for i in tuple_list:
#                 if this_theme_id == i[2]:
#                     notes_text = f"Title: {i[0]}\nText: {i[1]}"
#                     output_list.append(notes_text)
#             await bot.send_message(message.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list),
#                                    parse_mode="HTML")
#             await NoteSearch.next()
#
#     @dp.callback_query_handler(text="🔎Search by name🔎")
#     async def search_by_name(call_this: types.CallbackQuery):
#         tuple_list = await find_tuple_list(call_this)
#         this_title = []
#         iteration_list = []
#         with connection.cursor() as curs:
#
#             for i in tuple_list:
#                 curs.execute(f"""SELECT title FROM notatics WHERE themes_id = {i[2]}""")
#                 temp = curs.fetchall()[iteration_list.count(i[2])][0]
#                 if temp not in this_title:
#                     this_title.append(temp)
#                 iteration_list.append(i[2])
#         if this_title:
#             await bot.send_message(call_this.from_user.id, "<b>Titles:</b>\n" + "\n".join(this_title),
#                                    parse_mode="HTML")
#             await bot.send_message(call_this.from_user.id, "<b>📝Enter TITLE of note📝</b>", parse_mode="HTML")
#             await NoteSearchByTitle.SearchByTitle.set()
#         else:
#             note = await bot.send_message(call_this.from_user.id, "<b>❌THERE IS NO TITLE❌</b>", parse_mode="HTML")
#             await asyncio.sleep(3)
#             await note.edit_text(f"👤<b>Hi! {call_this.from_user.first_name if call_this.from_user.first_name else ''} "
#                                  f"{call_this.from_user.last_name if call_this.from_user.last_name else ''}\n I'm "
#                                  f"bot Student Assistant.</b>", parse_mode="HTML",
#                                  reply_markup=markup.inline_keyboard_menu)
#
#         @dp.message_handler(state=NoteSearchByTitle.SearchByTitle)
#         async def search_notes_for_title(message: types.Message):
#             output_list = []
#
#             for j in tuple_list:
#                 if j[0] == message.text:
#                     notes_text = f"Title: {j[0]}\nText: {j[1]}"
#                     output_list.append(notes_text)
#
#             await bot.send_message(message.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list),
#                                    parse_mode="HTML")
#             await NoteSearchByTitle.next()
#
#
# async def find_tuple_list(c):
#     await c.message.delete()
#     id_themes_list = []
#     result_list = []
#     with connection.cursor() as cursor:
#         cursor.execute(f"""SELECT id FROM themes WHERE user_id = {c.from_user.id}""")
#         result = cursor.fetchall()
#     for id_themes in result:
#         id_themes_list.append(id_themes[0])
#
#     with connection.cursor() as cursor:
#         for id_themes in id_themes_list:
#             cursor.execute(f"""SELECT title, text_notatics, themes_id FROM notatics WHERE themes_id = {id_themes}""")
#             result = cursor.fetchall()
#             result_list.append(result)
#     tuple_list = []
#     for i in result_list:
#         for j in i:
#             tuple_list.append(j)
#     return tuple_list
#
#
# @dp.callback_query_handler(text="🖋️Edit note🖋️")
# async def edit_note(call: types.CallbackQuery):
#     await call.message.delete()
#     topic_names_list = []
#     theme_id = 0
#     title_this = 0
#     with connection.cursor() as cursor:
#         select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
#         cursor.execute(select_id)
#         result = cursor.fetchall()
#         list_themes = []
#         if result:
#             for themes in result:
#                 for theme in themes:
#                     list_themes.append(theme)
#             await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
#                                    parse_mode="HTML")
#         if len(list_themes):
#             await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note to delete it📝</b>", parse_mode="HTML")
#             await EditNote.SearchThemes.set()
#         else:
#             note = await bot.send_message(call.from_user.id, "<b>❌YOU HAVE NO THEMES❌</b>", parse_mode="HTML")
#             await asyncio.sleep(3)
#             await note.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
#                                  f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
#                                  f"bot Student Assistant.</b>", parse_mode="HTML",
#                                  reply_markup=markup.inline_keyboard_menu)
#
#     @dp.message_handler(state=EditNote.SearchThemes)
#     async def delete_note(message: types.Message):
#         nonlocal list_themes
#
#         if message.text in list_themes:
#             with connection.cursor() as curs:
#                 nonlocal topic_names_list
#                 nonlocal theme_id
#                 select_theme_id = f"""SELECT id FROM themes WHERE themes="{message.text}" AND user_id={message.from_user.id};"""
#                 curs.execute(select_theme_id)
#                 theme_id = curs.fetchone()[0]
#                 select_topics = f"""SELECT title FROM notatics WHERE themes_id= {theme_id}"""
#                 curs.execute(select_topics)
#                 topics = curs.fetchall()
#                 for topic in topics:
#                     topic_names_list.append(topic[0])
#                 await bot.send_message(call.from_user.id,
#                                        "<b>Available notes on this theme:</b>\n" + '\n'.join(topic_names_list),
#                                        parse_mode="HTML")
#                 await bot.send_message(call.from_user.id, "<b>📝Enter TITLE of note to delete it📝</b>",
#                                        parse_mode="HTML")
#                 await EditNote.SearchTitle.set()
#
#     @dp.message_handler(state=EditNote.SearchTitle)
#     async def delete_topic(message: types.Message):
#         nonlocal title_this
#         if message.text in topic_names_list:
#             title_this = message.text
#             await bot.send_message(message.from_user.id, "<b>Enter new note text</b>", parse_mode="HTML")
#             await EditNote.EnterText.set()
#         else:
#             await bot.send_message(message.from_user.id, "<b>❌THERE IS NO NAMES LIKE THIS❌</b>\nTRY AGAIN.",
#                                    parse_mode="HTML")
#
#     @dp.message_handler(state=EditNote.EnterText)
#     async def edit_text(message: types.Message):
#         with connection.cursor() as curs:
#             curs.execute(f"""UPDATE notatics
#             SET text_notatics = '{message.text}' WHERE themes_id={theme_id} AND title = '{title_this}';""")
#             this_note = await bot.send_message(message.from_user.id, "<b>✅THERE IS NO TITLE✅</b>", parse_mode="HTML")
#             connection.commit()
#             await asyncio.sleep(3)
#             await this_note.edit_text(
#                 f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
#                 f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
#                 f"bot Student Assistant.</b>", parse_mode="HTML",
#                 reply_markup=markup.inline_keyboard_menu)
#


@dp.callback_query_handler(text="📅Schedule📅")
async def schedule_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_schedule_menu)


@dp.callback_query_handler(text="🔧Settings🔧")
async def schedule_settings(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, f"<b>Current settings</b>:\nGroup: \nNotification: ", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_schedule_settings)


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
        call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
        reply_markup=markup.inline_keyboard_finance_menu
    )


@dp.callback_query_handler(text='💰Finance💰')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_finance_menu)


@dp.callback_query_handler(text='🏛️Budget🏛️')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    print(Finances.get_budget_daily_limit(call.from_user.id))
    print(Finances.get_budget_month_limit(call.from_user.id))
    await bot.send_message(
        call.from_user.id, f'<b>Your budget</b>:\n<b>Daily</b>: {Finances.get_budget_daily_limit(call.from_user.id)}\n'
                           f'<b>Month</b>: {Finances.get_budget_month_limit(call.from_user.id)}', parse_mode='HTML',
        reply_markup=markup.inline_keyboard_budget_menu
    )


@dp.callback_query_handler(text='📈Statistic📈')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_statistic_menu)


@dp.callback_query_handler(text='OTHER_FINANCE_MENU')
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "*Choose action to perform*", parse_mode="Markdown",
                           reply_markup=markup.inline_keyboard_other_menu)


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
            Finances.create_category_finance(message['text'], message.from_user.id)
            await asyncio.sleep(60)
        except exceptions.AddCategoryError as exp:
            await message.answer(str(exp))
            return


########################################################################################################################
# после добавления идет время и выводит меню, но работа функции не прекращаеться


@dp.callback_query_handler(text='💸Add expense💸')
async def add_expense_(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def adding_expense(message: types.Message):
        print(message)
        try:
            Finances.add_expense(message['text'], message.from_user.id)
        except exceptions.AddExpenseError as exp:
            await message.answer(str(exp))
        # await asyncio.sleep(20)
        # await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
        #                        reply_markup=markup.inline_keyboard_finance_menu)


@dp.callback_query_handler(text='💰Add incomes💰')
async def add_incomes(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def adding_incomes(message: types.Message):
        try:
            Finances.add_incomes(message['text'], message.from_user.id)
        except exceptions.AddIncomeError(str(message)) as exp:
            await message.answer(str(exp))


@dp.callback_query_handler(text='🖊️Edit budget🖊️')
async def edit_budget(call: types.CallbackQuery):
    await call.message.delete()

    @dp.message_handler()
    async def editing_budget(message: types.Message):
        try:
            Finances.edit_budget(message['text'], message.from_user.id)
        except exceptions.ChangeBudgetError(str(message)) as exp:
            await message.answer(str(exp))


@dp.message_handler(lambda message: message.text.startswith('/delexp'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    Finances.delete_expense(row_id, message.from_user.id)


@dp.callback_query_handler(text='TODAY_EXPENSES')
async def today_expenses_handler(call: types.CallbackQuery):
    print('@dp.callback_query_handler(text=TODAY_EXPENSES)')
    print(call.from_user.id)
    today_expenses_ = Finances.today_expenses(call.from_user.id)
    if not today_expenses_:
        await bot.send_message(call.from_user.id, 'Today expenses were not added', parse_mode='Markdown')
        return
    today_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}'
        for expense in today_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(today_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='WEEK_EXPENSES')
async def week_expenses_handler(call: types.CallbackQuery):
    print('week_expenses_handler(call: types.CallbackQuery)')
    this_week_expenses_ = Finances.this_week_expenses(call.from_user.id)
    print(this_week_expenses_)
    if not this_week_expenses_:
        await bot.send_message(call.from_user.id, 'This week were not added', parse_mode='Markdown')
        return
    this_week_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}' for expense in this_week_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(this_week_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='SEE_CATEGORIES')
async def categories_viewing_handler(call: types.CallbackQuery):
    print('categories_viewing_handler')
    categories_data = Finances.see_categories(call.from_user.id)
    if not categories_data:
        await bot.send_message(call.from_user.id, 'You haven`t any category yet', parse_mode='Markdown')
        return
    categories_ = [f'<b>{category.name_}:</b>    {category.category_text}' for category in categories_data]
    print("\n".join(categories_))
    await bot.send_message(call.from_user.id, '<b>Your Categories:</b>\n\n' + '\n'.join(categories_), parse_mode='HTML')


@dp.callback_query_handler(text='MONTH_EXPENSES')
async def month_expenses_handler(call: types.CallbackQuery):
    this_month_expenses_ = Finances.this_month_expenses(call.from_user.id)
    if not this_month_expenses_:
        await bot.send_message(call.from_user.id, 'Today expenses were not added', parse_mode='Markdown')
        return
    this_month_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /delexp{expense.id}'
        for expense in this_month_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(this_month_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='TODAY_INCOMES')
async def today_incomes_handler(call: types.CallbackQuery):
    today_expenses_ = Finances.today_incomes(call.from_user.id)
    if not today_expenses_:
        await bot.send_message(call.from_user.id, 'Today expenses were not added', parse_mode='Markdown')
        return
    today_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /del_inc{expense.id}'
        for expense in today_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(today_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='WEEK_INCOMES')
async def week_incomes_handler(call: types.CallbackQuery):
    this_week_expenses_ = Finances.this_week_incomes(call.from_user.id)
    if not this_week_expenses_:
        await bot.send_message(call.from_user.id, 'This week were not added', parse_mode='Markdown')
        return
    this_week_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /del_inc{expense.id}'
        for expense in this_week_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(this_week_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='MONTH_INCOMES')
async def month_incomes_handler(call: types.CallbackQuery):
    this_month_expenses_ = Finances.this_month_incomes(call.from_user.id)
    if not this_month_expenses_:
        await bot.send_message(call.from_user.id, 'Today expenses were not added', parse_mode='Markdown')
        return
    this_month_expenses_rows = [
        f'{expense.amount} UAH on {expense.category_name} — /del_inc{expense.id}'
        for expense in this_month_expenses_
    ]
    await bot.send_message(call.from_user.id, "\n\n".join(this_month_expenses_rows), parse_mode='Markdown')


@dp.callback_query_handler(text='WEEK_STATISTIC')
async def this_week_statistic_handler(call: types.CallbackQuery):
    await call.message.delete()
    print('@dp.callback_query_handler(text=WEEK_STATISTIC)')
    file_name_ = Statistic.stats_for_current_week(call.from_user.id)
    result_ = Statistic.resulting_for_the_current_week(call.from_user.id)
    await bot.send_photo(
        call.from_user.id, open(f'{file_name_}.png', 'rb'),
        caption=f'<b>Total expenses:</b> {result_[0]}\n<b>Total incomes:</b> {result_[1]}\n'
                f'<b>Pure profit:</b> {result_[2]}', parse_mode='HTML'
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
                f'{result_[1]}\n<b>Pure profit: </b>{result_[2]}', parse_mode='HTML'
    )
    await asyncio.sleep(10)
    Statistic.delete_stats_image(file_name_)


# @dp.callback_query_handler(text='🖊️Edit budget🖊️')
# async def edit_budget(call: types.CallbackQuery):
#     await call.message.delete()
#
#     @dp.message_handler()
#     async def editing_budget(message: types.Message):
#         try:
#             print(message['text'])
#             Finances.edit_budget(message['text'])
#         except exceptions.AddIncomeError as exp:
#             await message.answer(str(exp))
#
#     # await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
#     #                        reply_markup=markup.inline_keyboard_finance_menu)
# @dp.callback_query_handler(text='🖊️Edit budget🖊️')
# async def edit_budget(call: types.CallbackQuery):
#     await call.message.delete()
#
#     @dp.message_handler()
#     async def editing_budget(message: types.Message):
#         try:
#             print(message['text'])
#             Finances.edit_budget(message['text'])
#         except exceptions.AddIncomeError as exp:
#             await message.answer(str(exp))
#
#     # await bot.send_message(call.from_user.id, '*Choose action to perform*', parse_mode='Markdown',
#     #                        reply_markup=markup.inline_keyboard_finance_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
