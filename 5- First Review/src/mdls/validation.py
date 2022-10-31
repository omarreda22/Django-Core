from django.core.exceptions import ValidationError


def not_omar_in(value):
    if 'omar' not in value:
        return value
    else:
        raise ValidationError("You Must don't have 'Omar' in Title field")


BLOCK_WORD = ['Fuck', 'Shit']


def blocks(value):
    init_value = f'{value}'.lower()
    init_items = set(init_value.split())
    init_blocks = set(x.lower() for x in BLOCK_WORD)

    valid_words = list(init_items & init_blocks)
    is_error = len(valid_words) > 0

    if is_error:
        invalid_items = []
        for i, ward in enumerate(valid_words):
            invalid_items.append(ValidationError("%(value)s is blocked ward", params={
                                 'value': ward}, code=f"blocked-word={i}"))

        raise ValidationError(invalid_items)
