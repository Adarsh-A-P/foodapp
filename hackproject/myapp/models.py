from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FoodItem(models.Model):
    FOOD_TYPES = [
        ('cooked', 'Cooked Food'),
        ('raw', 'Raw Ingredients'),
        ('packaged', 'Packaged Food'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    expiry_date = models.DateTimeField()
    location = models.CharField(max_length=200)  # Location as text
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    location_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.username} on {self.date_posted}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)  # kg, dozen, etc.
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
