from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProducts.as_view(), name="list"),
    path('<slug>', views.ProductDetails.as_view(), name="details"),
    path('addtocart/', views.AddToCart.as_view(), name="addtocart"),
    path('removefromcart/', views.RemoveFromCart.as_view(),
        name="removefromcart"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('resume/', views.Resume.as_view(), name="resume"),
    path('search/', views.Search.as_view(), name="search"),
]