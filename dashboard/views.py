from django.shortcuts import render
from openpyxl import Workbook
import csv
from django.http import HttpResponse
from .services import *
from django.core.paginator import Paginator
from shop.models import Product,Review

def dashboard(request):

    context = {

        "total_products": get_total_products(),

        "total_customers": get_total_customers(),

        "total_orders": get_total_orders(),

        "total_sold": get_total_sold(),

        "total_revenue": get_total_revenue(),

        "products": get_products_statistics(),

        "today_revenue": get_today_revenue(),

        "month_revenue": get_month_revenue(),


    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )




def export_excel(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response, delimiter=";")

    writer.writerow([
        "Product",
        "Price",
        "Pieces Sold",
        "Gross Sales",
        "Revenue",
    ])

    for item in get_products_statistics():

        writer.writerow([

            item["product"].name,

            item["product"].price,

            item["sold"],

            item["gross_sales"],

            item["revenue"],

        ])

    return response





def reviews(request):

    reviews = (
        Review.objects
        .select_related("user", "product")
        .order_by("-created_at")
    )

    paginator = Paginator(reviews, 10)

    page = request.GET.get("page")

    page_obj = paginator.get_page(page)

    return render(
        request,
        "dashboard/reviews.html",
        {
            "page_obj": page_obj
        },
    )


def analytics(request):

    context = get_dashboard_statistics()

    context["monthly_revenue"] = json.dumps(
        get_monthly_revenue()
    )

    context["top_products"] = get_top_selling_products()

    return render(
        request,
        "dashboard/analytics.html",
        context
    )
        

    

    