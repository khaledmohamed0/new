from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_type",
        "value",
        "minimum_order",
        "usage_limit",
        "used_count",
        "is_active",
        "valid_from",
        "valid_to",
    )

    search_fields = (
        "code",
    )

    list_filter = (
        "discount_type",
        "is_active",
    )