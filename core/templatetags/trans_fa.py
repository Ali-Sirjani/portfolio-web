from django.template import library

register = library.Library()


@register.filter
def num_fa(value):
    if value:
        persian = '۰١٢٣۴۵٦٧٨٩'
        engilish = '0123456789'
        try:
            value = str(f'{value:,}')
        except ValueError:
            pass

        trans_table = str.maketrans(engilish, persian)
        translated_value = value.translate(trans_table)

        return translated_value

    return value
