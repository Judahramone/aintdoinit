from django.forms import ModelForm
from .models import Mod, Product

#create class for project form
class ModForm(ModelForm):
    class Meta:
        model = Mod
        fields =('sizes', 'colors')

#create class for portfolio form
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields =('title', 'product_type', 'is_active', 'price', 'description', 'image')