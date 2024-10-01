from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from core.serializers import UploadedFileSerializer
from core.models import UploadedFile

# Create your views here.
@api_view(["POST"])
def upload(request):
    serializer = UploadedFileSerializer(data=request.data) 
    serializer.is_valid()
    instance = serializer.save()
    return Response({"alias": instance.alias})

@api_view(["GET"])
def download(request, alias):
    uploaded_file = UploadedFile.objects.filter(alias=alias).first()
    if not uploaded_file:
        raise NotFound()
    file = open(uploaded_file.file.path, "rb")
    return FileResponse(file)
