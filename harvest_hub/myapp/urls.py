from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('inventory/', views.inventory_view, name='inventory'),
    path('sales/', views.sales_view, name='sales'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),

    path('digital-market/', views.market_view, name='digital_market'),
    path('contact/', views.contact_view, name='contact'),

    path('upload-product/', views.upload_product_view, name='upload_product'),
    path('product/delete/<int:product_id>/', views.delete_product_view, name='delete_product'),

]
