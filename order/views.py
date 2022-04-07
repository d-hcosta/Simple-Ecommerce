from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from product.models import Variation
from utils import utils
from .models import Order, OrderItem

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:create')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'



class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged.')
            return redirect('account:create')
        
        if not self.request.session.get('cart'):
            messages.error(self.request, 'Empty cart.')
            return redirect('product:list')

        cart = self.request.session.get('cart')
        id_var_cart = [v for v in cart]
        db_variation = list(
            Variation.objects.select_related('product').filter(
                id__in=id_var_cart))

        for variation in db_variation:
            vid = str(variation.id)
            inventory = variation.inventory
            cart_quantity = cart[vid]['quantity']
            unit_p = cart[vid]['unit_price']
            unity_promo_p = cart[vid]['unit_promotional_price']

            error_stock = ''

            if inventory < cart_quantity:
                cart[vid]['quantity'] = inventory
                cart[vid]['quantitative_price'] = inventory * unit_p
                cart[vid]['unit_promotional_price'] = inventory * unity_promo_p
                error_stock = 'Some products are out of stock. Check which ones are affected.'

            if error_stock:
                messages.error(
                    self.request,
                    error_stock
                )
                self.request.session.save()
                return redirect('product:cart')

        qty_total_cart = utils.cart_total(cart)
        value_total_cart = utils.sum_price_cart(cart)

        order = Order(
            user=self.request.user,
            total=value_total_cart,
            qty_total=qty_total_cart,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    id_product=v['product_id'],
                    variation=v['variation_name'],
                    id_variation=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['quantitative_promotional_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                    
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']
        return redirect(reverse('order:pay', kwargs={'pk':order.pk}))

class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order' 
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'

class List(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders' 
    template_name = 'order/list.html'
    paginated_by = 10
    ordering = ['-id']