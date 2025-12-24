from django.contrib import admin
from .models import Product, Profile


# -------------------------------------------------------
# PROFILE ADMIN
# -------------------------------------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'category')
    list_filter = ('category',)
    search_fields = ('user__username', 'mobile', 'category')
    readonly_fields = ('user',)


# -------------------------------------------------------
# PRODUCT ADMIN
# -------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'user')
    list_filter = ('category', 'price')
    search_fields = ('name', 'category', 'about', 'user__username')
