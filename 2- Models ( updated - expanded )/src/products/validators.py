from django.core.exceptions import ValidationError


BLOCK_LIST = ['FUCK', 'SHIT', 'Omar']

# 1- Clear input and Block list
# 2- Sum
# 3- if has error
# 4- iterate invalid items


def block(value):
    # 1- Clear input and Block list
    init_value = f"{value}".lower()
    init_items = set(init_value.split())
    block_list = set(x.lower() for x in BLOCK_LIST)

    # 2- Sum
    valid_words = list(init_items & block_list)
    has_error = len(valid_words) > 0

    # 3- if has error
    if has_error:
        invalid_items = []
        # 4- iterate invalid items
        for i, word in enumerate(valid_words):
            invalid_items.append(ValidationError("%(value)s is word blocked", params={
                                 'value': word}, code=f"blocked-word-{i}"))
        raise ValidationError(invalid_items)

    return value
