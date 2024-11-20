from django import template
import re

register = template.Library()

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Censor filter can only be applied to strings.")
    censored_words = ['редиска']  # Добавьте сюда нежелательные слова
    pattern = re.compile(r'\b(' + '|'.join(censored_words) + r')\b', re.IGNORECASE)
    return pattern.sub(lambda x: x.group()[0] + '*' * (len(x.group()) - 1), value)