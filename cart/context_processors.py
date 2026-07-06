# cart/context_processors.py

from .models import Cart_item,Wishlist_item

def cart_data(request):
    cart_items = Cart_item.objects.none()
    cart_count = 0
    cart_total = 0
    wishlist_items = Wishlist_item.objects.none()
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_items = (
            Cart_item.objects
            .filter(cart__user=request.user)
            .select_related("product_variant", "product_variant__product","cart")
            .prefetch_related("product_variant__product__product_image")
        )
        wishlist_items = (
            Wishlist_item.objects
            .filter(wishlist__user=request.user)
            .select_related("product","wishlist")
            .prefetch_related("product__product_image")
        )

        cart_count = cart_items.count()
        wishlist_count = wishlist_items.count()

        cart_total = sum(
            item.product_variant.product.price * item.quantity
            for item in cart_items
        )

    return {
        "cart_items": cart_items,
        "cart_count": cart_count,
        "cart_total": cart_total,
        "wishlist_items": wishlist_items,
        "wishlist_count": wishlist_count,
    }