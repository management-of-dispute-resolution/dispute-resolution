import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from api.api_consts import ERROR_MESSAGE, VALIDATION_MESSAGE


class UniquePasswordValidator(BaseValidator):
    """
    Check the new password and the current password.

    This validator checks if the new password
    matches the current password of the user.
    If they match, a ValidationError is raised.
    """

    def __init__(self, limit_value=1, *args, **kwargs):
        """
        Initialize the UniquePasswordValidator.

        Args:
            limit_value (int): The number of similar passwords
            to check against (default is 1).
        """
        super().__init__(limit_value, *args, **kwargs)

    def validate(self, password, user=None):
        """
        Validate the new password against the current password.

        Args:
            password (str): The new password to validate.
            user: The user object associated with the password
            (default is None).

        Raises:
            ValidationError: If the new password is
            the same as the current password.
        """
        if user and user.check_password(password):
            raise ValidationError(
                (ERROR_MESSAGE),
                code='password_reuse',
            )

        if not re.fullmatch(r'[A-Za-z0-9@№:;~#$%^!<>&+,.?/\\`()*|\-=]{8,32}',
                            password):
            raise ValidationError(VALIDATION_MESSAGE)

    def get_help_text(self):
        """Return a help text describing the validation rule."""
        return (ERROR_MESSAGE)
