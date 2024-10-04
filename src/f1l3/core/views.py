from django.http import FileResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from core.models import UploadedFile
from core.serializers import UploadedFileSerializer
from django.conf import settings
import typing as t

def get_base_url() -> t.Optional[str]:
    if settings.HOST == settings.EXAMPLE_HOST:
        return None
    return f"https://{settings.HOST}/"

def home(request):
    base_url = get_base_url() or f"https://{settings.EXAMPLE_HOST}/"
    return render(request, "core/index.html", {"base_url": base_url})


@api_view(["POST"])
def upload(request):
    serializer = UploadedFileSerializer(data=request.data)
    serializer.is_valid()
    instance = serializer.save()
    base_url = get_base_url()
    if base_url:
        return Response({"url": f"{base_url}download/{instance.alias}"})
    else:
        return Response({"alias": instance.alias})


@api_view(["POST"])
def upload_html(request):
    data = request.data
    serializer = UploadedFileSerializer(data=data)
    serializer.is_valid()
    instance = serializer.save()
    base_url = get_base_url() or f"https://{settings.EXAMPLE_HOST}/"
    return render(
        request,
        "core/uploaded.html",
        {"filename": data["file"].name, "alias": instance.alias, "base_url": base_url},
    )


@api_view(["GET"])
def download(request, alias):
    uploaded_file = UploadedFile.objects.filter(alias=alias).first()
    if not uploaded_file:
        raise NotFound()
    file = open(uploaded_file.file.path, "rb")
    return FileResponse(file)
