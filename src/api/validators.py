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


class MaximumLengthValidator(object):
    """Validate whether the password is of a maximum length."""

    def __init__(self, max_length=32):
        """
        Initialize the MaximumLengthValidator.

        Args:
            max_length (int): The maximum allowed length
            for the password (default is 32).
        """
        self.max_length = max_length

    def validate(self, password, user=None):
        """
        Validate the length of the password.

        Args:
            password (str): The password to validate.
            user: The user object associated with the password
            (default is None).

        Raises:
            ValidationError: If the password length exceeds
            the maximum allowed length.
        """
        if len(password) > self.max_length:
            raise ValidationError(
                "This password is too long."
                "It must contain at most {} character{}.".format(
                    self.max_length, 's' if self.max_length > 1 else ''
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        """Return a help text describing the maximum length validation rule."""
        return "Your password must contain at most {} character{}.".format(
            self.max_length, 's' if self.max_length > 1 else ''
        )
