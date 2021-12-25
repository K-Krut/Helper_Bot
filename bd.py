import requests, pymysql
from bs4 import BeautifulSoup
from config import connection


def get_info(book_info):
    url = []
    data = {}
    r = requests.get('https://www.yakaboo.ua/search/?multi=0&cat=&q=' + book_info)
    html_main = BeautifulSoup(r.text, features="html.parser")
    quote_main = html_main.find('ul',
                                class_="products-grid thumbnails thumbnails_horizontal thumbnails_middle data-list")
    if quote_main:
        r = requests.get(quote_main.find_all('li')[0].find('a').get('href'))
        html_main = BeautifulSoup(r.text, features="html.parser")
    quote_book = html_main.find('table', id="product-attribute-specs-table")
    if not quote_book:
        return
    keys = ['Автор', 'Издательство', 'Язык', 'Год издания', 'Количество страниц']
    key = ''
    data['Название'] = html_main.find('div', class_="big-description block translate").find('span').text
    data['Код'] = int(html_main.find('div', class_="product-sku").find('span', itemprop="sku").text)
    ind = False
    for q in quote_book.find_all('td'):
        if (ind):
            if q.find('a'):
                url.append(q.find('a').get('href'))
            data[key] = q.text.removeprefix(' ')
            ind = False
        if (q.text in keys):
            key = q.text
            ind = True
    for check in keys:
        if check not in data:
            data[check] = 'Нет информации'
    return [data, url]


def add_book(information, telegram_id):
    data = information[0]
    url = information[1]
    if data['Издательство'] == 'Нет информации':
        return False
    # connection = pymysql.connect(host="localhost", port=3306, user='root', password='Koll10000', database='library',
    #                              cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        if len(url) == 1:
            url.append(url[0])
        else:
            html_author = BeautifulSoup(requests.get(url[0]).text, features="html.parser")
            psevdo = html_author.find('div', class_="page-title category-title").find('h1').text.removesuffix(
                ' — книги и биография').removeprefix('    ')
            create_query = f"""SELECT psevdonim FROM Author WHERE psevdonim='{psevdo}';"""
            cursor.execute(create_query)
            if not cursor.fetchall():
                create_query = f"""INSERT INTO Author (psevdonim) VALUES('{psevdo}');"""
                cursor.execute(create_query)
                quote_author = html_author.find('div', class_="product-shop span6")
                if quote_author:
                    if len(quote_author.find_all('td')) > 2:
                        create_query = f"""UPDATE Author SET date_of_birth='{quote_author.find_all('td')[3].text}' WHERE psevdonim='{psevdo}';"""
                        cursor.execute(create_query)
                    create_query = f"""UPDATE Author SET author_description='{quote_author.find('p').text}' WHERE psevdonim='{psevdo}';"""
                    cursor.execute(create_query)

        html_publisher = BeautifulSoup(requests.get(url[1]).text, features="html.parser")
        publisher_name = html_publisher.find('div', class_="page-title category-title").find('h1').text.removeprefix(
            '    Издательство книг ')
        create_query = f"""SELECT publisher_name FROM Publisher WHERE publisher_name='{publisher_name}';"""
        cursor.execute(create_query)
        if not cursor.fetchall():
            create_query = f"""INSERT INTO Publisher (publisher_name) VALUES('{publisher_name}');"""
            cursor.execute(create_query)
            quote_publisher = html_publisher.find('div', class_="product-shop span9")
            if quote_publisher:
                create_query = f"""UPDATE Publisher SET publisher_description='{quote_publisher.find('p').text}' WHERE publisher_name='{publisher_name}';"""
                cursor.execute(create_query)

        connection.commit()

        create_query = f"""SELECT book_id FROM Books WHERE book_id={data['Код']};"""
        cursor.execute(create_query)
        if not cursor.fetchall():
            create_query = f"""INSERT INTO Books (book_id,title,author,publisher,book_language,year_of_publishing,amount_of_pages) VALUES({data['Код']},'{data['Название']}','{data['Автор']}','{data['Издательство']}','{data['Язык']}',{data['Год издания']},'{data['Количество страниц']}');"""
            cursor.execute(create_query)

        connection.commit()

        create_query = f"""SELECT user_id FROM LibraryUser WHERE telegram_id={telegram_id} AND book={data['Код']};"""
        cursor.execute(create_query)
        if cursor.fetchall():
            # connection.close()
            return False
        create_query = f"""INSERT INTO LibraryUser (book,telegram_id) VALUES({data['Код']},{telegram_id});"""
        cursor.execute(create_query)

        connection.commit()
    # connection.close()
    return True


