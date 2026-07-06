from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/<int:id>/review/",views.add_review,name="add_review"),
]