from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),
    path("export/",views.export_excel,name="export_excel"),
    path("reviews/",views.reviews,name="dashboard_reviews"),
    path("analytics/",views.analytics,name="dashboard_analytics"),


]