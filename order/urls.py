from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path(
    "my-orders/<int:id>/",
    views.order_detail,
    name="order_detail",
)

]