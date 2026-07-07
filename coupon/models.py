from django.db import models


class Coupon(models.Model):

    PERCENTAGE = "percentage"
    FIXED = "fixed"

    DISCOUNT_TYPE = (
        (PERCENTAGE, "Percentage"),
        (FIXED, "Fixed Amount"),
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE,
        default=PERCENTAGE
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    minimum_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    usage_limit = models.PositiveIntegerField(
        default=1
    )

    used_count = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.code