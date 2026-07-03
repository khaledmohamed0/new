from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from cart.models import Cart
from .models import Order, OrderItem

DELIVERY_FEE = Decimal("60.00")


@transaction.atomic
@login_required(login_url="login")
@transaction.atomic
def checkout(request):

    cart = Cart.objects.get(user=request.user)

    cart_items = cart.items.select_related("product").all()

    if not cart_items.exists():
        return redirect("cart")

    subtotal = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    total = subtotal + DELIVERY_FEE

    if request.method == "POST":

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

                    product=item.product,

                    quantity=item.quantity,

                    price=item.product.price,

                )

            )

        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()

        return redirect("my-orders")

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery_fee": DELIVERY_FEE,
        "total": total,
    }

    return render(request, "order/checkout.html", context)




@login_required(login_url="login")
def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
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
        Order.objects.prefetch_related("items__product"),
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