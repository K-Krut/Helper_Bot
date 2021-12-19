import pymysql

connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Varta4899",
    db='finance'
)


def insert(table, column_values):
    columns = ', '.join(column_values.keys())
    values = [tuple(i for i in column_values.values())]
    placeholders = '%s' + ', %s' * (len(column_values) - 1)
    with connection.cursor() as cursor:
        cursor.executemany(
            f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values
        )
        connection.commit()


def fetchall_(table, columns):
    print(f'COLOMNS {columns}')
    columns_joined = ", ".join(columns)
    print(f'COLOMNS {columns_joined}')
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


def delete(table, row, value):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table} WHERE {row}='{value}'")
        connection.commit()

# delete('category', 'code_name', 'other_')
# delete('category', 'code_name', 'dinner_')