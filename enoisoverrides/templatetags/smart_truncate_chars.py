from django import template
# http://chriskief.com/2014/05/11/django-template-tag-for-truncating-characters-at-a-word-boundary/


register = template.Library()

# truncate chars but leaving last word complete
@register.filter(name='smarttruncatechars')
def smart_truncate_chars(value, max_length):

    if len(value) > max_length:
        # limits the number of characters in value to max_length (blunt cut)
        truncd_val = value[:max_length]
        # check if the next upcoming character after the limit is not a space,
        # in which case it might be a word continuing
        if value[max_length] != ' ':
            # rfind will return the last index where matching the searched character,
            # in this case we are looking for the last space
            # then we only return the number of character up to that last space
            truncd_val = truncd_val[:truncd_val.rfind(' ')]

        return truncd_val + '...'

    return value
