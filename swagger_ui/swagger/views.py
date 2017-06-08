from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import DocumentSerializer
from .utils import del_none


class DocumentView(APIView):
    def get(self, request, doc_id):
        doc = models.Document.objects.get(pk=doc_id)
        serializer = DocumentSerializer(doc)
        data = dict(serializer.data)
        return Response(del_none(data))
