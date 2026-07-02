from django.urls import path
from .views import cart,add_to_cart,remove_from_cart,wishlist,remove_from_wishlist,add_to_wishlist


urlpatterns = [
    path('',cart,name='cart'),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path('wishlist/', wishlist, name='wishlist'),
    path("wishlist/remove/<int:item_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    path("wishlist/add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),

]