from django.core.validators import RegexValidator


def text_validator():
    """Check the text."""
    return RegexValidator(
        regex=r'^[A-Za-zА-Яа-я0-9\s\W]+$',
        message='''Текст может быть только на латинице и кириллице''',
    )
