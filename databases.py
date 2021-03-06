from config import connection


def insert(table, column_values):
    print(column_values)
    columns = ', '.join(column_values.keys())
    values = [tuple(i for i in column_values.values())]
    placeholders = '%s' + ', %s' * (len(column_values) - 1)
    with connection.cursor() as cursor:
        cursor.executemany(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values)
        connection.commit()


def fetchall_(table, columns):
    columns_joined = ", ".join(columns)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = cursor.fetchall()
    result_ = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result_.append(dict_row)
    return result_


def fetchone_for_budget(table, columns, condition):
    columns_joined = ", ".join(columns)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {condition}")
        return cursor.fetchone()[0]


def delete(table, row, value):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table} WHERE {row}='{value}'")
        connection.commit()


def update_(table, data, condition):
    columns = ', '.join([f'{i} = %s' for i in data])
    values = [[i] for i in data.values()]
    print(f'UPDATE {table} SET {columns} WHERE {condition}')
    with connection.cursor() as cursor:
        cursor.execute(f'UPDATE {table} SET {columns} WHERE {condition}', values)
        connection.commit()
