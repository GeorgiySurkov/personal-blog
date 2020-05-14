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


class TagValidator:
    def __init__(self, amount_err_message=None, name_err_message=None):
        if amount_err_message is None:
            amount_err_message = 'У поста не может быть больше 10 тегов'
        self.amount_err_message = amount_err_message
        if name_err_message is None:
            name_err_message = 'В теге не может быть больше 3 слов'
        self.name_err_message = name_err_message

    def __call__(self, form, field):
        tags = field.data.split(',')
        if len(tags) > 10:
            raise ValidationError(self.amount_err_message)
        for tag in map(str.strip, tags):
            tag_words = tag.split()
            if len(tag_words) > 3:
                raise ValidationError(self.name_err_message)
