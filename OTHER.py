# import numpy as np
#
# import os
#
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib.dates import DayLocator
# from matplotlib.ticker import AutoMinorLocator
# from random import shuffle
# from imports import connection
#
#
# def _get_formatted(date):
#     return date.strftime('%Y-%m-%d')
#
#
# def week_data_for_stats():
#     print('week_data_for_stats')
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f'SELECT  SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
#             f'WHERE yearweek(CURDATE()) = yearweek(date_time) '
#             f'GROUP BY CAST(date_time AS DATE) '
#             f'ORDER BY date_time ASC'
#         )
#         rows = cursor.fetchall()
#     return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]
#
#
# def week_data_():
#     print('week_data_for_stats')
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f'SELECT SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM incomes '
#             f'WHERE yearweek(CURDATE()) = yearweek(date_time) '
#             f'GROUP BY CAST(date_time AS DATE) '
#             f'ORDER BY date_time ASC'
#         )
#         rows = cursor.fetchall()
#     return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]
#
#
# def month_data_for_stats():
#     print('month_data_for_stats')
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f'SELECT  SUM(amount), CAST(date_time AS DATE) AS Date_, date_time FROM expenses '
#             f'WHERE MONTH(date_time)=MONTH(CURDATE())'
#             f'and YEAR(date_time)=YEAR(CURDATE())'
#             f'GROUP BY CAST(date_time AS DATE) '
#             f'ORDER BY date_time ASC'
#         )
#         rows = cursor.fetchall()
#     return [i[0] for i in rows], [_get_formatted(j[1]) for j in rows]
#
#
# def create_diagram_for_stats(values, dates, type_='jfgjf'):
#     print('create_diagram_for_stats')
#     x = np.arange(len(dates))
#
#
#
#     y = np.array(values)
#     fig, ax = plt.subplots(figsize=(10, 4))
#     plt.title(type_)
#     plt.xlabel("Date")
#     plt.ylabel("Amount")
#     plt.plot(x, y, 'o-')
#     ax.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
#     ax.set_xticklabels(dates, fontsize=10)
#     ax.xaxis.set_minor_locator(AutoMinorLocator())
#     ax.xaxis.set_major_locator(DayLocator())
#     fig.autofmt_xdate()
#     # plt.plot(week_data_()[0], week_data_()[1], 'o-')
#
#     plt.show()
#
#
# create_diagram_for_stats(week_data_for_stats()[0], week_data_for_stats()[1])

k = ['2021-12-19', '2021-12-20', '2021-12-21']
z = ['2021-12-19','2021-12-05']

# for i in z:
#     if i not in k:
#         k.append(i)
#
# k.append(str(i) for i in z if i not in k)
#
# print(k)