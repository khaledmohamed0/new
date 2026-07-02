from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from . import views

urlpatterns=[
    path("profile",views.profile,name="profile"),
    path("login/",views.CustomLoginView.as_view(),name="login"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.LogoutView.as_view(next_page="home"),name="logout"),
    path("change-password/",views.PasswordChangeView.as_view(template_name="account/change_password.html",success_url=reverse_lazy("profile")),name="change_password"),
    

]

