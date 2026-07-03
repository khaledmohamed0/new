

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
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



@login_required(login_url="login")
def add_review(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review, created = Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    "rate": form.cleaned_data["rate"],
                    "review": form.cleaned_data["review"],
                }
            )

            review.user = request.user
            review.product = product

            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    "rate": review.rate,
                    "review": review.review,
                }
            )

        return JsonResponse({
        "success": True,
        "username": request.user.username,
        "review": review.review,
        "rate": review.rate,
        "created_at": review.created_at.strftime("%d %b %Y"),
    })