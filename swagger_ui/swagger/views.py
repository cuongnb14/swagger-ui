from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import DocumentSerializer


class DocumentView(APIView):
    def get(self, request, doc_id):
        doc = models.Document.objects.get(pk=doc_id)
        serializer = DocumentSerializer(doc)
        return Response(serializer.data)
