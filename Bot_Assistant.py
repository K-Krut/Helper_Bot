from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

import Finances
import Statistic
import bd
import exceptions
from imports import *
import config
import logging
from datetime import datetime, timedelta as tmd
from config import connection
from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import markup
import re

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class GroupAdd(StatesGroup):
    AddGroup = State()
    SelectGroup = State()


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


class AddPair(StatesGroup):
    AddSubject = State()


class AddAudiences(StatesGroup):
    AddAudience = State()


class AddTeachers(StatesGroup):
    AddTeacher = State()


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


list_of_themes = []
selected_day = 0
selected_pair = 0
selected_week = 0
selected_type_of_class = 0
selected_subject = 0
selected_audience = 0
selected_teacher = 0
selected_audience_id = 0
selected_subject_id = 0
selected_teacher_id = 0
update_week = False


@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    await message.delete()
    print(Finances.check_user_exists(str(message.from_user.id)))
    if not Finances.check_user_exists(str(message.from_user.id)):
        print("aboba")
        Finances.add_user(message['from'])
        Finances.set_default_budget(str(message.from_user.id))
    await bot.send_message(
        message.from_user.id, f"👤*Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                              f"{message.from_user.last_name if message.from_user.last_name else ''}\n "
                              f"I'm bot Student Assistant.*", parse_mode="HTML",
        reply_markup=markup.inline_keyboard_menu
    )


@dp.callback_query_handler(text="📝Notes📝")
async def note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_note_menu)


@dp.callback_query_handler(text="➕Add note➕")
async def add_note(call: types.CallbackQuery):
    await call.message.delete()
    selected_theme_id = 0
    selected_note_id = 0

    with connection.cursor() as cursor:

        select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
        cursor.execute(select_id)
        result = cursor.fetchall()
        global list_of_themes
        list_of_themes = []
        if result:
            for themes in result:
                for theme in themes:
                    list_of_themes.append(theme)
            await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_of_themes),
                                   parse_mode="HTML")
        await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note📝</b>", parse_mode="HTML")
        await Note.AddTheme.set()

    @dp.message_handler(state=Note.AddTheme)
    async def add_theme(message: types.Message):
        nonlocal selected_theme_id
        global list_of_themes

        if message.text in list_of_themes:
            with connection.cursor() as curs:
                search_theme = f"SELECT id FROM themes WHERE user_id = {message.from_user.id} " \
                               f"AND themes = '{message.text}'"
                curs.execute(search_theme)
                selected_theme_id = curs.fetchone()[0]
        else:
            with connection.cursor() as curs:
                adding_theme = f"INSERT INTO themes(user_id, themes) VALUES({message.from_user.id}, '{message.text}');"
                curs.execute(adding_theme)
                connection.commit()
                search_theme = f"SELECT id FROM themes WHERE user_id = {message.from_user.id} " \
                               f"AND themes = '{message.text}'"
                curs.execute(search_theme)
                selected_theme_id = curs.fetchone()[0]
        await bot.send_message(message.from_user.id, "<b>📝Enter NAME of note📝</b>", parse_mode="HTML")
        await Note.AddName.set()

    @dp.message_handler(state=Note.AddName)
    async def add_name(message: types.Message):
        nonlocal selected_theme_id
        nonlocal selected_note_id
        with connection.cursor() as cur:

            this_title = f"""SELECT title FROM notatics WHERE themes_id={selected_theme_id}"""
            cur.execute(this_title)
            results = cur.fetchall()
            list_of_title = []
            if results:
                for titles in results:
                    for title in titles:
                        list_of_title.append(title)
        if message.text in list_of_title:
            await bot.send_message(message.from_user.id, "This name is already used on this topic, try another")
        else:

            with connection.cursor() as curs:
                adding_name = f"""INSERT INTO notatics(themes_id, title) 
                VALUES({selected_theme_id}, "{message.text}")"""
                curs.execute(adding_name)
                connection.commit()
                search_note = f"""SELECT id FROM notatics WHERE themes_id = {selected_theme_id} """ \
                              f"""AND title = "{message.text}" """
                curs.execute(search_note)
                selected_note_id = curs.fetchone()[0]
                await Note.AddText.set()
                await bot.send_message(message.from_user.id, "<b>📝Enter TEXT of note📝</b>", parse_mode="HTML")

    @dp.message_handler(state=Note.AddText)
    async def add_text(message: types.Message):
        nonlocal selected_note_id
        with connection.cursor() as curs:
            adding_name = f"""UPDATE notatics SET text_notatics = "{message.text}" WHERE id = {selected_note_id};"""
            curs.execute(adding_name)
            connection.commit()
        await Note.next()
        mes = await bot.send_message(message.from_user.id, "<b>✅Note added✅</b>", parse_mode="HTML")
        await asyncio.sleep(3)
        await mes.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                            f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                            f"bot Student Assistant.</b>", parse_mode="HTML",
                            reply_markup=markup.inline_keyboard_menu)


