from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.Create.as_view(), name="create"),
    path('actualize/', views.Actualize.as_view(), name="actualize"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
]