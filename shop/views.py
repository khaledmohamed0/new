

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product,Review
from django.db.models import Avg
from .forms import ReviewForm

def products(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "shop/products.html", context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.product_image.all()
    reviews = Review.objects.filter(
        product=product
    ).select_related("user").order_by("-created_at")

    form = ReviewForm()


    context = {
        "product": product,
        "reviews": reviews,
        "form": form,
        "review_count": product.review_product.count(),
        "average_rating": reviews.aggregate(avg=Avg("rate"))["avg"] or 0,
        "images": images,

    }

    return render(request, "shop/product_detail.html", context)



def add_review(request, product_id):

    return 0,