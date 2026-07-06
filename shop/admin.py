from django.contrib import admin
from .models import Product, ProductImage, Review, ProductVariant, Size, Color


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):

    model = ProductVariant

    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    

    list_display = (
        "name",
        "price",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        ProductVariantInline,
        ProductImageInline,
    ]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "hex_code",
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "color",
        "size",
        "stock",
        "is_active",
    )

    list_filter = (
        "color",
        "size",
        "is_active",
    )


admin.site.register(Review)