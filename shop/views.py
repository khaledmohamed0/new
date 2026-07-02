

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Avg

def products(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "shop/products.html", context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.product_image.all()
    reviews = product.review_product.select_related("user")


    context = {
        "product": product,
        "reviews": reviews,
        "review_count": product.review_product.count(),
        "average_rating": reviews.aggregate(avg=Avg("rate"))["avg"] or 0,
        "images": images,

    }

    return render(request, "shop/product_detail.html", context)