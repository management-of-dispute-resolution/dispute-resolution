from django.core.validators import RegexValidator


def phone_number_validator():
    """Check the phone_number."""
    return RegexValidator(
        regex=r'''^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[
                    \s\-]?[0-9]{2}[\s\-]?[0-9]{2}$''',
        message='''Номер телефона может начинаться только с 7, +7, 8 и
                разделители только "-" или пробел.''',
    )
