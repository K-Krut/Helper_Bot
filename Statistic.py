import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator
from matplotlib.ticker import AutoMinorLocator
from random import shuffle
from imports import connection


def _get_formatted(date):
    return date.strftime('%Y-%m-%d')


def merging_list(arr1, arr2):
    return [i for i in arr2 if i not in arr1] + arr1


def delete_stats_image(name_):
    path_ = os.getcwd().replace(f'\\', '/')
    os.remove(f"{path_}/{name_}.png")


def get_week_expenses_for_stats(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
            f'WHERE yearweek(date_time, 1) = yearweek(CURDATE(), 1) AND user_id = {user_id} '
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def get_week_incomes_for_stats(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM incomes '
            f'WHERE yearweek(date_time, 1)  = yearweek(CURDATE(), 1)  AND user_id = {user_id} '
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def get_month_expenses_for_stats(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
            f'WHERE MONTH(date_time) = MONTH(CURDATE()) '
            f'AND YEAR(date_time) = YEAR(CURDATE()) AND user_id = {user_id} '
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def get_month_incomes_for_stats(user_id):
    print('get_month_incomes_for_stats')
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM incomes '
            f'WHERE MONTH(date_time) = MONTH(CURDATE()) '
            f'AND YEAR(date_time) = YEAR(CURDATE()) AND user_id = {user_id} '
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        print(rows)
        # rows.sort(key=lambda x: x.count, reverse=True)
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def week_data_for_stats(user_id):
    expenses_ = get_week_expenses_for_stats(user_id)
    incomes_ = get_week_incomes_for_stats(user_id)
    return expenses_[0], expenses_[1], incomes_[0], incomes_[1]


def month_data_for_stats(user_id):
    expenses_ = get_month_expenses_for_stats(user_id)
    incomes_ = get_month_incomes_for_stats(user_id)
    return expenses_[0], expenses_[1], incomes_[0], incomes_[1]


def stats_for_current_week(user_id):
    print('stats_for_current_week')
    current_week_data_ = week_data_for_stats(user_id)
    return create_diagram_for_stats(current_week_data_[0], current_week_data_[2],
                                    current_week_data_[1], current_week_data_[3], 'Week Statistic')


def stats_for_current_month(user_id):
    print('stats_for_current_month')
    current_month_data_ = month_data_for_stats(user_id)
    return create_diagram_for_stats(current_month_data_[0], current_month_data_[2],
                                    current_month_data_[1], current_month_data_[3], 'Month Statistic')


def create_diagram_for_stats(values_expenses, values_incomes, dates_expenses, dates_incomes, type_):
    print('create_diagram_for_stats')
    x = np.arange(len(dates_expenses))
    y = np.array(values_expenses)
    y2 = np.array(values_incomes)
    x2 = np.arange(len(dates_incomes))
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title(type_)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    ax.xaxis.set_major_locator(DayLocator())
    plt.plot(x, y, 'o-')
    plt.plot(x2, y2, 'o-')
    print(dates_expenses)
    print(merging_list(dates_expenses, dates_incomes))
    ax.set_xticklabels(merging_list(dates_expenses, dates_incomes), fontsize=10)
    ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    fig.autofmt_xdate()
    alphabet_ = list('abcdefghhijklmnopqrsruwxyz')
    shuffle(alphabet_)
    name_ = ''.join(i for i in alphabet_[:10])
    plt.savefig(name_)
    return name_


def calculating_results(values_expenses, values_incomes):
    total_expenses = sum(values_expenses)
    total_incomes = sum(values_incomes)
    pure_profit = total_incomes - total_expenses
    return total_expenses, total_incomes, pure_profit


def resulting_for_the_current_week(user_id):
    current_week_data_ = week_data_for_stats(user_id)
    return calculating_results(current_week_data_[0], current_week_data_[2])


def resulting_for_the_current_month(user_id):
    current_month_data_ = month_data_for_stats(user_id)
    return calculating_results(current_month_data_[0], current_month_data_[2])

