from django.db import models
from django.conf import settings

# Create your models here.
class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        
class Category(Timestamped):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    def __str__(self):
        return self.name

class MenuItem(Timestamped):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    def __str__(self):
        return self.name    
class Order(Timestamped):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    
    @property
    def total_cents(self):
        return sum(item.subtotal_cents for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} — {self.status}"
    
class OrderItem(Timestamped):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_cents = models.PositiveIntegerField()  # snapshot price

    @property
    def subtotal_cents(self):
        return self.quantity * self.price_cents

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"