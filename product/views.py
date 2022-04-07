from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from account.models import Account
from . import models

class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']

class ProductDetails(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug = slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                "Product doesn't exist."  
            )
            return redirect(http_referer)
        
        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_inventory = variation.inventory

        product = variation.product
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        unit_promotional_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.inventory < 1:
            messages.error(
                self.request,
                "Insufficient stock."
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            quantity += 1

            if variation_inventory < cart_quantity:
                messages.warning(
                    self.request,
                    f'Insufficient stock for {cart_quantity} in product '
                    f'"{product_name}". We add {variation_inventory} in your cart.'
                )
                cart_quantity = variation_inventory
            
            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['quantitative_promotional_price'] = unit_promotional_price * cart_quantity
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'unit_promotional_price': unit_promotional_price,
                'quantitative_price': unit_price,
                'quantitative_promotional_price': unit_promotional_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }
        
        self.request.session.save()

        messages.success(
            self.request,
            f'Product {product_name} {variation_name} added to your cart '
            f'{cart[variation_id]["quantity"]}x'
        )
        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)
        
        cart = self.request.session['cart'][variation_id]
        
        messages.success(
            self.request,
            f'Product {cart["product_name"]} {cart["variation_name"]}'
            f' removed.')
        
        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        
        return render(self.request, 'product/cart.html', context)

class Resume(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:create')
        
        account = Account.objects.filter(user=self.request.user).exists()
        if not account:
            messages.error(self.request, 'This user does not have an account.')
            return redirect('account:create')
        

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Empty cart.')
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'product/resume.html', context)