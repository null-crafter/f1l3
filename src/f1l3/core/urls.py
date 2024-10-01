from django.urls import path
from core.views import upload, download
app_name = "core"
urlpatterns = [
    path("upload/", upload, name="upload"),
    path("download/<slug:alias>", download, name="download"),
]