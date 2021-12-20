import pytz

from imports import *
from exceptions import *
import databases as db


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        categories = db.fetchall_("category", "code_name category_name aliases_".split())
        categories = self._fill_aliases(categories)
        return categories

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

    def get_all_categories(self):
        return self._categories

    def get_category(self, category_name):
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other_":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded


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
    ###################################################################################################################
    # amount = regexp_result.group(1).replace(" ", "")
    # category_text = regexp_result.group(2).strip().lower()
    return Message(amount=int(regexp.group(1).replace(" ", "")), category_text=regexp.group(2).strip().lower())


def _parse_budget_message(message):
    # regexp_ = re.match(r'daily ([1-9]([0-9]){0,10}) month ([1-9]([0-9]){0,10})', message)
    regexp_ = re.match(r'(daily) ([1-9]([0-9]){0,10}) (month) ([1-9]([0-9]){0,10})',
                       str(message).lower().replace("  ", " "))
    print(f'{regexp_.group(1)}, {regexp_.group(2)}, {regexp_.group(4)}, {regexp_.group(5)}')
    # if not (regexp_.group(1) and regexp_.group(2)) or (regexp_.group(4) and regexp_.group(5)):
    if not regexp_.group(0):
        raise ChangeBudgetError('SOENENE=ENENE')
    print(str(message))
    return BudgetMessage(daily_amount=int(regexp_.group(2)), month_amount=int(regexp_.group(5)))


def add_expense(message):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert(
        "expenses",
        {
            "amount": parsed_message.amount,
            "date_time": _get_now_formatted(),
            "category": category.codename
        }
    )
    return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def edit_budget(message):
    parsed_message = _parse_budget_message(message)
    db.update_(
        "budget", {
            'daily_limit': parsed_message.daily_amount,
            'month_limit': parsed_message.month_amount
        },
        "code_name = 'general'"
    )


def add_incomes(message):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert(
        "incomes",
        {
            "amount": parsed_message.amount,
            "date_time": _get_now_formatted(),
            "category": category.codename
        }
    )
    return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def create_category_finance(message):
    print(message)
    parsed_data = _parse_category(message)
    db.insert(
        "category", {
            'code_name': parsed_data.name_ + '_',
            'category_name': parsed_data.name_,
            'aliases_': parsed_data.category_text
        }
    )
    return CreateCategory(code_name_=parsed_data[0] + '_', category_name_=parsed_data[0], aliases_text_=parsed_data[1])


def delete_expense(row_id):
    with connection.cursor() as cursor:
        row_id = int(row_id)
        cursor.execute(f"delete from expenses where expense_id={row_id}")
        connection.commit()


def _get_now_formatted():
    return _get_now_datetime().strftime('%Y-%m-%d %H:%M:%S')


def _get_now_datetime():
    return datetime.datetime.now()


def get_budget_month_limit():
    print(db.fetchall_('budget', ['month_limit'])[0]['month_limit'])
    return db.fetchall_('budget', ['month_limit'])[0]['month_limit']


def get_budget_daily_limit():
    print(db.fetchall_('budget', ['daily_limit'])[0]['daily_limit'])
    return db.fetchall_('budget', ['daily_limit'])[0]['daily_limit']

#
# def last() -> List[Expense]:
#     """Возвращает последние несколько расходов"""
#     cursor = db.get_cursor()
#     cursor.execute(
#         "select e.id, e.amount, c.name "
#         "from expense e left join category c "
#         "on c.codename=e.category_codename "
#         "order by created desc limit 10")
#     rows = cursor.fetchall()
#     last_expenses = [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
#     return last_expenses


def today_expenses():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE CAST(date_time AS DATE) = CAST(CURDATE() AS DATE)'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_week_expenses():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE yearweek(CURDATE()) = yearweek(date_time)'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_month_expenses():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.expense_id, a.amount, b.category_name '
            f'FROM expenses a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE MONTH(date_time)=MONTH(CURDATE())'
            f'and YEAR(date_time)=YEAR(CURDATE());'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def today_incomes():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE CAST(date_time AS DATE) = CAST(CURDATE() AS DATE)'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_week_incomes():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE yearweek(CURDATE()) = yearweek(date_time)'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]


def this_month_incomes():
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT a.income_id, a.amount, b.category_name '
            f'FROM incomes a LEFT JOIN category b ON b.code_name=a.category '
            f'WHERE MONTH(date_time)=MONTH(CURDATE())'
            f'and YEAR(date_time)=YEAR(CURDATE());'
        )
        rows = cursor.fetchall()
    return [IncomeExpense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
