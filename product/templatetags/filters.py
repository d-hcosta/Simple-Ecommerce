from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_price(val):
    return utils.format_price(val)

@register.filter
def cart_total(cart):
    return utils.cart_total(cart)

@register.filter
def sum_price_cart(cart):
    return utils.sum_price_cart(cart)