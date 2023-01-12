from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    stopword = ['культура', 'нюхать', 'зал', 'конец']
    if type(value) is str:
        for word in stopword:
            value = value.replace(word, word[0] + "*" * (len(word) - 1))
            value = value.replace(word.capitalize(), word[0] + "*" * (len(word) - 1))
    else:
        raise ValueError('Требуется строка')

    return value