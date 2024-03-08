# Create a custom template filter in your Django app (e.g., myapp/templatetags/custom_filters.py)

from django import template

register = template.Library()

@register.filter
def truncate_words(value, max_words):
    words = value.split()
    if len(words) > max_words:
        words = words[:max_words]
        words.append('...')  # Add an ellipsis to indicate truncated text
    return ' '.join(words)
