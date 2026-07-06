from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    sku = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,blank=True)


    def avg_rate(self):
        avg = self.review_product.aggregate(avg_rate=Avg('rate'))
        if not avg['avg_rate']:
            result = 0
            return result
        return avg['avg_rate']

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product , related_name='product_image', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images')

    def __str__(self):
        return str(self.product)

class Size(models.Model):

    name = models.CharField(
        max_length=10,
        unique=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Color(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    hex_code = models.CharField(
        max_length=7,
        default="#000000"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(default=True)

    class Meta:

        unique_together = (
            "product",
            "size",
            "color",
        )

        ordering = [
            "product",
            "color",
            "size",
        ]

    def __str__(self):

        return (
            f"{self.product.name}"
            f" - {self.color.name}"
            f" - {self.size.name}"
        )





#_____________________________________________________
class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_author', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(
        validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ]
    )
    review = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_review_per_user_product",
            )
        ]

    def __str__(self):
        return f"{self.user} rated {self.product.name}"

    @classmethod
    def count_reviews_by_user(cls, user):
        return cls.objects.filter(user=user).count()