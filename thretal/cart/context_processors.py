from cart.models import Cart

from cart.models import Cart

def cart_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum(i.quantity for i in cart_items)
        cart_total = sum(i.quantity * i.product.price for i in cart_items)
    else:
        cart_items = []
        cart_count = 0
        cart_total = 0

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total
    }

