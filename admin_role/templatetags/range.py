from django import template

register = template.Library()
@register.filter
def times(number):
    return range(number)

@register.filter
def times1(number):
    return range(5-number)

@register.filter
def mul(v1, v2):
    return v1  * (100-v2)//100

@register.filter
def eql(v1,v2):
    # if int(v1*(100-v2)/100)==int(v1):
    if v1==v2 : 
        return 0
    else:
        return 1
