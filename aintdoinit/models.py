from django.db import models
from django.urls import reverse

class Size(models.Model):
    SIZE_CHOICES = [
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('LG', 'Large'),
        ('XL', 'Extra-Large'),
    ]
    value = models.CharField(max_length=2, choices=SIZE_CHOICES, unique=True)

class Color(models.Model):
    COLOR_CHOICES = [
        ('W', 'White'),
        ('K', 'Black'),
        ('B', 'Blue'),
        ('G', 'Green'),
        ('R', 'Red'),
    ]
    value = models.CharField(max_length=1, choices=COLOR_CHOICES, unique=True)   

class Product(models.Model):
    PRODUCT_TYPE = (
        ('SK', 'Sticker'),
        ('TS', 'Short Sleeve T-shirt'),
        ('TL', 'Long Sleeve T-shirt'),
        ('HZ', 'Zip-Up Hoodie '),
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
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

class Mod(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    
    def __str__(self):
        return self.product.title  # reference to product's title


