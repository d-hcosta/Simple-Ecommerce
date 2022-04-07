def format_price(val):
    return f'${val:.2f}'

def cart_total(cart):
    return sum([item['quantity']for item in cart.values()])

def sum_price_cart(cart):
    return sum(
        [
            item.get('quantitative_promotional_price')
            if item.get('quantitative_promotional_price')
            else item.get('quantitative_price')
            for item
            in cart.values()
        ]
    )