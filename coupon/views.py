from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from cart.models import Cart,Cart_item
from django.contrib import messages
from django.shortcuts import redirect


@require_POST
def apply_coupon(request):

    code = request.POST.get("code", "").strip()

    try:

        coupon = Coupon.objects.get(
            code__iexact=code,
            is_active=True,
        )

    except Coupon.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "Invalid coupon."
        })

    now = timezone.now()

    if not (coupon.valid_from <= now <= coupon.valid_to):

        return JsonResponse({
            "success": False,
            "message": "Coupon expired."
        })
    
    cart = Cart.objects.get(user=request.user)

    cart_items = cart.items.select_related(
        "product_variant",
        "product_variant__product"
    )

    subtotal = sum(
        item.total_price
        for item in cart_items
    )

    if subtotal < coupon.minimum_order:

        return JsonResponse({
            "success": False,
            "message": f"Minimum order is {coupon.minimum_order} EGP."
        })

    if coupon.discount_type == "percentage":

        discount = subtotal * (coupon.value / 100)

        if (
            coupon.maximum_discount and
            discount > coupon.maximum_discount
        ):
            discount = coupon.maximum_discount

    else:

        discount = coupon.value

    total = subtotal - discount

    if total < 0:
        total = 0

    if coupon.used_count >= coupon.usage_limit:

        return JsonResponse({
            "success": False,
            "message": "Coupon usage limit reached."
        })

    request.session["coupon_id"] = coupon.id

    return JsonResponse({

        "success": True,

        "subtotal": float(subtotal),

        "discount": float(discount),

        "total": float(total),

    })