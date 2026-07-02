from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from account.models import UserProfile
from cart.models import Cart, Wishlist

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)