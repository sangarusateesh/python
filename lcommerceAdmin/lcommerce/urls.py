from django.urls import path
from . import views

app_name = 'lcommerce'

urlpatterns = [
    path('hello/', views.say_hello),
    path('login/', views.login),
    path('loginUser/',views.loginUser),
    path('sign_up/',views.sign_up),
    path('OrderDetails',views.OrderDetails),
    path('check_mysql_connection/', views.check_mysql_connection),
    path('register_user/', views.register_user,  name='register_user')
]