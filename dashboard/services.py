from shop.models import Product
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from order.models import OrderItem,Order
from django.db.models import Sum,F,DecimalField,ExpressionWrapper
from django.db.models.functions import ExtractMonth,TruncMonth
from decimal import Decimal
from django.db.models import Q
import json
from django.utils import timezone
from django.db.models import Count

COMMISSION_RATE = Decimal("0.04")

User = get_user_model()


def calculate_revenue(queryset):

    gross_sales = queryset.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("price") * F("quantity"),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )["total"] or Decimal("0")

    return gross_sales * COMMISSION_RATE

def get_total_products():
    return Product.objects.count()



def get_total_customers():
    return User.objects.count()

def get_total_orders():
    return Order.objects.count()

def get_total_sold():

    return (
        OrderItem.objects.filter(
            order__status="delivered"
        ).aggregate(
            total=Sum("quantity")
        )["total"] or 0
    )



def get_total_revenue():

    gross_sales = (
        OrderItem.objects
        .filter(order__status="delivered")
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("price") * F("quantity"),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            )
        )["total"] or Decimal("0")
    )

    return gross_sales * COMMISSION_RATE
    return revenue



def get_products_statistics():

    products = (
        Product.objects.annotate(

            sold=Sum(
                "orderitem__quantity",
                filter=Q(orderitem__order__status="delivered")
            )

        )
    )

    data = []

    for product in products:

        sold = product.sold or 0

        gross_sales = product.price * sold

        revenue = gross_sales * COMMISSION_RATE

        data.append({

            "product": product,

            "sold": sold,

            "gross_sales": gross_sales,

            "revenue": revenue,

        })

    return data


def get_today_revenue():

    today = timezone.now().date()

    revenue = Decimal("0")

    items = OrderItem.objects.filter(
        order__created_at__date=today
    ).exclude(
        order__status="cancelled"
    )

    for item in items:

        revenue += (
            item.price *
            item.quantity *
            COMMISSION_RATE
        )

    return revenue

def get_month_revenue():

    now = timezone.now()

    revenue = Decimal("0")

    items = OrderItem.objects.filter(

        order__created_at__year=now.year,

        order__created_at__month=now.month,

    ).exclude(

        order__status="cancelled"

    )

    for item in items:

        revenue += (
            item.price *
            item.quantity *
            COMMISSION_RATE
        )

    return revenue

def get_monthly_revenue():

    current_year = timezone.now().year

    data = (
        OrderItem.objects
        .filter(
            order__status="delivered",
            order__created_at__year=current_year
        )
        .annotate(
            month=ExtractMonth("order__created_at")
        )
        .values("month")
        .annotate(
            revenue=Sum(
                ExpressionWrapper(
                    F("price") * F("quantity"),
                    output_field=DecimalField(
                        max_digits=15,
                        decimal_places=2
                    )
                )
            )
        )
        .order_by("month")
    )

    monthly_revenue = [0] * 12

    for item in data:

        monthly_revenue[item["month"] - 1] = float(
            item["revenue"] * COMMISSION_RATE
        )

    return monthly_revenue


def get_dashboard_statistics():

    return {

        "total_products": get_total_products(),

        "total_customers": get_total_customers(),

        "total_pieces_sold": get_total_sold(),

        "total_revenue": get_total_revenue(),

        "today_revenue": get_today_revenue(),

        "month_revenue": get_month_revenue(),

    }

def get_top_selling_products(limit=5):

    products = (
        OrderItem.objects
        .filter(order__status="delivered")
        .values(
            "product__id",
            "product__name",
        )
        .annotate(

            pieces_sold=Sum("quantity"),

            orders_count=Count(
                "order",
                distinct=True
            ),

            gross_sales=Sum(
                ExpressionWrapper(
                    F("price") * F("quantity"),
                    output_field=DecimalField(
                        max_digits=15,
                        decimal_places=2
                    )
                )
            )

        )
        .order_by("-pieces_sold")[:limit]
    )

    for product in products:

        product["revenue"] = (
            product["gross_sales"] *
            COMMISSION_RATE
        )

    return products