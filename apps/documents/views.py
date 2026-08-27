from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from .models import Document
from .serializers import DocumentSerializer
from .tasks import ingest_document


class DocumentViewSet(viewsets.ModelViewSet):
    """F1 (upload), D2 (statut), F10/D11 (suppression/réindexation par un admin)."""

    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        document = serializer.save(
            owner=self.request.user,
            original_filename=self.request.FILES["file"].name,
        )
        # F2 : ingestion asynchrone, ne bloque pas la requête HTTP (cf. 17.1 Définition de Done)
        ingest_document.delay(document.id)
