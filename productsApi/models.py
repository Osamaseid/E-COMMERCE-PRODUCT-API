from django.contrib.auth.models import AbstractUser
from django.db import models

# Category Schema
class Category(models. Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

# User Schema
class User(AbstractUser):
    email = models.EmailField(unique=True) 
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Set unique related names to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Change this to something unique
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Change this to something unique
        blank=True,
        help_text='Specific permissions for this user.'
    )


# Product Schema
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.URLField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
   
   
# Review Schema
class Review(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Order Schema
class Order (models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Order Items Schema
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


