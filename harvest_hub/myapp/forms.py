from django import forms

from .models import Crop, Inventory, Sale, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


CATEGORY_CHOICES = [
    ('Farmer', 'Farmer'),
    ('Buyer', 'Buyer'),
]

class CustomRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=15)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'category', 'name', 'about', 'price']