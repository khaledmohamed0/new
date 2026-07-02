from django.shortcuts import render
from shop.models import Product
from cart.models import Cart_item

# Create your views here.
def home(request):
    products = Product.objects.all()[:8]

   
 

    context = {
        "products": products,
        
    }

    return render(request,'Home/index.html',context)    