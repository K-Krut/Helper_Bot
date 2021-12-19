class AddCategoryError(Exception):
    def __init__(self, category, error_message='Incorrect category input'):
        self._category = category
        self._error_message = error_message
        super().__init__(self._error_message)

    def __str__(self):
        return f'{self._error_message}:\n{self._category} does not much the format:\n' \
               f'`products: products, food, eat`'


class AddExpenseError(Exception):
    def __init__(self, expense, error_message='Incorrect expense input'):
        self._expense = expense
        self._error_message = error_message
        super().__init__(self._error_message)

    def __str__(self):
        return f'{self._error_message}:\n{self._category} does not much the format: `125 taxi`'


class AddIncomeError(Exception):
    def __init__(self, income, error_message='Incorrect income input'):
        self._income = income
        self._error_message = error_message
        super().__init__(self._error_message)

    def __str__(self):
        return f'{self._error_message}:\n{self._category} does not much the format: `125 job`'
