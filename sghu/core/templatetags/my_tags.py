from django import template
from django.contrib.auth.models import Group

register = template.Library()



@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()