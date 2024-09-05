# urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.book_catering, name='book_catering'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('contact/', views.contact_us, name='contact_us'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('order-history/', views.order_history, name='order_history'),
    path('generate-bill/<int:booking_id>/', views.generate_bill, name='generate_bill'),
    path('calendar/', views.calendar_view, name='calendar_view'),
]