@dp.callback_query_handler(text="🔥Delete note🔥")
async def send_themes(call: types.CallbackQuery):
    await call.message.delete()
    topic_names_list = []
    theme_id = 0
    with connection.cursor() as cursor:
        select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
        cursor.execute(select_id)
        result = cursor.fetchall()
        list_themes = []
        if result:
            for themes in result:
                for theme in themes:
                    list_themes.append(theme)
            await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
                                   parse_mode="HTML")
        if len(list_themes):
            await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note to delete it📝</b>", parse_mode="HTML")
            await NoteEdit.DeleteNote.set()
        else:
            note = await bot.send_message(call.from_user.id, "<b>❌THERE IS NO NOTES TO DELETE❌</b>", parse_mode="HTML")
            await asyncio.sleep(3)
            await note.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                                 f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                                 f"bot Student Assistant.</b>", parse_mode="HTML",
                                 reply_markup=markup.inline_keyboard_menu)

    @dp.message_handler(state=NoteEdit.DeleteNote)
    async def delete_note(message: types.Message):
        nonlocal list_themes

        if message.text in list_themes:
            with connection.cursor() as curs:
                nonlocal topic_names_list
                nonlocal theme_id
                select_theme_id = f"""SELECT id FROM themes WHERE themes="{message.text}" AND user_id={message.from_user.id};"""
                curs.execute(select_theme_id)
                theme_id = curs.fetchone()[0]
                select_topics = f"""SELECT title FROM notatics WHERE themes_id= {theme_id}"""
                curs.execute(select_topics)
                topics = curs.fetchall()
                for topic in topics:
                    topic_names_list.append(topic[0])
                await bot.send_message(call.from_user.id,
                                       "<b>Available notes on this theme:</b>\n" + '\n'.join(topic_names_list),
                                       parse_mode="HTML")
                await bot.send_message(call.from_user.id, "<b>📝Enter TITLE of note to delete it📝</b>",
                                       parse_mode="HTML")
                await NoteEdit.DeleteTopic.set()

    @dp.message_handler(state=NoteEdit.DeleteTopic)
    async def delete_topic(message: types.Message):
        if message.text in topic_names_list:
            with connection.cursor() as curs:
                note_delete = f"""DELETE 
                                  FROM notatics 
                                  WHERE themes_id={theme_id} 
                                  AND title = '{message.text}';"""
                curs.execute(note_delete)
                connection.commit()
            mes = await bot.send_message(message.from_user.id, f"<b>✅Note was successfully deleted✅</b>",
                                         parse_mode="HTML")
            await asyncio.sleep(3)
            await mes.edit_text(f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                                f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
                                f"bot Student Assistant.</b>", parse_mode="HTML",
                                reply_markup=markup.inline_keyboard_menu)
            await NoteEdit.next()
            topic_names_list.remove(message.text)
            if not topic_names_list:
                with connection.cursor() as curs:
                    themes_delete = f"""DELETE FROM themes WHERE id={theme_id};"""
                    curs.execute(themes_delete)
                    connection.commit()
        else:
            await bot.send_message(message.from_user.id, "<b>❌THERE IS NO NAMES LIKE THIS❌</b>\nTRY AGAIN.",
                                   parse_mode="HTML")


@dp.callback_query_handler(text="🔎Search note🔎")
async def search_note_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_search_menu)

    @dp.callback_query_handler(text="🔎Show all notes🔎")
    async def show_all_notes(c: types.CallbackQuery):
        tuple_list = await find_tuple_list(c)
        output_list = []
        for i in tuple_list:
            notes_text = f"Title: {i[0]}\nText: {i[1]}"
            output_list.append(notes_text)
        await bot.send_message(c.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list), parse_mode="HTML")

    @dp.callback_query_handler(text="🔎Search by theme🔎")
    async def search_by_theme(c: types.CallbackQuery):
        list_themes = []
        tuple_list = await find_tuple_list(c)
        with connection.cursor() as cursor:
            select_id = f"""SELECT themes FROM themes WHERE user_id={c.from_user.id}"""
            cursor.execute(select_id)
            result = cursor.fetchall()
            if result:
                for themes in result:
                    for theme in themes:
                        list_themes.append(theme)
                await bot.send_message(c.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
                                       parse_mode="HTML")
                await bot.send_message(c.from_user.id, "<b>📝Enter THEME of note📝</b>", parse_mode="HTML")
                await NoteSearch.SearchNote.set()
            else:
                note = await bot.send_message(c.from_user.id, "<b>❌THERE IS NO THEMES❌</b>", parse_mode="HTML")
                await asyncio.sleep(3)
                await note.edit_text(f"👤<b>Hi! {c.from_user.first_name if c.from_user.first_name else ''} "
                                     f"{c.from_user.last_name if c.from_user.last_name else ''}\n I'm "
                                     f"bot Student Assistant.</b>", parse_mode="HTML",
                                     reply_markup=markup.inline_keyboard_menu)

        @dp.message_handler(state=NoteSearch.SearchNote)
        async def search_notes_for_themes(message: types.Message):
            nonlocal tuple_list
            output_list = []
            with connection.cursor() as curs:
                curs.execute(f"""SELECT id FROM themes WHERE themes = '{message.text}'""")
                this_theme_id = curs.fetchone()[0]
            for i in tuple_list:
                if this_theme_id == i[2]:
                    notes_text = f"Title: {i[0]}\nText: {i[1]}"
                    output_list.append(notes_text)
            await bot.send_message(message.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list),
                                   parse_mode="HTML")
            await NoteSearch.next()

    @dp.callback_query_handler(text="🔎Search by name🔎")
    async def search_by_name(call_this: types.CallbackQuery):
        tuple_list = await find_tuple_list(call_this)
        this_title = []
        iteration_list = []
        with connection.cursor() as curs:

            for i in tuple_list:
                curs.execute(f"""SELECT title FROM notatics WHERE themes_id = {i[2]}""")
                temp = curs.fetchall()[iteration_list.count(i[2])][0]
                if temp not in this_title:
                    this_title.append(temp)
                iteration_list.append(i[2])
        if this_title:
            await bot.send_message(call_this.from_user.id, "<b>Titles:</b>\n" + "\n".join(this_title),
                                   parse_mode="HTML")
            await bot.send_message(call_this.from_user.id, "<b>📝Enter TITLE of note📝</b>", parse_mode="HTML")
            await NoteSearchByTitle.SearchByTitle.set()
        else:
            note = await bot.send_message(call_this.from_user.id, "<b>❌THERE IS NO TITLE❌</b>", parse_mode="HTML")
            await asyncio.sleep(3)
            await note.edit_text(f"👤<b>Hi! {call_this.from_user.first_name if call_this.from_user.first_name else ''} "
                                 f"{call_this.from_user.last_name if call_this.from_user.last_name else ''}\n I'm "
                                 f"bot Student Assistant.</b>", parse_mode="HTML",
                                 reply_markup=markup.inline_keyboard_menu)

        @dp.message_handler(state=NoteSearchByTitle.SearchByTitle)
        async def search_notes_for_title(message: types.Message):
            output_list = []

            for j in tuple_list:
                if j[0] == message.text:
                    notes_text = f"Title: {j[0]}\nText: {j[1]}"
                    output_list.append(notes_text)

            await bot.send_message(message.from_user.id, "<b>Notes:</b>\n" + "\n\n".join(output_list),
                                   parse_mode="HTML")
            await NoteSearchByTitle.next()


