from lepl.apps.rfc3696 import Email as EmailValidator
from wtforms.validators import ValidationError


class Email(object):
    def __init__(self):
        self._validate = EmailValidator()

    def __call__(self, form, field):
        email = field.data
        if email and not self._validate(email):
            raise ValidationError('Invalid email address.')
