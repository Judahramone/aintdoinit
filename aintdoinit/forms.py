from django.forms import ModelForm
from .models import ProductVariation, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

#create class for project form
class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields =('size', 'color','stock')

#create class for portfolio form
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields =('title', 'is_active', 'product_type','price', 'description', 'image')
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields= ['username', 'email', 'password1', 'password2']