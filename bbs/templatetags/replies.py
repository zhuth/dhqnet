from django.template import Library

register = Library()

@register.inclusion_tag('show_levels.html')
def show_levels(post):
    return {'post': post}