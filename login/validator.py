from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator():

    def __init__(self):
        self.min_length = 1

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Su contraseña debe contener al menos un número.'))
        # if not any(char.isalpha() for char in password):
        #     raise ValidationError(_('Su contraseña debe contener al menos %(min_length)d letter.') % {'min_length': self.min_length})
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Su contraseña debe contener al menos un caracter especial.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Su contraseña debe contener al menos una letra mayúscula.'))
        if not any(char.islower() for char in password):
            raise ValidationError(_('Su contraseña no debe ser completamente en mayúsculas'))

    def get_help_text(self):
        return 'Su contraseña debe contener al menos una letra mayúscula y un caracter especial.'