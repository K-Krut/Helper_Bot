from typing import NamedTuple, List, Optional

from imports import *
from exceptions import *
import databases as db


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        return self._fill_aliases(db.fetchall_("category", "code_name category_name aliases_".split()))
        # categories = db.fetchall_("category", "code_name category_name aliases_".split())
        # categories = self._fill_aliases(categories)
        # return categories

    def _fill_aliases(self, categories):
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases_"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["code_name"])
            aliases.append(category["category_name"])
            categories_result.append(
                Category(codename=category['code_name'], name=category['category_name'], aliases=aliases)
            )
        return categories_result

    @property
    def get_all_categories(self):
        return self._categories

    def get_category(self, category_name):
        category_finded = None
        others = None
        for category in self._categories:
            if category.codename == "other_":
                others = category
            for alias in category.aliases:
                if category_name in alias:
                    category_finded = category
        if not category_finded:
            category_finded = others
        return category_finded


class CreateCategory(NamedTuple):
    code_name_: str
    category_name_: str
    aliases_text_: str


class CategoryMessage(NamedTuple):
    name_: str
    category_text: str


class Category(NamedTuple):
    codename: str
    name: str
    aliases: List[str]


class Message(NamedTuple):
    amount: int
    category_text: str


class BudgetMessage(NamedTuple):
    daily_amount: int
    month_amount: int


class IncomeExpense(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


class UserData(NamedTuple):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


def _parse_user_data(message):
    return UserData(
        id=str(message['id']), first_name=message['first_name'], last_name=message['last_name'],
        username=message['username']
    )


def _parse_category(message):
    regexp_ = re.match(r'^([a-z]+: )([a-z]+, ){1,7}([a-z]+)', str(message))
    if not regexp_ or not regexp_.group(0):
        raise AddCategoryError(str(message))
    reg_str = str(regexp_.group(0)).split(': ')
    return CategoryMessage(name_=reg_str[0], category_text=reg_str[1])


def _parse_message(message):
    regexp = re.match(r"([\d ]+) (.*)", message)
    print(f'PARSE {regexp} -> {regexp.group(0)} -> {regexp.group(1)} -> {regexp.group(2)}')
    if not regexp or not regexp.group(0) \
            or not regexp.group(1) or not regexp.group(2):
        raise AddCategoryError(str(message))
    return Message(amount=int(regexp.group(1).replace(" ", "")), category_text=regexp.group(2).strip().lower())


def _parse_budget_message(message):
    regexp_ = re.match(r'(daily) ([1-9]([0-9]){0,10}) (month) ([1-9]([0-9]){0,10})',
                       str(message).lower().replace("  ", " "))
    print(f'{regexp_.group(1)}, {regexp_.group(2)}, {regexp_.group(4)}, {regexp_.group(5)}')
    # if not (regexp_.group(1) and regexp_.group(2)) or (regexp_.group(4) and regexp_.group(5)):
    if not regexp_.group(0):
        raise ChangeBudgetError(str(message))
    return BudgetMessage(daily_amount=int(regexp_.group(2)), month_amount=int(regexp_.group(5)))


def check_user_exists(user_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    return bool(cursor.rowcount)


def add_user(message):
    user_info = _parse_user_data(message)
    db.insert(
        "users",
        {
            "id": user_info.id,
            "first_name": user_info.first_name,
            "last_name": user_info.last_name,
            "username": user_info.username
        }
    )


def add_expense(message, user_id):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert(
        "expenses",
        {
            "amount": parsed_message.amount,
            "date_time": _get_now_formatted(),
            "category": category.codename,
            "user_id": str(user_id)
        }
    )
    return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def edit_budget(message, user_id):
    parsed_message = _parse_budget_message(message)
    db.update_(
        "budget", {
            'daily_limit': parsed_message.daily_amount,
            'month_limit': parsed_message.month_amount,
            'user_id': str(user_id)
        },
        f"code_name = 'general' AND user_id = {user_id}"
    )


def add_incomes(message, user_id):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert(
        "incomes",
        {
            "amount": parsed_message.amount,
            "date_time": _get_now_formatted(),
            "category": category.codename,
            "user_id": str(user_id)
        }
    )
    return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def create_category_finance(message, user_id):
    print(message)
    parsed_data = _parse_category(message)
    db.insert(
        "category", {
            'code_name': parsed_data.name_ + '_',
            'category_name': parsed_data.name_,
            'aliases_': parsed_data.category_text,
            'user_id': str(user_id)
        }
    )
    return CreateCategory(code_name_=parsed_data[0] + '_', category_name_=parsed_data[0], aliases_text_=parsed_data[1])


def see_categories(user_id):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT category_name, aliases_ FROM category WHERE user_id = {str(user_id)}')
        rows = cursor.fetchall()
    return [CategoryMessage(name_=row[0], category_text=row[1]) for row in rows]


def delete_expense(row_id, user_id):
    with connection.cursor() as cursor:
        row_id = int(row_id)
        cursor.execute(f"DELETE FROM expenses WHERE expense_id = {row_id} AND user_id = {user_id}")
        connection.commit()


def delete_income(row_id, user_id):
    with connection.cursor() as cursor:
        row_id = int(row_id)
        cursor.execute(f"DELETE FROM incomes WHERE income_id = {row_id} AND user_id = {user_id}")
        connection.commit()


def _get_now_formatted():
    return _get_now_datetime().strftime('%Y-%m-%d %H:%M:%S')


def _get_now_datetime():
    return datetime.datetime.now()


def set_default_budget(user_id):
    with connection.cursor() as cursor:
        cursor.execute(f'INSERT INTO budget (daily_limit, month_limit, user_id) VALUES (0, 0, {str(user_id)})')
        connection.commit()


def get_budget_month_limit(user_id):
    print(f"{['month_limit']} {user_id}")
    return db.fetchone_for_budget('budget', f"month_limit".split(), f'user_id = {user_id}')


def get_budget_daily_limit(user_id):
    print(f"{['daily_limit']} {user_id}")
    return db.fetchone_for_budget('budget', f"daily_limit".split(), f'user_id = {user_id}')


def today_expenses(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (CAST(date_time AS DATE) = CAST(CURDATE() AS DATE) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_week_expenses(user_id):
    print('this_week_expenses')
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (YEARWEEK(CURDATE()) = YEARWEEK(date_time) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
        print(rows)
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_month_expenses(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (MONTH(date_time) = MONTH(CURDATE()) AND '
            f'YEAR(date_time) = YEAR(CURDATE()) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def today_incomes(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (CAST(date_time AS DATE) = CAST(CURDATE() AS DATE) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_week_incomes(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (YEARWEEK(CURDATE()) = YEARWEEK(date_time) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_month_incomes(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category AND a.user_id = b.user_id '
            f'WHERE (MONTH(date_time)=MONTH(CURDATE()) AND '
            f'YEAR(date_time)=YEAR(CURDATE()) AND a.user_id = {str(user_id)})'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
