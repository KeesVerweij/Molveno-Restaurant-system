from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\].,]"
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('The Password must contain at least 1 digit.'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('The Password must contain at least 1 letter.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('The Password must contain at least 1 Capital letter.'))
        if not any(char in special_characters for char in password):
            raise ValidationError(_('The Password must contain at least 1 special character.') % {'min_length': self.min_length})
        if len(password) < self.min_length:
            raise ValidationError(_('The Password must contain at least %(min_length)d characters.') % {'min_length': self.min_length})


    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters, 1 number, 1 letter, 1 special character and 1 Capital letter."
            % {'min_length': self.min_length}
        )
