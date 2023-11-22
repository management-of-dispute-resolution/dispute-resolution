from django.core.validators import RegexValidator


def text_validator():
    """Check the text."""
    return RegexValidator(
        regex=r'''^[A-Za-zа-яА-Я0-9_-]*$''',
        message='''Текст может быть только на латинице и кириллице''',
    )
