

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Product,Review,ProductImage,ProductVariant
from django.db.models import Avg
import json
from .forms import ReviewForm
from django.core.paginator import Paginator

def products(request):
    products = Product.objects.all().order_by("-id")

    paginator = Paginator(products, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "shop/products.html", context)

def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    images = product.product_image.all()

    reviews = (
        Review.objects
        .filter(product=product)
        .select_related("user")
        .order_by("-created_at")
    )

    variants = (
        product.variants
        .select_related("color", "size")
        .filter(is_active=True)
    )

    colors = []

    for variant in variants:
        if variant.color not in colors:
            colors.append(variant.color)

    form = ReviewForm()

    variants_json = []

    for variant in variants:

        variants_json.append({
            "id": variant.id,
            "color_id": variant.color.id,
            "color": variant.color.name,
            "size": variant.size.name,
            "stock": variant.stock,
        })

    context = {
        "product": product,
        "images": images,
        "reviews": reviews,
        "form": form,
        "variants": variants,
        "colors": colors,
        "review_count": product.review_product.count(),
        "average_rating": reviews.aggregate(avg=Avg("rate"))["avg"] or 0,
        "variants_json": json.dumps(variants_json),
    }

    return render(
        request,
        "shop/product_detail.html",
        context
    )



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

            return JsonResponse({

                "success": True,
                "username": request.user.username,
                "review": review.review,
                "rate": review.rate,
                "created_at": review.created_at.strftime("%d %b %Y"),

            })

        return JsonResponse({
            "success": False,
            "errors": form.errors
        })

    return JsonResponse({
        "success": False
    })