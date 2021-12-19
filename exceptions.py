class AddCategoryError(Exception):
    def __init__(self, category, error_message='Incorrect category input'):
        self._category = category
        self._error_message = error_message
        super().__init__(self._error_message)

    def __str__(self):
        return f'{self._error_message}:\n{self._category} does not much the format:\n' \
               f'products: products, food, eat'
