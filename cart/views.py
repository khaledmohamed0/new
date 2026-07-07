from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Cart,Cart_item,Wishlist,Wishlist_item
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from shop.models import ProductVariant

@login_required(login_url="login")
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    delivery_fee = 60

    if cart:
        cart_items = cart.items.select_related("product_variant","product_variant__product").all()
        
        


        subtotal = sum(
            item.product_variant.product.price * item.quantity
            for item in cart_items
        )

        total = subtotal + delivery_fee 

    else:
        cart_items = []
        subtotal = 0
        total = 0
        delivery_fee = 0

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    }

    return render(request, "cart/cart.html", context)

@login_required(login_url="login")
@require_POST
def add_to_cart(request):

    data = json.loads(request.body)

    variant_id = data.get("variant_id")
    quantity = int(data.get("quantity", 1))

    variant = get_object_or_404(

        ProductVariant,

        id=variant_id,

        is_active=True

    )

    if variant.stock == 0:

        return JsonResponse({

            "success": False,

            "message": "Out of Stock"

        })

    cart, created = Cart.objects.get_or_create(

        user=request.user

    )

    cart_item, created = Cart_item.objects.get_or_create(

        cart=cart,

        product_variant=variant,

        defaults={

            "quantity": quantity

        }

    )

    if not created:

        if cart_item.quantity + quantity > variant.stock:

            return JsonResponse({

                "success": False,

                "message": "Stock limit reached"

            })

        cart_item.quantity += quantity

        cart_item.save()

    return JsonResponse({

        "success": True,

        "message": "Added Successfully",

        "cart_count": cart.items.count()

    })
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        Cart_item,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect(request.META.get("HTTP_REFERER", "cart"))

@login_required(login_url="login")
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()

    if wishlist:
        wishlist_items = wishlist.wishlist_items.select_related("product","wishlist").all()

    else:
        wishlist_items = []

    context = {
        "wishlist": wishlist,
        "wishlist_items": wishlist_items,
    }

    return render(request, "wishlist/wishlist.html", context)


def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(
        Wishlist_item,
        id=item_id,
        wishlist__user=request.user
    )

    wishlist_item.delete()

    return redirect(request.META.get("HTTP_REFERER", "wishlist"))

@login_required(login_url="login")
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user
    )

    wishlist_item, created = Wishlist_item.objects.get_or_create(
        wishlist=wishlist,
        product=product,
        defaults={
            "quantity": quantity
        }
    )

    if not created:
        wishlist_item.quantity += quantity
        wishlist_item.save()

    return redirect("wishlist")


@login_required(login_url="login")
def update_cart_quantity(request):

    data = json.loads(request.body)

    item_id = data.get("item_id")
    action = data.get("action")
    

    item = Cart_item.objects.get(id=item_id)

    if action == "increase":

        if item.quantity < item.product_variant.stock:
            item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1

        item.save()

    item.save()

    cart = item.cart

    cart_items = cart.items.select_related("product_variant", "product_variant__product").all()

    subtotal = sum(
        cart_item.total_price
        for cart_item in cart_items
    )

    discount = 0

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

                request.session.pop("coupon_id", None)

        except Coupon.DoesNotExist:

            request.session.pop("coupon_id", None)

    total = subtotal - discount

    if total < 0:
        total = 0



    
    return JsonResponse({

        "success": True,

        "quantity": item.quantity,

        "item_total": float(item.total_price),

        "subtotal": float(subtotal),

        "discount": float(discount),

        "total": float(total),

    })