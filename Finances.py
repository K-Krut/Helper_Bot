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


def _parse_message(raw_message):
    regexp = re.match(r"([\d ]+) (.*)", raw_message)
    print(f'PARSE {regexp} -> {regexp.group(0)} -> {regexp.group(1)} -> {regexp.group(2)}')
    if not regexp or not regexp.group(0) \
            or not regexp.group(1) or not regexp.group(2):
        raise AddCategoryError('_parse_message for expense/income')
    # amount = regexp_result.group(1).replace(" ", "")
    # category_text = regexp_result.group(2).strip().lower()
    return Message(
        amount=int(regexp.group(1).replace(" ", "")), category_text=regexp.group(2).strip().lower()
    )


def add_expense(message):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert("expenses", {
        "amount": parsed_message.amount,
        "date_time": _get_now_formatted(),
        "category": category.codename
    })
    # return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def add_income(message):
    parsed_message = _parse_message(message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert("incomes", {
        "amount": parsed_message.amount,
        "date_time": _get_now_formatted(),
        "category": category.codename
    })
    # return IncomeExpense(id=None, amount=parsed_message.amount, category_name=category.name)


def delete_expense(row_id):
    db.delete("expense", row_id)


def _get_now_formatted():
    return _get_now_datetime().strftime('%Y-%m-%d %H:%M:%S')


def _get_now_datetime():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    return now


def get_budget_month_limit():
    print(db.fetchall_('budget', 'month_limit')[0]['month_limit'])
    return db.fetchall_('budget', 'month_limit')[0]['month_limit']


def get_budget_daily_limit():
    print(db.fetchall_('budget', 'daily_limit')[0]['daily_limit'])
    return db.fetchall_('budget', 'daily_limit')[0]['daily_limit']


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
    return CreateCategory(code_name_=parsed_data[0] + '_', category_name_=parsed_data[0],
                          aliases_text_=parsed_data[1])


