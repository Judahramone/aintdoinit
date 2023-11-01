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