async def find_tuple_list(c):
    await c.message.delete()
    id_themes_list = []
    result_list = []
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM themes WHERE user_id = {c.from_user.id}""")
        result = cursor.fetchall()
    for id_themes in result:
        id_themes_list.append(id_themes[0])

    with connection.cursor() as cursor:
        for id_themes in id_themes_list:
            cursor.execute(f"""SELECT title, text_notatics, themes_id FROM notatics WHERE themes_id = {id_themes}""")
            result = cursor.fetchall()
            result_list.append(result)
    tuple_list = []
    for i in result_list:
        for j in i:
            tuple_list.append(j)
    return tuple_list


@dp.callback_query_handler(text="🖋️Edit note🖋️")
async def edit_note(call: types.CallbackQuery):
    await call.message.delete()
    topic_names_list = []
    theme_id = 0
    title_this = 0
    with connection.cursor() as cursor:
        select_id = f"""SELECT themes FROM themes WHERE user_id={call.from_user.id}"""
        cursor.execute(select_id)
        result = cursor.fetchall()
        list_themes = []
        if result:
            for themes in result:
                for theme in themes:
                    list_themes.append(theme)
            await bot.send_message(call.from_user.id, "<b>Available themes:</b>\n" + '\n'.join(list_themes),
                                   parse_mode="HTML")
        if len(list_themes):
            await bot.send_message(call.from_user.id, "<b>📝Enter THEME of note to delete it📝</b>", parse_mode="HTML")
            await EditNote.SearchThemes.set()
        else:
            note = await bot.send_message(call.from_user.id, "<b>❌YOU HAVE NO THEMES❌</b>", parse_mode="HTML")
            await asyncio.sleep(3)
            await note.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                                 f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                                 f"bot Student Assistant.</b>", parse_mode="HTML",
                                 reply_markup=markup.inline_keyboard_menu)

    @dp.message_handler(state=EditNote.SearchThemes)
    async def delete_note(message: types.Message):
        nonlocal list_themes

        if message.text in list_themes:
            with connection.cursor() as curs:
                nonlocal topic_names_list
                nonlocal theme_id
                select_theme_id = f"""SELECT id FROM themes WHERE themes="{message.text}" AND user_id={message.from_user.id};"""
                curs.execute(select_theme_id)
                theme_id = curs.fetchone()[0]
                select_topics = f"""SELECT title FROM notatics WHERE themes_id= {theme_id}"""
                curs.execute(select_topics)
                topics = curs.fetchall()
                for topic in topics:
                    topic_names_list.append(topic[0])
                await bot.send_message(call.from_user.id,
                                       "<b>Available notes on this theme:</b>\n" + '\n'.join(topic_names_list),
                                       parse_mode="HTML")
                await bot.send_message(call.from_user.id, "<b>📝Enter TITLE of note to delete it📝</b>",
                                       parse_mode="HTML")
                await EditNote.SearchTitle.set()

    @dp.message_handler(state=EditNote.SearchTitle)
    async def delete_topic(message: types.Message):
        nonlocal title_this
        if message.text in topic_names_list:
            title_this = message.text
            await bot.send_message(message.from_user.id, "<b>Enter new note text</b>", parse_mode="HTML")
            await EditNote.EnterText.set()
        else:
            await bot.send_message(message.from_user.id, "<b>❌THERE IS NO NAMES LIKE THIS❌</b>\nTRY AGAIN.",
                                   parse_mode="HTML")

    @dp.message_handler(state=EditNote.EnterText)
    async def edit_text(message: types.Message):
        with connection.cursor() as curs:
            curs.execute(f"""UPDATE notatics 
                             SET text_notatics = '{message.text}' 
                             WHERE themes_id={theme_id} 
                             AND title = '{title_this}';""")
            connection.commit()
            this_note = await bot.send_message(message.from_user.id, "<b>✅NOTE SUCCESSFULLY EDITED✅</b>",
                                               parse_mode="HTML")

            await asyncio.sleep(3)
            await EditNote.next()
            await this_note.edit_text(
                f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
                f"bot Student Assistant.</b>", parse_mode="HTML",
                reply_markup=markup.inline_keyboard_menu)


@dp.callback_query_handler(text="📅Schedule📅")
async def schedule_menu(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Choose action to perform</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_schedule_menu)


@dp.callback_query_handler(text="🔧Settings🔧")
async def schedule_settings(call: types.CallbackQuery):
    await call.message.delete()
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT group_id FROM users WHERE id = '{call.from_user.id}';""")
        group_id = cursor.fetchone()[0]
        if group_id:
            cursor.execute(f"""SELECT group_name FROM group_name WHERE id = {group_id}""")
            group_name = cursor.fetchone()[0]
        else:
            group_name = "❌"
    await bot.send_message(call.from_user.id, f"<b>Current settings</b>:\nGroup: {group_name}", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_schedule_settings)


