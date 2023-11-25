from django.contrib import admin
from .models import Product, ProductVariation, Color, Size, Customer, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Customer)
admin.site.register(Cart)