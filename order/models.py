from django.db import models
from shop.models import Product, ProductVariant
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    full_name = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=20, blank=True)

    governorate = models.CharField(max_length=100, blank=True)

    city = models.CharField(max_length=100, blank=True)

    notes = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    address = models.CharField(max_length=255)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=60
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return (
            f"{self.product_variant.product.name}"
            f" - {self.product_variant.color.name}"
            f" - {self.product_variant.size.name}"
            f" x {self.quantity}"
        )