from django.urls import path

from .views import collection_view

urlpatterns = [
    path("", collection_view.html_view, name="index"),
    path("rf/", collection_view.read_file, name="read_file"),
]