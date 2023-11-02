from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum


class Size(models.Model):
    SIZE_CHOICES = [
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('LG', 'Large'),
        ('XL', 'Extra-Large'),
    ]
    value = models.CharField(max_length=2, choices=SIZE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_value_display()

class Color(models.Model):
    COLOR_CHOICES = [
        ('W', 'White'),
        ('K', 'Black'),
        ('B', 'Blue'),
        ('G', 'Green'),
        ('R', 'Red'),
    ]
    value = models.CharField(max_length=1, choices=COLOR_CHOICES, unique=True)   
    
    def __str__(self):
        return self.get_value_display()

class Product(models.Model):
    PRODUCT_TYPE = (
        ('SK', 'Sticker'),
        ('TS', 'Short Sleeve T-shirt'),
        ('TL', 'Long Sleeve T-shirt'),
        ('HZ', 'Zip-Up Hoodie'),
        ('HP', 'Pull-Over Hoodie'),
        ('CP', 'Cap'),
        ('MS', 'Miscellaneous')
    )
    
    title = models.CharField("Title", max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=False)
    description = models.TextField("About",blank=True)
    product_type = models.CharField(max_length=2, choices=PRODUCT_TYPE)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/", max_length=100)
    
    def __str__(self):
        return f"{self.title} ({self.get_product_type_display()})"

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.size.value} - {self.color.value} ({self.stock})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the variation first
        total_stock = ProductVariation.objects.filter(product=self.product).aggregate(total_stock=Sum('stock'))['total_stock']
        self.product.is_active = total_stock > 0
        self.product.save()

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_variation.product.title} - {self.quantity} item(s)"