def delete_book(book_id, telegram_id):
    # connection = pymysql.connect(host="localhost", port=3306, user='root', password='Koll10000', database='library',
    #                              cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        create_query = f"""SELECT book FROM LibraryUser WHERE book={book_id} AND telegram_id={telegram_id};"""
        cursor.execute(create_query)
        if not cursor.fetchall():
            # connection.close()
            return False
        create_query = f"""DELETE FROM LibraryUser WHERE book={book_id} AND telegram_id={telegram_id};"""
        cursor.execute(create_query)
        connection.commit()
        # connection.close()
        return True


def get_max_info(telegram_id):
    data = {}
    keys = [['Псевдоним', 'Дата рождения', 'Описание', 'Количество'], ['Название', 'Описание', 'Количество']]

    # connection = pymysql.connect(host="localhost", port=3306, user='root', password='Koll10000', database='library',
    #                              cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:

        create_query = f"""SELECT psevdonim,date_of_birth,author_description,COUNT(telegram_id) AS amount FROM LibraryUser LEFT OUTER JOIN (SELECT book_id,psevdonim,date_of_birth,author_description FROM Books LEFT OUTER JOIN Author ON psevdonim=author) AS Psevdo ON book_id=book WHERE telegram_id={telegram_id} GROUP BY psevdonim ORDER BY amount DESC LIMIT 3;"""
        cursor.execute(create_query)
        rows = cursor.fetchall()
        if not rows:
            data['Топ 3 ваших автора'] = 'Твой список пуст'
        else:
            string = ''
            for row in rows:
                string += '--' * 29 + '\nАвтор:\n'

                author_info = '\n'.join(str(item) for item in row).split('\n')

                for i in range(len(author_info)):
                    string += keys[0][i] + ': ' + (
                        '-' if author_info[i] == 'None' or author_info[i] == 'Нет информации' else author_info[
                            i]) + '\n'

            data['Топ 3 ваших автора'] = string

        create_query = f"""SELECT publisher_name,publisher_description,COUNT(telegram_id) AS amount FROM LibraryUser LEFT OUTER JOIN (SELECT book_id,publisher_name,publisher_description FROM Books LEFT OUTER JOIN Publisher ON publisher_name=publisher) AS Publ ON book_id=book WHERE telegram_id={telegram_id} GROUP BY publisher_name ORDER BY amount DESC LIMIT 3;"""
        cursor.execute(create_query)
        rows = cursor.fetchall()
        if not rows:
            data['Топ 3 ваших издательcтва'] = 'Твой список пуст'
        else:
            string = ''
            for row in rows:
                string += '--' * 29 + '\nИздательство:\n'
                publisher_info = '\n'.join(str(item) for item in row).split('\n')
                for i in range(len(publisher_info)):
                    string += keys[1][i] + ': ' + (
                        '--' if publisher_info[i] == 'None' or publisher_info[i] == 'Нет информации' else
                        publisher_info[i]) + '\n'
            print(string)
            data['Топ 3 ваших издательтва'] = string
        # connection.close()
        return data


def get_list(telegram_id):
    string = ''
    keys = ['Код', 'Название', 'Автор', 'Издательство', 'Язык', 'Год издания', 'Количество страниц']

    # connection = pymysql.connect(host="localhost", port=3306, user='root', password='Koll10000', database='library',
    #                              cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        create_query = f"""SELECT book FROM LibraryUser WHERE telegram_id={telegram_id};"""
        cursor.execute(create_query)
        if not cursor.fetchall():
            # connection.close()
            return 'Твой список пуст'
        create_query = f"""SELECT book_id,title,author,publisher,book_language,year_of_publishing,amount_of_pages 
		FROM LibraryUser LEFT OUTER JOIN Books ON book_id=book WHERE telegram_id={telegram_id};"""
        cursor.execute(create_query)
        rows = cursor.fetchall()
        for row in rows:
            string += '--' * 29 + '\nКнига:\n'
            book_info = '\n'.join(str(item) for item in row).split('\n')
            for i in range(len(keys)):
                string += keys[i] + ': ' + book_info[i] + '\n'
    # connection.close()
    return string
