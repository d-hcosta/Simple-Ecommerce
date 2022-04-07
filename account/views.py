from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy
from . import models, forms

class AccountBase(View):
    template_name = 'account/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        self.account = None

        if self.request.user.is_authenticated:
            self.account = models.Account.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'accountform': forms.AccountForm(
                    data=self.request.POST or None,
                    instance=self.account
                ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'accountform': forms.AccountForm(
                    data=self.request.POST or None
                ),
            }

        self.userform = self.context['userform']
        self.accountform = self.context['accountform']

        if self.request.user.is_authenticated:
            self.template_name = 'account/actualize.html'

        self.renderer = render(self.request, self.template_name, self.context)


    def get(self, *args, **kwargs):
        return self.renderer

class Create(AccountBase):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.accountform.is_valid():
            messages.error(
                self.request,
                'There are errors in the registration form. '
                'Check that all fields are filled in correctly.'
            )

            return self.renderer
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User, username=self.request.user.username)

            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.account:
                self.accountform.cleaned_data['user'] = user
                print(self.accountform.cleaned_data)
                account = models.Account(**self.accountform.cleaned_data)
                account.save()
            else:
                account = self.accountform.save(commit=False)
                account.user = user
                account.save()
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            account = self.accountform.save(commit=False)
            account.user = user
            account.save()

        if password:
            authentication = authenticate(
                self.request,
                username=user,
                password=password
            )

            if authentication:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Your account has been successfully created or updated.'
        )

        messages.success(
            self.request,
            'You are logged in and can complete your purchase.'
        ) 

        return redirect('product:cart')
        return self.renderer

class Actualize(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Actualize')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Invalid username or password.')
            return redirect('account:create')

        user = authenticate(
            self.request, username=username, password=password)

        if not user:
            messages.error(self.request, 'Invalid username or password.')
            return redirect('account:create')
        
        login(self.request, user=user)
        messages.success(self.request, 'You have been successfully logged in.')
        return redirect('product:cart')        


class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')