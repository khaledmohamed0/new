from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from account.models import UserProfile
from shop.models import Review
from cart.models import Wishlist
from order.models import Order
from .forms import CustomPasswordChangeForm,LoginForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm



@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        "profile": profile,

        "orders_count": Order.objects.filter(
            user=request.user
        ).count(),

        "wishlist_count": Wishlist.objects.get(
            user=request.user
        ).wishlist_items.count(),

        "reviews_count": Review.objects.filter(
            user=request.user
        ).count(),
    }

    return render(
        request,
        "account/profile.html",
        context
    )





PasswordChangeView.as_view(

    form_class=CustomPasswordChangeForm,

    template_name="account/change_password.html",

    success_url=reverse_lazy("profile"),

)




class CustomLoginView(LoginView):
    template_name = "account/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        return self.request.GET.get("next") or "/"




def signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = SignupForm()

    return render(
        request,
        "account/signup.html",
        {
            "form": form,
        },
    )