@dp.callback_query_handler(text="➕Add group➕")
async def add_group(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Enter your group</b>", parse_mode="HTML")
    founded_groups = []
    await GroupAdd.AddGroup.set()

    @dp.message_handler(state=GroupAdd.AddGroup)
    async def find_group(message: types.Message):
        nonlocal founded_groups
        groups_name = []
        groups_correct_name = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT group_name FROM group_name")
            groups_name.append(cursor.fetchall())
        for group in groups_name[0]:
            groups_correct_name.append(group[0])
        for group_name in filter(re.compile(message.text.lower()).match, groups_correct_name):
            founded_groups.append(group_name)
        if not founded_groups or not message.text[:1].isalpha():
            await bot.send_message(message.from_user.id, "<b>Invalid name (at least two letters), try again</b>",
                                   parse_mode="HTML")
        else:
            await bot.send_message(message.from_user.id,
                                   "<b>Founded group:\n</b>" + '\n'.join(founded_groups),
                                   parse_mode="HTML")
            await bot.send_message(message.from_user.id, "<b>Choose group from this list, and write it</b>",
                                   parse_mode="HTML")
            await GroupAdd.SelectGroup.set()

    @dp.message_handler(state=GroupAdd.SelectGroup)
    async def select_group(message: types.Message):
        nonlocal founded_groups
        if message.text.lower() in founded_groups:
            with connection.cursor() as curs:
                curs.execute(f"""SELECT id FROM group_name WHERE group_name = "{message.text.lower()}";""")
                group_id = curs.fetchone()[0]
                curs.execute("SET FOREIGN_KEY_CHECKS=OFF;")
                curs.execute(f""" UPDATE users SET group_id = {group_id} WHERE id="{message.from_user.id}";""")
            connection.commit()
            note = await bot.send_message(message.from_user.id, "<b>✅GROUP SUCCESSFULLY ADDED✅</b>",
                                          parse_mode="HTML")
            await GroupAdd.next()
            await asyncio.sleep(3)
            await note.edit_text(f"👤<b>Hi! {message.from_user.first_name if message.from_user.first_name else ''} "
                                 f"{message.from_user.last_name if message.from_user.last_name else ''}\n I'm "
                                 f"bot Student Assistant.</b>", parse_mode="HTML",
                                 reply_markup=markup.inline_keyboard_menu)
        else:
            await bot.send_message(message.from_user.id,
                                   "<b>❌Invalid name, there is no such name in groups!❌\nTry again</b>",
                                   parse_mode="HTML")


@dp.callback_query_handler(text="➖Delete group➖")
async def delete_group(call: types.CallbackQuery):
    await call.message.delete()
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=OFF;")
        cursor.execute(
            f"""UPDATE users SET group_id = NULL WHERE id = '{call.from_user.id}';""")
    connection.commit()
    note = await bot.send_message(call.from_user.id, "<b>✅GROUP SUCCESSFULLY DELETED✅</b>",
                                  parse_mode="HTML")
    await asyncio.sleep(3)
    await note.edit_text(f"👤<b>Hi! {call.from_user.first_name if call.from_user.first_name else ''} "
                         f"{call.from_user.last_name if call.from_user.last_name else ''}\n I'm "
                         f"bot Student Assistant.</b>", parse_mode="HTML",
                         reply_markup=markup.inline_keyboard_menu)


@dp.callback_query_handler(text="➕Add schedule➕")
async def add_lesson_menu(call: types.CallbackQuery):
    with connection.cursor() as curs:
        curs.execute(f"""SELECT group_id FROM users WHERE id = '{call.from_user.id}';""")
        result = curs.fetchone()[0]
        print(result)
    await call.message.delete()
    if result:
        await bot.send_message(call.from_user.id, "<b>Choose day of weekday</b>",
                               reply_markup=markup.inline_keyboard_day_of_week, parse_mode="HTML")
    else:
        note = await bot.send_message(call.from_user.id, "<b>❌You can not use schedule before you choose group❌</b>",
                                      parse_mode="HTML")
        await asyncio.sleep(3)
        await note.edit_text(f"<b>Current settings</b>:\nGroup: ❌", parse_mode="HTML",
                             reply_markup=markup.inline_keyboard_schedule_settings)


@dp.callback_query_handler(text="Monday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 1
    await add_lessons_day_of_week(call)


@dp.callback_query_handler(text="Tuesday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 2
    await add_lessons_day_of_week(call)


@dp.callback_query_handler(text="Wednesday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 3
    await add_lessons_day_of_week(call)


@dp.callback_query_handler(text="Thursday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 4
    await add_lessons_day_of_week(call)


@dp.callback_query_handler(text="Friday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 5
    await add_lessons_day_of_week(call)


@dp.callback_query_handler(text="Saturday")
async def add_monday(call: types.CallbackQuery):
    global selected_day
    selected_day = 6
    await add_lessons_day_of_week(call)


async def add_lessons_day_of_week(call):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>Add lesson</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_pair)


@dp.callback_query_handler(text="First")
async def first(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 1
    await bot.send_message(call.from_user.id, "<b>ADD FIRST PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Second")
async def second(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 2
    await bot.send_message(call.from_user.id, "<b>ADD SECOND PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Third")
async def third(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 3
    await bot.send_message(call.from_user.id, "<b>ADD THIRD PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Fourth")
async def fourth(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 4
    await bot.send_message(call.from_user.id, "<b>ADD FOURTH PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Fifth")
async def fifth(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 5
    await bot.send_message(call.from_user.id, "<b>ADD FIFTH PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Sixth")
async def sixth(call: types.CallbackQuery):
    await call.message.delete()
    global selected_pair
    selected_pair = 6
    await bot.send_message(call.from_user.id, "<b>ADD SIXTH PAIR INFO</b>",
                           reply_markup=markup.inline_keyboard_add_pair,
                           parse_mode="HTML")


@dp.callback_query_handler(text="Week")
async def week(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, f"<b>SELECT WEEK</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_week_menu)


@dp.callback_query_handler(text="EVEN")
async def even(call: types.CallbackQuery):
    await choose_week(call, 1, "EVEN")


@dp.callback_query_handler(text="ODD")
async def odd(call: types.CallbackQuery):
    await choose_week(call, 2, "ODD")


async def choose_week(call, select_week, string_week):
    await call.message.delete()
    global selected_week
    global update_week

    with connection.cursor() as curs:
        curs.execute(
            f"""SELECT week_number FROM schedules 
            WHERE user_id='{call.from_user.id}' AND day_of_week = {selected_day} AND class_id = {selected_pair};""")
        information = curs.fetchall()

        weeks = [x[0] for x in information]
        print(weeks)

    if select_week in weeks:
        update_week = True

    selected_week = select_week
    note = await bot.send_message(call.from_user.id, f"<b>✅YOU SELECT {string_week} WEEK✅</b>", parse_mode="HTML")
    await asyncio.sleep(3)
    await note.edit_text("<b>ADD PAIR INFO</b>",
                         reply_markup=markup.inline_keyboard_add_pair,
                         parse_mode="HTML")


@dp.callback_query_handler(text="Type of class")
async def type_of_class(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, f"<b>SELECT TYPE OF LESSON</b>", parse_mode="HTML",
                           reply_markup=markup.inline_keyboard_type_of_lesson_menu)


@dp.callback_query_handler(text="Lecture")
async def lecture(call: types.CallbackQuery):
    await select_type(call, 2, "LECTURE")


@dp.callback_query_handler(text="Lab")
async def lab(call: types.CallbackQuery):
    await select_type(call, 3, "LAB")


@dp.callback_query_handler(text="Practice")
async def practice(call: types.CallbackQuery):
    await select_type(call, 1, "PRACTICE")


async def select_type(call, select_type_class, string_type_of_class):
    await call.message.delete()
    global selected_type_of_class
    selected_type_of_class = select_type_class
    note = await bot.send_message(call.from_user.id, f"<b>✅YOU SELECT {string_type_of_class}✅</b>",
                                  parse_mode="HTML")
    await asyncio.sleep(3)
    await note.edit_text("<b>ADD PAIR INFO</b>",
                         reply_markup=markup.inline_keyboard_add_pair,
                         parse_mode="HTML")


@dp.callback_query_handler(text="Subject name")
async def subject_name(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>🖊Enter subject🖊</b>", parse_mode="HTML")
    await AddPair.AddSubject.set()

    @dp.message_handler(state=AddPair.AddSubject)
    async def add_subject(message: types.Message):
        global selected_subject
        selected_subject = message.text
        await AddPair.next()
        note = await bot.send_message(message.from_user.id, f"<b>✅YOU SELECT SUBJECT✅</b>",
                                      parse_mode="HTML")
        await asyncio.sleep(3)
        await note.edit_text("<b>ADD PAIR INFO</b>",
                             reply_markup=markup.inline_keyboard_add_pair,
                             parse_mode="HTML")


@dp.callback_query_handler(text="Audience")
async def audience(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>🖊Enter audience🖊</b>", parse_mode="HTML")
    await AddAudiences.AddAudience.set()

    @dp.message_handler(state=AddAudiences.AddAudience)
    async def add_audience(message: types.Message):
        global selected_audience
        selected_audience = message.text
        await AddAudiences.next()

        note = await bot.send_message(message.from_user.id, f"<b>✅YOU SELECT AUDIENCE✅</b>",
                                      parse_mode="HTML")
        await asyncio.sleep(3)
        await note.edit_text("<b>ADD PAIR INFO</b>",
                             reply_markup=markup.inline_keyboard_add_pair,
                             parse_mode="HTML")


@dp.callback_query_handler(text="Teacher")
async def teacher(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "<b>🖊Enter teacher🖊</b>", parse_mode="HTML")
    await AddTeachers.AddTeacher.set()
    print(f"first --> {call.from_user.id}")

    @dp.message_handler(state=AddTeachers.AddTeacher)
    async def add_audience(message: types.Message):
        global selected_teacher
        selected_teacher = message.text
        await AddTeachers.next()
        print(f"second --> {message.from_user.id}")
        note = await bot.send_message(message.from_user.id, f"<b>✅YOU SELECT TEACHER✅</b>",
                                      parse_mode="HTML")

        await asyncio.sleep(3)
        await note.edit_text("<b>ADD PAIR INFO</b>",
                             reply_markup=markup.inline_keyboard_add_pair,
                             parse_mode="HTML")


@dp.callback_query_handler(text="✅Ready✅")
async def ready(call: types.CallbackQuery):
    await call.message.delete()
    global selected_day, selected_pair, selected_type_of_class, selected_week, selected_audience, selected_subject, \
        selected_teacher, selected_audience_id, selected_subject_id, selected_teacher_id
    if selected_subject:
        selected_subject_id = await push_info('subjects', 'subject_name', selected_subject)
    if selected_audience:
        selected_audience_id = await push_info('audiences', 'audience', selected_audience)
    if selected_audience:
        selected_teacher_id = await push_info('teacher', 'teacher_name', selected_teacher)
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT group_id FROM users WHERE id = {call.from_user.id}""")
        group_id = cursor.fetchone()
    note1 = 0
    note2 = 0
    note3 = 0
    note4 = 0
    note5 = 0

    if not selected_type_of_class:
        note1 = await bot.send_message(call.from_user.id,
                                       "<b>You must enter all fields. Please, select type of class. </b>",
                                       parse_mode="HTML")

    if not selected_week:
        note2 = await bot.send_message(call.from_user.id,
                                       "<b>You must enter all fields. Please, select week, odd or even.</b>",
                                       parse_mode="HTML")

    if not selected_audience_id:
        note3 = await bot.send_message(call.from_user.id,
                                       "<b>You must enter all fields. Please, write down audience.</b>",
                                       parse_mode="HTML")

    if not selected_subject_id:
        note4 = await bot.send_message(call.from_user.id,
                                       "<b>You must enter all fields. Please, write down subject.</b>",
                                       parse_mode="HTML")

    if not selected_teacher_id:
        note5 = await bot.send_message(call.from_user.id,
                                       "<b>You must enter all fields. Please, write down teacher.</b>",
                                       parse_mode="HTML")

    if not selected_audience_id or not selected_week or not selected_audience_id or not selected_subject_id \
            or not selected_teacher_id:
        await asyncio.sleep(3)
        if not isinstance(note1, int):
            await note1.delete()
        if not isinstance(note2, int):
            await note2.delete()
        if not isinstance(note3, int):
            await note3.delete()
        if not isinstance(note4, int):
            await note4.delete()
        if not isinstance(note5, int):
            await note5.delete()

        await bot.send_message(call.from_user.id, "<b>ADD PAIR INFO</b>", reply_markup=markup.inline_keyboard_add_pair,
                               parse_mode="HTML")
    else:
        await add_schedules(call, selected_day, selected_pair, selected_type_of_class, selected_week,
                            selected_audience_id, selected_subject_id, call.from_user.id, group_id[0],
                            selected_teacher_id)

        selected_subject = 0
        selected_audience = 0
        selected_day = 0
        selected_pair = 0
        selected_type_of_class = 0
        selected_week = 0
        selected_teacher = 0

        await bot.send_message(call.from_user.id, "<b>Choose day of weekday</b>",
                               reply_markup=markup.inline_keyboard_day_of_week, parse_mode="HTML")


async def push_info(table, line, selected):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM {table} WHERE {line}='{selected}'""")
        result = cursor.fetchone()
    if result:
        return result[0]
    else:
        with connection.cursor() as cur:
            cur.execute(f"""INSERT INTO {table}({line}) VALUES("{selected}");""")
            connection.commit()
        with connection.cursor() as c:
            c.execute(f"""SELECT id FROM {table} WHERE {line} = '{selected}';""")
            return c.fetchone()[0]


async def add_schedules(call, day, pair, type_class, weeks, audiences, subject, user_id, group_id, teacher_id):
    print(day, pair, type_class, weeks, audiences, subject, user_id, group_id, teacher_id)
    global update_week
    if update_week:
        with connection.cursor() as cur:
            cur.execute(
                f"""UPDATE schedules SET group_id = {group_id}, subject_name = {subject}, type_of_class = {type_class}, 
                audience = {audiences}, teacher = {teacher_id} WHERE user_id = '{call.from_user.id}' 
                AND day_of_week = {selected_day} AND class_id = {selected_pair} AND week_number = {selected_week}""")
            connection.commit()
        update_week = False
    else:
        with connection.cursor() as curs:
            curs.execute(
                f"""INSERT INTO schedules(
                day_of_week, class_id, type_of_class, week_number ,audience, subject_name, user_id, group_id, teacher) 
                VALUES({day}, {pair}, {type_class}, {weeks}, {audiences}, {subject}, 
                '{user_id}', {group_id}, {teacher_id});"""
            )
            connection.commit()


@dp.callback_query_handler(text="⌚Today schedule⌚")
async def today_schedule(call: types.CallbackQuery):
    await call.message.delete()
    today = datetime.today().isoweekday()
    today_week = await even_or_odd()
    group_id_number = 0
    today_schedules = []
    await day_schedule(call, today, today_week, group_id_number, today_schedules)


async def even_or_odd():
    now = datetime.now()
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    return 2 if not ((((now - tmd(days=now.weekday())) -
                       (sep - tmd(days=sep.weekday()))).days // 7) % 2) else 1


async def day_schedule(call, day, weeks, group_id, today_schedules):
    with connection.cursor() as curs:
        curs.execute(f"""SELECT group_id FROM users WHERE id = '{call.from_user.id}';""")
        group_id = curs.fetchone()[0]
    if day == 7:
        await bot.send_message(call.from_user.id, f"<b>Неділя\nВихідний\nLesson: ❌</b>")
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT class_id, type_of_class,
                audience, subject_name, teacher FROM schedules
                WHERE day_of_week = {day} AND user_id = "{call.from_user.id}" AND group_id = {group_id} 
                AND week_number = {weeks};""")
            today_info = cursor.fetchall()
        with connection.cursor() as cur:
            cur.execute(f"""SELECT name_day_of_week FROM days_of_week WHERE id = {day};""")
            day = cur.fetchone()[0]
            today_schedules.append(day)
            for today_information in today_info:
                cur.execute(f"""SELECT id, time_of_start, time_of_end FROM classes WHERE id = {today_information[0]}""")
                time_of_lesson = cur.fetchall()
                cur.execute(f"""SELECT subject_name FROM subjects WHERE id = {today_information[3]}""")
                subject_now = cur.fetchone()[0]
                cur.execute(f"""SELECT type_of_class FROM type_of_classes WHERE id = {today_information[1]}""")
                type_of_class_now = cur.fetchone()[0]
                cur.execute(f"""SELECT teacher_name FROM teacher WHERE id = {today_information[4]}""")
                teacher_now = cur.fetchone()[0]
                cur.execute(f"""SELECT audience FROM audiences WHERE id = {today_information[2]}""")
                audience_now = cur.fetchone()[0]
                for pair_time in time_of_lesson:
                    today_schedules.append(f"Lesson: {pair_time[0]}")
                    today_schedules.append("Time of start: " + str(pair_time[1]))
                    today_schedules.append("Time of end: " + str(pair_time[2]))
                today_schedules.append(f"Subject: {subject_now}")
                today_schedules.append(f"Type of lesson: {type_of_class_now}")
                today_schedules.append(f"Teacher: {teacher_now}")
                today_schedules.append(f"Audience: {audience_now}\n")
        await bot.send_message(call.from_user.id, "<b>" + '\n'.join(today_schedules) + "</b>", parse_mode="HTML")


@dp.callback_query_handler(text="📅Next day schedule📅")
async def back(call: types.CallbackQuery):
    await call.message.delete()
    next_day = datetime.today().isoweekday() + 1
    next_week = await even_or_odd()
    if next_day == 8:
        next_day = 1
        if next_week == 1:
            next_week = 2
        else:
            next_week = 1
    group_id_number = 0
    next_day_schedules = []
    await day_schedule(call, next_day, next_week, group_id_number, next_day_schedules)


@dp.callback_query_handler(text="⏭️Next pair⏭️")
async def next_pair(call: types.CallbackQuery):
    await call.message.delete()
    next_pair_day = datetime.today().isoweekday()
    next_pair_weeks = await even_or_odd()
    next_pair_this_time = datetime.now().time()
    next_pair_group_id = 0
    today_schedules = []
    with connection.cursor() as curs:
        curs.execute(f"""SELECT group_id FROM users WHERE id = '{call.from_user.id}';""")
        next_pair_group_id = curs.fetchone()[0]

    today_schedules = await next_pair_schedule(call, next_pair_day, next_pair_weeks, next_pair_group_id,
                                               next_pair_this_time)
    while not today_schedules:
        next_pair_day += 1
        next_pair_this_time = datetime.strptime("00:00:00", "%H:%M:%S").time()
        if next_pair_day == 8:
            next_pair_day = 1
            if next_pair_weeks == 1:
                next_pair_weeks = 2
            else:
                next_pair_weeks = 1
        today_schedules = await next_pair_schedule(call, next_pair_day, next_pair_weeks, next_pair_group_id,
                                                   next_pair_this_time)
    await bot.send_message(call.from_user.id, "<b>" + '\n'.join(today_schedules) + "</b>", parse_mode="HTML")


async def next_pair_schedule(call, day, weeks, group_id, this_time):
    today_schedules = []
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT class_id, type_of_class,
            audience, subject_name, teacher FROM schedules
            WHERE day_of_week = {day} AND user_id = "{call.from_user.id}" AND group_id = {group_id} 
            AND week_number = {weeks};""")
        today_info = cursor.fetchall()
    with connection.cursor() as cur:
        cur.execute(f"""SELECT name_day_of_week FROM days_of_week WHERE id = {day};""")
        day = cur.fetchone()[0]
        for today_information in today_info:
            cur.execute(f"""SELECT id, time_of_start, time_of_end FROM classes WHERE id = {today_information[0]}""")
            time_of_lesson = cur.fetchall()
            cur.execute(f"""SELECT subject_name FROM subjects WHERE id = {today_information[3]}""")
            subject_now = cur.fetchone()[0]
            cur.execute(f"""SELECT type_of_class FROM type_of_classes WHERE id = {today_information[1]}""")
            type_of_class_now = cur.fetchone()[0]
            cur.execute(f"""SELECT teacher_name FROM teacher WHERE id = {today_information[4]}""")
            teacher_now = cur.fetchone()[0]
            cur.execute(f"""SELECT audience FROM audiences WHERE id = {today_information[2]}""")
            audience_now = cur.fetchone()[0]
            for pair_time in time_of_lesson:
                lesson_time = str(pair_time[1])
                if this_time < datetime.strptime(lesson_time, "%H:%M:%S").time():
                    today_schedules.append(day)
                    today_schedules.append(f"Lesson: {pair_time[0]}")
                    today_schedules.append("Time of start: " + str(pair_time[1]))
                    today_schedules.append("Time of end: " + str(pair_time[2]))
                    today_schedules.append(f"Subject: {subject_now}")
                    today_schedules.append(f"Type of lesson: {type_of_class_now}")
                    today_schedules.append(f"Teacher: {teacher_now}")
                    today_schedules.append(f"Audience: {audience_now}\n")
                    return today_schedules


@dp.callback_query_handler(text="🟡This week schedule🟡")
async def this_week_schedule(call: types.CallbackQuery):
    await call.message.delete()
    await week_schedule(call, await even_or_odd())


@dp.callback_query_handler(text="⚫Next week schedule⚫")
async def this_week_schedule(call: types.CallbackQuery):
    await call.message.delete()
    current_week = await even_or_odd()
    if current_week == 1:
        current_week = 2
    else:
        current_week = 1
    await week_schedule(call, current_week)


async def week_schedule(call, this_week_week):
    today_schedules = []
    with connection.cursor() as curs:
        curs.execute(f"""SELECT group_id FROM users WHERE id = '{call.from_user.id}';""")
        group_id = curs.fetchone()[0]
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT  day_of_week, class_id, type_of_class,
            audience, subject_name, teacher FROM schedules
            WHERE user_id = "{call.from_user.id}" AND group_id = {group_id} AND week_number = {this_week_week};""")
        this_week_info = cursor.fetchall()
    with connection.cursor() as cur:

        for today_information in this_week_info:
            cur.execute(f"""SELECT name_day_of_week FROM days_of_week WHERE id = {today_information[0]};""")
            day = cur.fetchone()[0]
            cur.execute(f"""SELECT id, time_of_start, time_of_end FROM classes WHERE id = {today_information[1]}""")
            time_of_lesson = cur.fetchall()
            cur.execute(f"""SELECT subject_name FROM subjects WHERE id = {today_information[4]}""")
            subject_now = cur.fetchone()[0]
            cur.execute(f"""SELECT type_of_class FROM type_of_classes WHERE id = {today_information[2]}""")
            type_of_class_now = cur.fetchone()[0]
            cur.execute(f"""SELECT teacher_name FROM teacher WHERE id = {today_information[5]}""")
            teacher_now = cur.fetchone()[0]
            cur.execute(f"""SELECT audience FROM audiences WHERE id = {today_information[3]}""")
            audience_now = cur.fetchone()[0]
            if day not in today_schedules:
                today_schedules.append(day)
            for pair_time in time_of_lesson:
                today_schedules.append(f"Lesson: {pair_time[0]}")
                today_schedules.append("Time of start: " + str(pair_time[1]))
                today_schedules.append("Time of end: " + str(pair_time[2]))
            today_schedules.append(f"Subject: {subject_now}")
            today_schedules.append(f"Type of lesson: {type_of_class_now}")
            today_schedules.append(f"Teacher: {teacher_now}")
            today_schedules.append(f"Audience: {audience_now}\n")
    await bot.send_message(call.from_user.id, "<b>" + '\n'.join(today_schedules) + "</b>", parse_mode="HTML")


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


""" Finance handlers  """


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
    await bot.send_message(call.from_user.id, "Enter like this: 245 taxi")
    await HandlerExpenses.AddExpensesState.set()

    @dp.message_handler(state=HandlerExpenses.AddExpensesState)
    async def adding_expense(message: types.Message):
        print(message)
        try:
            Finances.add_expense(message['text'], message.from_user.id)
        except exceptions.AddExpenseError as exp:
            await message.answer(str(exp))
        await bot.send_message(message.from_user.id, 'ADDED', parse_mode='HTML')
        await HandlerExpenses.next()


@dp.callback_query_handler(text='💰Add incomes💰')
async def add_incomes(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "Enter like this: 245 job")
    await HandlerIncomes.AddIncomesState.set()

    @dp.message_handler(state=HandlerIncomes.AddIncomesState)
    async def adding_incomes(message: types.Message):
        try:
            Finances.add_incomes(message['text'], message.from_user.id)
        except exceptions.AddIncomeError(str(message)) as exp:
            await message.answer(str(exp))
        await bot.send_message(message.from_user.id, 'ADDED', parse_mode='HTML')
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
            return
        await bot.send_message(message.from_user.id, 'Edited', parse_mode='HTML')
        await HandlerCategory.next()


@dp.message_handler(lambda message: message.text.startswith('/delexp'))
async def del_expense(message: types.Message):
    try:
        Finances.delete_expense(int(message.text[7:]), message.from_user.id)
    except exceptions.DeleteError(str(message)) as exp:
        await bot.send_message(message.from_user.id, f'{exp}', parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Deleted')


@dp.message_handler(lambda message: message.text.startswith('/delinc'))
async def del_expense(message: types.Message):
    try:
        Finances.delete_expense(int(message.text[7:]), message.from_user.id)
    except exceptions.DeleteError(str(message)) as exp:
        await bot.send_message(message.from_user.id, f'{exp}', parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Deleted')


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
    await call.message.delete()
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
    await call.message.delete()
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
    await call.message.delete()
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
    await call.message.delete()
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
    await call.message.delete()
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
    await call.message.delete()
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
                f'<b>Pure profit:</b> {result_[2]}\n',
        # f'<b>Of Budget:</b> {Finances.get_budget_month_limit(call.from_user.id)}'
        parse_mode='HTML'
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
                f'{result_[1]}\n<b>Pure profit: </b>{result_[2]}\n',
        # f'<b>Of Budget:</b> {Finances.get_budget_month_limit(call.from_user.id) - result_[2]}',
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


lib = types.InlineKeyboardMarkup(row_width=1)
add = types.InlineKeyboardButton(text="Add book to list", callback_data="add")
stats = types.InlineKeyboardButton(text="View your top", callback_data="stats")
full = types.InlineKeyboardButton(text="View full list", callback_data="full")
lib.add(add, stats, full, markup.inline_button_back)


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
async def deletess(message: types.Message, state: FSMContext):
    if message.text and not any((numb not in '1234567890') for numb in message.text):
        await state.finish()
        if bd.delete_book(int(message.text), message.from_user.id):
            await bot.send_message(message.chat.id, "Книга удалена")
        else:
            await bot.send_message(message.chat.id, "Я не смог найти книгу по даному запросу")
    else:
        await bot.send_message(message.chat.id, "Введите пожалуйста код")
        await message.delete()


@dp.callback_query_handler(text="📚Library📚")
async def library(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, "Выбирайте,что именно вы хотите сделать с книжным списком желаний:",
                           reply_markup=lib)


@dp.callback_query_handler(text="add")
async def add_(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, "Напишите запрос,по которому я буду искать книгу:")
    await FSMBook.write_search.set()


@dp.callback_query_handler(text="full")
async def full_(call: types.CallbackQuery):
    await call.message.delete()
    delete = types.InlineKeyboardButton(text="Удалить книгу со списка", callback_data="delete")
    await bot.send_message(call.message.chat.id, "Список ваших интересов:\n" + bd.get_list(
        call.from_user.id) + '\nВведи код книги ,если хочешь убрать её',
                           reply_markup=InlineKeyboardMarkup(row_width=1).add(delete))


@dp.callback_query_handler(text="delete")
async def delete_(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Введи код книги для удаления:")
    await FSMBook.write_delete.set()


@dp.callback_query_handler(text="stats")
async def stats_(call: types.CallbackQuery):
    await call.message.delete()
    data = bd.get_max_info(call.from_user.id)
    await bot.send_message(call.message.chat.id, "Информация:\n" + '<><><><><><><><>\n'.join(
        '\n'.join(str(item) for item in group) for group in data.items()))


executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
