from django.contrib import admin
from .models import Product, Mod, Color, Size

# Register your models here.
admin.site.register(Product)
admin.site.register(Mod)
admin.site.register(Color)
admin.site.register(Size)