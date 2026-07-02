from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("review/<int:product_id>/",views.add_review,name="add_review"),
]