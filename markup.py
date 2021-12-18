from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
 
"""INLINE KEYBOARD BUTTONS"""
 
inline_button_notes = InlineKeyboardButton('📝Notes📝', callback_data='📝Notes📝')
inline_button_library = InlineKeyboardButton('📚Library📚', callback_data='📚Library📚')
inline_button_schedule = InlineKeyboardButton('📅Schedule📅', callback_data='📅Schedule📅')
inline_button_finance = InlineKeyboardButton('💰Finance💰', callback_data='💰Finance💰')
inline_button_help = InlineKeyboardButton('ℹ️Helpℹ️', callback_data='ℹ️Helpℹ️')
inline_button_back = InlineKeyboardButton('🔙', callback_data='🔙')
inline_keyboard_menu = InlineKeyboardMarkup(row_width=2).add(inline_button_schedule,
                                                             inline_button_notes,
                                                             inline_button_library,
                                                             inline_button_finance,
                                                             inline_button_help)
 
inline_button_check_notes = InlineKeyboardButton("🔎Search note🔎", callback_data="🔎Search note🔎")
inline_button_add_note = InlineKeyboardButton('➕Add note➕', callback_data='➕Add note➕')
inline_button_delete_note = InlineKeyboardButton("🔥Delete note🔥", callback_data="🔥Delete note🔥")
inline_button_edit_note = InlineKeyboardButton("🖋️Edit note🖋️", callback_data="🖋️Edit note🖋️")
inline_keyboard_note_menu = InlineKeyboardMarkup(row_width=2).add(inline_button_check_notes,
                                                                  inline_button_add_note,
                                                                  inline_button_edit_note,
                                                                  inline_button_delete_note,
                                                                  inline_button_back)
 
inline_button_schedule_settings = InlineKeyboardButton("🔧Settings🔧", callback_data="🔧Settings🔧")
inline_button_schedule_currentday = InlineKeyboardButton("⌚Today schedule⌚",
                                                         callback_data="⌚Today schedule⌚")
inline_button_schedule_nextday = InlineKeyboardButton("📅Next day schedule📅", callback_data="📅Next day schedule📅")
inline_button_schedule_next = InlineKeyboardButton("⏭️Next pair⏭️", callback_data="⏭️Next pair⏭️")
inline_keyboard_schedule_menu = InlineKeyboardMarkup(row_width=2).add(inline_button_schedule_settings,
                                                                      inline_button_schedule_currentday,
                                                                      inline_button_schedule_nextday,
                                                                      inline_button_schedule_next,
                                                                      inline_button_back)
 
inline_button_add_group = InlineKeyboardButton("➕Add group➕", callback_data="➕Add group➕")
inline_button_delete_group = InlineKeyboardButton("➖Delete group➖", callback_data="➖Delete group➖")
inline_button_on_notification = InlineKeyboardButton("📧On notification📧", callback_data="📧On notification📧")
inline_button_off_notification = InlineKeyboardButton("📴Off notification📴", callback_data="📴Off notification📴")
inline_keyboard_schedule_settings = InlineKeyboardMarkup(row_width=2).add(inline_button_add_group,
                                                                          inline_button_delete_group,
                                                                          inline_button_on_notification,
                                                                          inline_button_off_notification,
                                                                          inline_button_back)
cb = CallbackData("night_action", "user_id", "button_for", "id_game")
 
