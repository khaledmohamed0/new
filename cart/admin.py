from django.contrib import admin
from .models import Cart, Cart_item, Wishlist, Wishlist_item


class CartItemInline(admin.TabularInline):
    model = Cart_item
    extra = 0
class WishlistItemInline(admin.TabularInline):
    model = Wishlist_item
    extra = 0    


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)
    inlines = [CartItemInline]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)
    inlines = [WishlistItemInline]

