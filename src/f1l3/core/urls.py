from django.urls import path

from core import views

app_name = "f1l3_core"
urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("upload-html/", views.upload_html, name="upload_html"),
    path("download/<slug:alias>", views.download, name="download"),
    path("", views.home, name="home"),
]
