from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

inline_button_search_by_name = InlineKeyboardButton("🔎Search by name🔎", callback_data="🔎Search by name🔎")
inline_button_search_by_theme = InlineKeyboardButton("🔎Search by theme🔎", callback_data="🔎Search by theme🔎")
inline_button_show_all = InlineKeyboardButton("🔎Show all notes🔎", callback_data="🔎Show all notes🔎")
inline_keyboard_search_menu = InlineKeyboardMarkup(row_width=2).add(inline_button_search_by_name,
                                                                    inline_button_search_by_theme,
                                                                    inline_button_show_all, inline_button_back)

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


""" Finance buttons """


inline_button_add_finance_category = InlineKeyboardButton('➕Add category➕', callback_data='➕Add category➕')
inline_button_add_expense = InlineKeyboardButton('💸Add expense💸', callback_data='💸Add expense💸')
inline_button_add_incomes = InlineKeyboardButton('💰Add incomes💰', callback_data='💰Add incomes💰')
inline_button_budget = InlineKeyboardButton('🏛️Budget🏛️', callback_data='🏛️Budget🏛️')
inline_button_finance_statistic = InlineKeyboardButton('📈Statistic📈', callback_data='📈Statistic📈')
inline_button_finance_other = InlineKeyboardButton('✨Other✨', callback_data='OTHER_FINANCE_MENU')
inline_button_back_to_finance = InlineKeyboardButton('🔙', callback_data='BACK_TO_FINANCE')

inline_keyboard_finance_menu = InlineKeyboardMarkup(row_width=2).add(
    inline_button_add_incomes, inline_button_add_expense, inline_button_finance_statistic,
    inline_button_add_finance_category, inline_button_budget, inline_button_finance_other,
    inline_button_back
)

# inline_button_statistic_today = InlineKeyboardButton('Today', callback_data='TODAY_STATISTIC')
inline_button_statistic_by_week = InlineKeyboardButton('This week', callback_data='WEEK_STATISTIC')
inline_button_statistic_by_month = InlineKeyboardButton('This month', callback_data='MONTH_STATISTIC')

inline_keyboard_statistic_menu = InlineKeyboardMarkup(row_width=2).add(
    inline_button_statistic_by_week, inline_button_statistic_by_month,
    inline_button_back_to_finance
)

inline_button_edit_budget = InlineKeyboardButton('🖊️Edit budget🖊️', callback_data='🖊️Edit budget🖊️')

inline_keyboard_budget_menu = InlineKeyboardMarkup(row_width=2).add(
    inline_button_edit_budget, inline_button_back_to_finance
)

inline_button_see_today_expenses = InlineKeyboardButton('Today Expenses', callback_data='TODAY_EXPENSES')
inline_button_see_week_expenses = InlineKeyboardButton('This week Expenses', callback_data='WEEK_EXPENSES')
inline_button_see_month_expenses = InlineKeyboardButton('This month Expenses', callback_data='MONTH_EXPENSES')

inline_button_see_today_incomes = InlineKeyboardButton('Today Incomes', callback_data='TODAY_INCOMES')
inline_button_see_week_incomes = InlineKeyboardButton('This week Incomes', callback_data='WEEK_INCOMES')
inline_button_see_month_incomes = InlineKeyboardButton('This month Incomes', callback_data='MONTH_INCOMES')


inline_button_back_to_other_finance = InlineKeyboardButton('🔙', callback_data='BACK_TO_OTHER_FINANCE')
inline_button_see_categories = InlineKeyboardButton('My categories', callback_data='SEE_CATEGORIES')


inline_keyboard_other_menu = InlineKeyboardMarkup(row_width=2).add(
    inline_button_see_today_expenses, inline_button_see_today_incomes,
    inline_button_see_week_expenses, inline_button_see_week_incomes,
    inline_button_see_month_expenses, inline_button_see_month_incomes,
    inline_button_see_categories, inline_button_back_to_finance
)
