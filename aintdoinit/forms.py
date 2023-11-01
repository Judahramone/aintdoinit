from django.forms import ModelForm
from .models import ProductVariation, Product

#create class for project form
class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields =('size', 'color','stock','product')

#create class for portfolio form
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields =('title', 'product_type', 'is_active', 'price', 'description', 'image')