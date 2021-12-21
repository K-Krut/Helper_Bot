import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator
from matplotlib.ticker import AutoMinorLocator
from random import shuffle
from imports import connection


def _get_formatted(date):
    return date.strftime('%Y-%m-%d')


def week_data_for_stats():
    print('week_data_for_stats')
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT  SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
            f'WHERE yearweek(CURDATE()) = yearweek(date_time) '
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def month_data_for_stats():
    print('month_data_for_stats')
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT  SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
            f'WHERE MONTH(date_time)=MONTH(CURDATE())'
            f'and YEAR(date_time)=YEAR(CURDATE())'
            f'GROUP BY CAST(date_time AS DATE) '
            f'ORDER BY date_time ASC'
        )
        rows = cursor.fetchall()
        return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]


def create_diagram_for_stats(values, dates, type_):
    print('create_diagram_for_stats')
    x = np.arange(len(dates))
    y = np.array(values)
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.title(type_)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    ax.xaxis.set_major_locator(DayLocator())
    plt.plot(x, y, 'o-')
    ax.set_xticklabels(dates, fontsize=10)
    ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    fig.autofmt_xdate()
    k = list('abcdefghhijklmnopqrsruwxyz')
    shuffle(k)
    name_ = ''.join(i for i in k[:10])
    plt.savefig(name_)
    return name_, sum(values)


def stats_for_current_week():
    print('stats_for_current_week')
    current_week_data_ = week_data_for_stats()
    return create_diagram_for_stats(current_week_data_[0], current_week_data_[1], 'Week Expenses')


def stats_for_current_month():
    print('stats_for_current_month')
    current_month_data_ = month_data_for_stats()
    return create_diagram_for_stats(current_month_data_[0], current_month_data_[1], 'Month Expenses')


def delete_stats_image(name_):
    path_ = os.getcwd().replace(f'\\', '/')
    os.remove(f"{path_}/{name_}.png")









# def suka():
#     return [_get_formatted(i) for i in numpy.array([datetime(2021, 12, 1) + timedelta(hours=i) for i in xrange(31)])]


# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # # l = week_data_for_stats()[0]
# # # # k = week_data_for_stats()[1]
# # # y = np.array(l)
# # # x = np.arange(len(k))
# # # # x = np.linspace(0, 10, 50)
# # # fig, ax = plt.subplots(figsize=(10, 4))
# # # plt.title("Линейная зависимость y = x") # заголовок
# # # plt.xlabel("Date") # ось абсцисс
# # # plt.ylabel("Amount") # ось ординат
# # # ax.xaxis.set_major_locator(DayLocator())
# # #
# # # plt.plot(x, y, 'o-')  # построение графика
# # # ax.set_xticklabels(k, fontsize=10)
# # # ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
# # #
# # # ax.xaxis.set_minor_locator(AutoMinorLocator())
# # # fig.autofmt_xdate()
# # #
# # # plt.show()
# from random import random, sample, shuffle
#
