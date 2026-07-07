from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib import messages
from shop.models import ProductVariant
from django.utils import timezone
from coupon.models import Coupon


from cart.models import Cart
from .models import Order, OrderItem

DELIVERY_FEE = Decimal("60.00")


from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render
from django.utils import timezone

@transaction.atomic
@login_required(login_url="login")
def checkout(request):

    cart = Cart.objects.get(user=request.user)

    cart_items = cart.items.select_related(
        "product_variant",
        "product_variant__product",
        "product_variant__color",
        "product_variant__size",
    )

    if not cart_items.exists():
        return redirect("cart")

    subtotal = sum(
        item.total_price
        for item in cart_items
    )

    coupon = None
    discount = Decimal("0")

    coupon_id = request.session.get("coupon_id")

    if coupon_id:

        try:

            coupon = Coupon.objects.get(
                id=coupon_id,
                is_active=True
            )

            now = timezone.now()

            if (
                coupon.valid_from <= now <= coupon.valid_to
                and coupon.used_count < coupon.usage_limit
                and subtotal >= coupon.minimum_order
            ):

                if coupon.discount_type == "percentage":

                    discount = subtotal * (
                        coupon.value / Decimal("100")
                    )

                    if (
                        coupon.maximum_discount
                        and discount > coupon.maximum_discount
                    ):
                        discount = coupon.maximum_discount

                else:

                    discount = coupon.value

            else:

                coupon = None

        except Coupon.DoesNotExist:

            coupon = None

    total = subtotal - discount + DELIVERY_FEE

    if total < DELIVERY_FEE:
        total = DELIVERY_FEE

    if request.method == "POST":

        for item in cart_items:

            variant = item.product_variant

            variant.refresh_from_db()

            if item.quantity > variant.stock:

                messages.error(
                    request,
                    f"Only {variant.stock} pieces available for "
                    f"{variant.product.name} "
                    f"({variant.color.name} / {variant.size.name})"
                )

                return redirect("cart")

        order = Order.objects.create(

            user=request.user,

            full_name=request.POST["name"],

            phone=request.POST["phone"],

            governorate=request.POST["governorate"],

            city=request.POST["city"],

            address=request.POST["address"],

            notes=request.POST.get("notes", ""),

            subtotal=subtotal,

            delivery_fee=DELIVERY_FEE,

            total_price=total,

        )

        order_items = []

        for item in cart_items:

            order_items.append(

                OrderItem(

                    order=order,

                    product_variant=item.product_variant,

                    quantity=item.quantity,

                    price=item.product_variant.product.price,

                )

            )

        OrderItem.objects.bulk_create(order_items)

        for item in cart_items:

            ProductVariant.objects.filter(
                id=item.product_variant.id
            ).update(
                stock=F("stock") - item.quantity
            )

        if coupon:

            coupon.used_count += 1
            coupon.save()

            del request.session["coupon_id"]

        cart_items.delete()

        return redirect("my-orders")

    context = {

        "cart_items": cart_items,

        "subtotal": subtotal,

        "discount": discount,

        "delivery_fee": DELIVERY_FEE,

        "total": total,

    }

    return render(
        request,
        "order/checkout.html",
        context,
    )


@login_required(login_url="login")
def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by("-created_at")
        .prefetch_related(
            "items__product_variant",
            "items__product_variant__product",
            "items__product_variant__color",
            "items__product_variant__size",
        )
    )

    return render(
        request,
        "order/myorders.html",
        {
            "orders": orders
        }
    )



@login_required(login_url="login")
def order_detail(request, id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
                        "items__product_variant",
                        "items__product_variant__product",
                        "items__product_variant__color",
                        "items__product_variant__size",
                    ),
        id=id,
        user=request.user
    )

    subtotal = sum(
        item.price * item.quantity
        for item in order.items.all()
    )

    context = {
        "order": order,
        "subtotal": subtotal,
    }

    return render(
        request,
        "order/orderdetail.html",
        context
    )