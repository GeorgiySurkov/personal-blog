from wtforms import ValidationError
from string import ascii_lowercase, digits


class UsernameValidator:
    def __init__(self, message=None):
        if message is None:
            message = 'Имя пользователя должно состоять из строчных латинских букв,' \
                      ' цифр, нижнего подчеркивания или точки'
        self.message = message
        self._charset = frozenset(ascii_lowercase + digits + '_.')

    def __call__(self, form, field):
        for char in field.data:
            if char not in self._charset:
                raise ValidationError(self.message)
