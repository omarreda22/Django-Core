from django.core.exceptions import ValidationError


def validate_for_email(value):
    if '@' in value:
        return value
    else:
        raise ValidationError('You Must Put Email Here!!')


def validate_for_omar(value):
    if 'omar' not in value:
        return value
    else:
        raise ValidationError("You Must Don't have 'omar' in email")
